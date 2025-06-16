# vehicle_module.py

import requests

url = "http://127.0.0.1:8000/ota"

print("[Vehicle] Sending OTA update request...")

response = requests.get(url)

if response.status_code == 200:
    with open("downloaded_ota.bin", "wb") as f:
        f.write(response.content)
    print("[Vehicle] OTA file received! Saved as downloaded_ota.bin")
else:
    print("[Vehicle] Failed to download OTA file. Status code:", response.status_code)
