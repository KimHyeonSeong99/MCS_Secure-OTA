from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion
import os
import time  # Added for delay
import json  # Added for JSON handling
import shutil

FIRMWARE_DIR = "firmwares"
OTA_DIR = "updates"
NOTIFIED_FILES = "notified_files.json"
os.makedirs(FIRMWARE_DIR, exist_ok=True)
os.makedirs(OTA_DIR, exist_ok=True)

def load_notified_files():
    if os.path.exists(NOTIFIED_FILES):
        with open(NOTIFIED_FILES, "r") as f:
            return set(json.load(f))
    return set()

def save_notified_files(seen_files):
    with open(NOTIFIED_FILES, "w") as f:
        json.dump(list(seen_files), f)

def monitor_directory():
    seen_files = load_notified_files()  # Load notified files
    client = Client(callback_api_version=CallbackAPIVersion.VERSION2)
    client.username_pw_set("mose", "3103")
    client.connect("203.246.114.61", 12010)
    while True:
        current_files = set(os.listdir(FIRMWARE_DIR))
        new_files = current_files - seen_files
        if new_files:
            
            client.loop_start()
            for file in new_files:
                shutil.move(os.path.join(FIRMWARE_DIR, file), os.path.join(OTA_DIR, file))
                client.publish("ota/updates", file.encode(), qos = 2, retain=True)
                print(f"New OTA file available: {file}")
                seen_files.update(new_files)  # Update seen files
                save_notified_files(seen_files)  # Save updated list
                time.sleep(10)
            client.loop_stop()
            client.disconnect()
        time.sleep(10)  # Add delay to reduce CPU usage

if __name__ == "__main__":
    monitor_directory()
