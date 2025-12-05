import paho.mqtt.client as mqtt
import os
import random

# --- SETTINGS ---
BROKER = "localhost"
PORT = 1883
CONFIG_FILE = "default.config"  # or "silent-running.config"

# --- LOAD TOPICS FROM CONFIG ---
def load_topics(config_file):
    topics = {}
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found!")
        return topics
    with open(config_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                topic, value, _ = line.split(maxsplit=2)
                if topic not in topics:
                    topics[topic] = set()
                topics[topic].add(value)
            except ValueError:
                continue
    return topics

# --- MQTT SETUP ---
client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

topics = load_topics(CONFIG_FILE)
if not topics:
    print("No topics loaded. Check your config.")
    exit(1)

print(f"Loaded {len(topics)} topics from {CONFIG_FILE}:")
for t, values in topics.items():
    print(f"  {t} -> {values}")

print("\nInteractive MQTT simulator started!")
print("Type 'topic payload' and press Enter to publish.")
print("Press Enter without typing anything to publish random payloads.")
print("Ctrl+C to stop.\n")

try:
    while True:
        user_input = input(">>> ").strip()
        if user_input:
            try:
                topic, payload = user_input.split(maxsplit=1)
                if topic in topics:
                    client.publish(topic, payload)
                    print(f"Published: {topic} -> {payload}")
                else:
                    print(f"Invalid topic or payload. Allowed payloads for {topic}: {topics.get(topic, set())}")
            except ValueError:
                print("Invalid input format. Use: topic payload")
        else:
            # Random publish if user presses Enter
            topic = random.choice(list(topics.keys()))
            payload = random.choice(list(topics[topic]))
            client.publish(topic, payload)
            print(f"Randomly published: {topic} -> {payload}")

except KeyboardInterrupt:
    print("\nSimulation stopped by user.")
    client.loop_stop()
