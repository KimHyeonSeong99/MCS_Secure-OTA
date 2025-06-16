# Folder Structure

```
reference_code_DNS_Spoofing/
├── ota_client/ #OTA target vehicle
|   ├── certs/
|   |   ├── ota.crt
|   |   └── client.key
|   └── client_simulator.py
├── attacker/   #OTA attacker
|   ├── certs/
|   |   ├── ota.crt
|   |   └── attacker.key
|   ├── fake_app.py
|   ├── attacker.pub
|   ├── firmware.bin
|   ├── firmware.hash
|   ├── firmware.sig
|   └── client_simulator.py
├── server/     #OTA normal update server
|   ├── certs/
|   |   ├── ota.crt
|   |   └── server.key
|   ├── firmware.bin 
|   └── app.py
└── README.md
```
# ota_client

## 1. certs

### 1.1 generate ota.crt
~~~
#generate ota.crt wirte in your linux bash
openssl req -x509 -newkey rsa:2048 -keyout ota.key -out ota.crt -days 365 -nodes
~~~

### 1.2 generate client.key
~~~
#generate ota.crt wirte in your linux bash
openssl genrsa -out client.key 2048
~~~

## 2. client_simulator.py
~~~
import requests
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import os

base_url = "https://ota.realserver.com"

def download_file(filename):
    print(f"[+] Downloading {filename}...")
    try:
        r = requests.get(f"{base_url}/{filename}", verify=False)
        r.raise_for_status() 
        with open(os.path.join(os.path.dirname(__file__), filename), 'wb') as f:
            f.write(r.content)
        return r.content
    except requests.exceptions.RequestException as e:
        print(f"[✗] Download failed for {filename}: {e}")
        exit()

print("\n--- Downloading OTA Files ---")
firmware = download_file("firmware.bin")
signature = download_file("firmware.sig")
hash_expected_content = download_file("firmware.hash")

if hash_expected_content is None:
    print("[✗] Expected hash file could not be downloaded. Aborting.")
    exit()

hash_expected = hash_expected_content.decode().split()[0]


print("\n--- Verifying Hash ---")
hash_actual = hashlib.sha256(firmware).hexdigest()
print(f"[✓] Expected hash: {hash_expected}")
print(f"[✓] Actual hash:   {hash_actual}")

if hash_expected != hash_actual:
    print("[✗] Hash mismatch! Aborting OTA installation.")
    exit()
else:
    print("[✓] Hash match. Firmware integrity confirmed.")

print("\n--- Verifying Signature ---")
public_key_path = os.path.join(os.path.dirname(__file__), "attacker.pub")
if not os.path.exists(public_key_path):
    print(f"[✗] Public key not found at {public_key_path}. Please copy 'attacker.pub' to this directory.")
    exit()

try:
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    public_key.verify(
        signature,
        firmware,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("[✓] Signature is valid. OTA installation complete.")
    print("[!] Malicious OTA update successfully installed due to DNS spoofing and signature trust.")
except Exception as e:
    print("[✗] Signature verification failed:", e)
    print("[!] OTA installation failed due to signature mismatch or other error.")
~~~

# attacker

## 1. certs

### 1.1 generate ota.crt
~~~
#generate ota.crt wirte in your linux bash
openssl req -x509 -newkey rsa:2048 -keyout ota.key -out ota.crt -days 365 -nodes
~~~

### 1.2 generate attacker.key
~~~
#generate ota.crt wirte in your linux bash
openssl genrsa -out attacker.key 2048
~~~

## 2. fake_app.py
~~~
from flask import Flask, send_from_directory
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPDATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'updates'))

@app.route('/')
def index():
    return '<h1>Fake OTA Server - Flask (Attacker Controlled)</h1>'

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPDATE_DIR, filename)

if __name__ == '__main__':
    cert_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'certs', 'ota.crt'))
    key_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'certs', 'ota.key'))

    app.run(host='0.0.0.0', port=443, ssl_context=(cert_path, key_path))
~~~

## 3. generate attacker.pub
~~~
#generate ota.crt wirte in your linux bash
openssl rsa -in attacker.key -pubout -out attacker.pub
~~~

## 4. generate firmware.bin
~~~
#generate ota.crt wirte in your linux bash
echo "Malicious firmware simulation file - This is an attacker-controlled update!" > firmware.bin
~~~

## 5. generate firmware.hash
~~~
#generate ota.crt wirte in your linux bash
sha256sum firmware.bin > firmware.hash
~~~

## 6. generate firmware.sig
~~~
#generate ota.crt wirte in your linux bash
openssl dgst -sha256 -sign attacker.key -out firmware.sig firmware.bin
~~~

## 7. client_simulator.py
~~~
#generate ota.crt wirte in your linux bash
cp ~/flask_ota_lab/ota_client/client_simulator.py ~/flask_ota_lab/attacker/client_simulator.py
cp ~/flask_ota_lab/updates/attacker.pub ~/flask_ota_lab/attacker/
~~~

# server

## 1. certs

### 1.1 generate ota.crt
~~~
#generate ota.crt wirte in your linux bash
openssl req -x509 -newkey rsa:2048 -keyout server.key -out ota.crt -days 365 -nodes
# Common Name (e.g. server FQDN or YOUR name) []: ota.realserver.com
~~~

### 1.2 generate server.key
~~~
#generate ota.crt wirte in your linux bash
openssl genrsa -out server.key 2048
~~~

## 2. generate firmware.bin
~~~
#generate ota.crt wirte in your linux bash
echo "Legitimate firmware update file" > firmware.bin
~~~

## 3. app.py
~~~
from flask import Flask, send_from_directory
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPDATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'server', 'updates')) 

@app.route('/')
def index():
    return '<h1>Real OTA Server - Flask</h1>'

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.path.abspath(os.path.join(BASE_DIR, 'updates')), filename)


if __name__ == '__main__':
    cert_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'certs', 'ota.crt'))
    key_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'certs', 'server.key'))

    app.run(host='0.0.0.0', port=443, ssl_context=(cert_path, key_path))
~~~

