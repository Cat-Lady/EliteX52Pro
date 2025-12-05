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


### Install paho-mqtt:


#### Option 1 (system install)
``apt-get install python3-paho-mqtt`` (or quivalent for other package managers)


#### Option 2: With pip
``python3 -m pip install paho-mqtt``


#### Option 3 (pipx external environment)
``pipx install .``


### download the code:

either the zip file (unpack it), or with git:

``git clone https://github.com/Cat-Lady/EliteX52Pro.git``


### Run with:

``python3 elitex52pro.py [--debug]``


## 📁 Config files


Edit your configuration files in the same directory as the script:


``default.config``

``silent-running.config``


Each line should contain:
``<topic> <payload> <path-to-script-to-run>``


Example:

```
Telemetry/Dashboard/Flags/LandingGearDown 1 "./enabling/landing.sh"
Telemetry/Dashboard/Flags/LandingGearDown 0 "./disabling/landing-off.sh"
```


The `default.config` and `silent-running.config` are populated with entries for using scripts from `/enabling` and `/disabling` directories. Default color schemes are in the `/base` directory. One can use them as-is for pretty complete set, edit them, or to use as examples for creating completely new ones.


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
```
MIT License.
Free for personal and non-commercial use.
```
