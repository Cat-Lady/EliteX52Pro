#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import subprocess
import os
import sys
import signal
import shlex
import time
import psutil  # <-- standard library? no, external — we'll handle later if needed


# -------- Configuration --------
BROKER = "localhost"
PORT = 1883

CONFIG_DEFAULT = "default.config"
CONFIG_SILENT = "silent-running.config"
TRIGGER_TOPIC = "Telemetry/Dashboard/Flags/SilentRunning"

# PID file location
PID_FILE = "/tmp/elitex52pro.pid"

# Debug flag
DEBUG = "--debug" in sys.argv

# Base directory (directory where this script lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------- State --------
rules_default = {}
rules_silent = {}
active_rules = {}
current_mode = None
running_processes = {}
last_payload = {}


# -------- Logging --------
def log(msg, level="INFO", debug_only=False):
    if debug_only and not DEBUG:
        return
    print(f"[{level}] {msg}")


# -------- PID Management --------
def check_existing_instance():
    """Check if another instance of this program is already running."""
    if not os.path.exists(PID_FILE):
        return  # no PID file -> safe to continue

    try:
        with open(PID_FILE, "r") as f:
            pid_str = f.read().strip()
        if not pid_str:
            return
        pid = int(pid_str)
    except Exception:
        # malformed PID file -> remove it
        try:
            os.remove(PID_FILE)
        except Exception:
            pass
        return

    # Check if process with that PID exists
    try:
        if psutil.pid_exists(pid):
            p = psutil.Process(pid)
            cmdline = " ".join(p.cmdline())
            # defensive check: confirm it's really this script
            if os.path.basename(__file__) in cmdline:
                print(f"[ERROR] Another instance of elitex52pro is already running (PID {pid}).")
                sys.exit(1)
        # if PID exists but not our script -> overwrite
    except Exception:
        # can't access process info -> assume stale PID file
        pass

    # stale PID file
    try:
        os.remove(PID_FILE)
    except Exception:
        pass


def write_pid():
    """Write PID file for this process."""
    try:
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception as e:
        log(f"Failed to write PID file {PID_FILE}: {e}", "ERROR")


def cleanup():
    """Kill child processes and remove PID file."""
    log("Cleaning up before exit...")
    for key, proc in list(running_processes.items()):
        try:
            if proc.poll() is None:
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                    proc.wait(timeout=2)
                except Exception:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except Exception:
                        pass
        except Exception as e:
            log(f"Error while killing process {key}: {e}", "ERROR")
        finally:
            running_processes.pop(key, None)
    try:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    except Exception as e:
        log(f"Failed to remove PID file: {e}", "ERROR")


def handle_exit(signum, frame):
    cleanup()
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)


# -------- Config Loader --------
def load_config(filename):
    rules = {}
    if not os.path.exists(filename):
        log(f"Config file {filename} not found.", "WARN")
        return rules

    log(f"Loading config {filename}...")
    with open(filename, "r") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                parts = shlex.split(line)
                if len(parts) < 3:
                    raise ValueError("expected at least 3 tokens (topic value script)")
                topic = parts[0]
                value = parts[1]
                script_token = parts[2]
                if len(parts) > 3:
                    script_token = " ".join(parts[2:])

                script_token = os.path.expanduser(script_token)
                if not os.path.isabs(script_token):
                    script_token = os.path.join(BASE_DIR, script_token)
                script_path = os.path.abspath(script_token)

                rules.setdefault(topic, {})[value] = script_path
                log(f"Rule loaded: {topic} -> {value} => {script_path}", "DEBUG", debug_only=True)
            except Exception as e:
                log(f"Invalid line in {filename}: {line} ({e})", "ERROR")
    return rules


# -------- Process management --------
def kill_all_processes(exclude_keys=None):
    global running_processes
    exclude_keys = exclude_keys or []
    if running_processes:
        log(f"Killing {len(running_processes)} running processes due to config switch.", "INFO")
    for key, proc in list(running_processes.items()):
        if key in exclude_keys:
            continue
        try:
            if proc.poll() is None:
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                    proc.wait(timeout=2)
                except Exception:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except Exception:
                        pass
        except Exception as e:
            log(f"Error killing process {key}: {e}", "ERROR")
        finally:
            running_processes.pop(key, None)


def set_active_rules(mode, exclude_keys=None):
    global active_rules, current_mode, last_payload
    if current_mode is not None and mode == current_mode:
        log(f"Config {mode} already active; skipping switch.", "DEBUG", debug_only=True)
        return

    kill_all_processes(exclude_keys=exclude_keys)
    last_payload = {}
    active_rules = rules_default if mode == "default" else rules_silent
    current_mode = mode
    log(f"Switched active rules to {mode} config.")


def run_matching_rule(topic, payload):
    last = last_payload.get(topic)
    if last == payload:
        log(f"Skipping {topic}={payload}, same as last payload.", "DEBUG", debug_only=True)
        return
    last_payload[topic] = payload

    if topic not in active_rules or payload not in active_rules[topic]:
        log(f"No rule for topic {topic} with payload '{payload}' in {current_mode} config.", "MISS", debug_only=True)
        return

    script = active_rules[topic][payload]
    key = (topic, payload)
    if not os.path.isfile(script):
        log(f"Script file not found or not a file: {script}", "ERROR")
        return

    try:
        if DEBUG:
            proc = subprocess.Popen(["bash", script],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    preexec_fn=os.setsid)
        else:
            proc = subprocess.Popen(["bash", script],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    preexec_fn=os.setsid)
        running_processes[key] = proc
        log(f"Script {script} started in background (pid={proc.pid}).", "EXEC", debug_only=True)

        if DEBUG:
            time.sleep(0.05)
            rc = proc.poll()
            if rc is not None:
                out, err = proc.communicate(timeout=0.1)
                log(f"Script {script} exited immediately (code {rc}). stdout={out!r}, stderr={err!r}", "ERROR")
                running_processes.pop(key, None)
    except Exception as e:
        log(f"Failed to spawn script {script}: {e}", "ERROR")
        running_processes.pop(key, None)


# -------- MQTT --------
def on_connect(client, userdata, flags, rc):
    log(f"Connected to broker with result code {rc}")
    client.subscribe("#")
    log("Subscribed to all topics (#)", debug_only=True)


def on_message(client, userdata, msg):
    global current_mode
    topic = msg.topic
    payload = msg.payload.decode("utf-8").strip()

    log(f"Topic={topic} Payload='{payload}' (mode={current_mode})", "MQTT", debug_only=True)
    run_matching_rule(topic, payload)

    if topic == TRIGGER_TOPIC:
        exclude = [(topic, payload)]
        if payload == "1" and current_mode != "silent":
            set_active_rules("silent", exclude_keys=exclude)
        elif payload == "0" and current_mode != "default":
            set_active_rules("default", exclude_keys=exclude)
        elif payload not in ("0", "1"):
            log(f"Unknown SilentRunning payload: {payload}", "WARN")


# -------- main --------
def main():
    global rules_default, rules_silent
    check_existing_instance()   # <---- New instance check here

    rules_default = load_config(CONFIG_DEFAULT)
    rules_silent = load_config(CONFIG_SILENT)
    set_active_rules("default")

    write_pid()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    log(f"Connecting to {BROKER}:{PORT} ...")
    client.connect(BROKER, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
