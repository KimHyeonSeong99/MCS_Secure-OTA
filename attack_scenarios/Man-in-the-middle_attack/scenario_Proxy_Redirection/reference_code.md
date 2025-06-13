```
attack_scenarios/
└── Man-in-the-middle_attack/
    └── scenario_Proxy_Redirection/
        ├── README.md         # scenario description
        ├── images/           # Diagrams, explanatory pictures
        └── reference_code/   # Folder dedicated to reference code
            ├── server/
            │   ├── fake_ota_server.py
            │   └── fake_ota_update.bin
            └── client/
                └── vehicle_module.py
```

### 1. Basic Concept Explanation

This code demonstrates a simple simulation of a Man-in-the-Middle (MITM) attack during a car's OTA update process.

- MITM is a "Man-in-the-Middle" attack. A hacker intercepts communication in the middle.
- If a car receives an update without security, a hacker can send a malicious file to take control of or damage the vehicle.
### 2. Execution environment and preparation

Requirements

- Install Python 3
- Install the Flask library
```shell
#Install Flask by typing the following command in your terminal:

pip install flask
```

### 3. Code description by file

`fake_ota_server.py`

- Role: Fake OTA server created by hacker
- What it does: When someone accesses `/ota`, it sends a fake update file (`fake_ota_update.bin`).
- How to run:
fake_ota_server.py
```python
import requests

url = "http://ota.com:8000/ota"

print("[Vehicle] Sending OTA update request...")

response = requests.get(url)

if response.status_code == 200:
    with open("downloaded_ota.bin", "wb") as f:
        f.write(response.content)
    print("[Vehicle] OTA file received! Saved as downloaded_ota.bin")
else:
    print("[Vehicle] Failed to download OTA file. Status code:", response.status_code)

```

`vehicle_module.py`

- Role: Code that acts as a car
- What it does: Requests `http://ota.com:8000/ota` to get updates, and saves the received files.
- How to run:
vehicle_module.py
```python
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/ota")
def send_fake_file():
     return send_file("fake_ota_update.bin", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```
