# Scenario Name: MITM Attack via Proxy Redirection on Insecure OTA Update System

This project simulates a Man-In-The-Middle (MITM) attack on an insecure OTA (Over-The-Air) update system.

The attacker intercepts and redirects OTA requests, delivering a malicious update file instead of the legitimate one.

## 1. Scenario Overview and Initial Requirements

### 1.1 Scenario Overview

This scenario demonstrates how an attacker can impersonate a legitimate OTA update server by compromising a proxy.

The attacker intercepts the vehicle’s request, redirects the OTA traffic to a malicious server, and distributes a tampered firmware update.

### 1.2 Basic Requirements

- **Proxy Environment**: A proxy server under attacker control
- **Tools Used**: Python 3, Flask, local domain redirection (`hosts` file)
- **Simulation Devices**: One attacker machine and one simulated vehicle
- **OTA Security Status**: No TLS, no file integrity checks, and no authentication

## Assumptions

- The attacker has already taken control of the proxy.
- The vehicle requests firmware from a domain-based URL (e.g., `http://ota.com`)
- The OTA server does not enforce certificate validation or digital signatures
- The vehicle blindly installs updates without verifying their origin

# **2. Hands-on Procedure**

## Step 1: Firmware Update Uploaded to OTA Server (Baseline Assumption)

- A valid firmware file is uploaded to the official OTA server by the manufacturer.
- This update is published at a specific URL (e.g., `http://ota.com/ota`) and made publicly available.
- The vehicle or driver is notified (via push message or app) that a new OTA update is ready to install.

## Step 2: Vehicle Makes OTA Request

- The vehicle sends an OTA request to [http://ota.com](http://ota.com/) and resolves the domain name to an IP address.
- The attacker intercepts this resolution and redirects the request to their own server by spoofing the IP.

## Step 3: Attacker Hosts a Fake OTA Server

- The attacker sets up a fake OTA server that imitates the real one and serves a crafted `fake_ota_update.bin`.
- The file appears legitimate in format (e.g., headers, version) but includes malicious code.
- To avoid detection, the attacker may adjust the hash/signature or serve an outdated vulnerable version instead.

## Step 4: Vehicle Downloads Malicious OTA File

- The vehicle downloads the OTA file, assuming it’s genuine
- Without proper integrity checks, the malicious update is accepted and applied to the ECU.
- This allows the attacker to gain remote control or cause disruption to the vehicle.

# **Step-by-Step Simulation**

## **Step 1: Create a Fake OTA Server**

```python
# fake_ota_server.py

from flask import Flask, send_file

app = Flask(__name__)

@app.route("/ota")
def send_fake_file():
    return send_file("fake_ota_update.bin", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

**Explanation**

- A simple Flask server listens on port 8000.
- When /ota is accessed, it returns the fake binary file.
- The .bin file imitates a real OTA update.

![image](https://github.com/user-attachments/assets/adda3f2a-9f58-46a7-8b27-34544d66fa44)


## **Step 2: Simulate the Vehicle's Communication Module**

```python
# vehicle_module.py

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

**Explanation**

- Sends an HTTP GET request to `http://ota.com:8000/ota`.
- If successful, saves the file as `downloaded_ota.bin`.
- Simulates a vehicle blindly trusting the update file.

## **Configuration (for local testing)**

**1. Modify `hosts` file on your machine (Windows only)**

To redirect `ota.com` to your local attacker server:

1. Run Notepad as Administrator
2. Open: `C:\Windows\System32\drivers\etc\hosts`
3. Add the following line:

```python
127.0.0.1 ota.com
```

1. Save and close

![image](https://github.com/user-attachments/assets/a62f4bf1-0204-484b-8964-520d1fc68e54)


### Security Validation Elements

1. **Domain Name Validation**
    
    → Ensure OTA clients verify that the resolved IP truly belongs to the trusted server using DNSSEC or certificate pinning.
    
2. **TLS & Certificate Verification**
    
    → Enforce HTTPS communication and check server certificates to prevent MITM or downgrade attacks.
    
3. **Firmware Signature Verification**
    
    → The vehicle must check the digital signature of firmware before installation.
    
4. **Integrity Check with Cryptographic Hash**
    
    → Validate file integrity with SHA-256 or similar hash algorithms to detect tampering.
    
5. **Update Metadata Verification**
    
    → Compare version, timestamp, and publisher info against trusted values.
