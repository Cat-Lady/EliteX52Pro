# EliteX52Pro

**EliteX52Pro** is a lightweight Python automation tool that bridges Elite Dangerous telemetry (via MQTT, EDMC and EDMC-Telemetry plugin) with Logitech X52 Pro joystick LED control scripts.
It is developed and created with Linux environments in mind and X52Pro HOTAS setup, but can be altered to run in any platform and with any controller hardware, as long as the platform have any tools to control state of the hardware (leds, MFD, rumble, whatever) programatically from command line.

It dynamically reacts to in-game events such as:
- Landing gear,
- Silent running,
- Cargo scoop,
- Lights,
- Supercruise,
- FSD states,
...and more (everything that can be parsed from journal and dashboard states)

and triggers corresponding (fully customizable) LED scripts.

---

## 🧩 Features
- Uses `paho-mqtt` for fast local telemetry subscription.
- Dynamically switches between config sets (for now, `default.config`, `silent-running.config`).
- Spawns scripts safely in separate process groups (for clean termination).
- Supports subfolders and quoted paths in config files


---

## ⚙️ Installation

### Option 1 (system install)
Install paho-mqtt (for example, on Debian-based systems: apt-get install python3-paho-mqtt)
Run with:
python3 elitex52pro.py [--debug]

### Option 2: With pip
python3 -m pip install paho-mqtt
Run with:
python3 elitex52pro.py [--debug]


### Option 3 (pipx external environment)
pipx install .
Run with:
elitex52pro [--debug]

## 📁 Config files

Edit your configuration files in the same directory as the script:

default.config
silent-running.config

Each line should contain:
<topic> <payload> <path-to-script-to-run>

Example:

Telemetry/Dashboard/Flags/LandingGearDown 1 "./enabling/landing.sh"
Telemetry/Dashboard/Flags/LandingGearDown 0 "./disabling/landing-off.sh"

## Stopping
If launching headless, use an external script to kill, for example:

```
#!/bin/bash
PID_FILE="/tmp/elitex52pro.pid"
if [ -f "$PID_FILE" ]; then
    kill "$(cat "$PID_FILE")"
    rm -f "$PID_FILE"
fi
```

## 📜 License
MIT License.
Free for personal and non-commercial use.
