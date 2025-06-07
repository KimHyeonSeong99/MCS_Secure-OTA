import requests
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Server Address
base_url = "https://ota.realserver.com"

# File Download Function
def download_file(filename):
    print(f"[+] Downloading {filename}...")
    r = requests.get(f"{base_url}/{filename}", verify=False)
    with open(filename, 'wb') as f:
        f.write(r.content)
    return r.content

# 1. Download the OTA file
firmware = download_file("firmware.bin")
signature = download_file("firmware.sig")
hash_expected = download_file("firmware.hash").decode().split()[0]

# 2. Verify the hash
hash_actual = hashlib.sha256(firmware).hexdigest()
print(f"[✓] Expected hash: {hash_expected}")
print(f"[✓] Actual hash:   {hash_actual}")

if hash_expected != hash_actual:
    print("[✗] Hash mismatch! Aborting OTA installation.")
    exit()

# 3. Verify the signature using the public key
with open("attacker.pub", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

try:
    public_key.verify(
        signature,
        firmware,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("[✓] Signature is valid. OTA installation complete.")
except Exception as e:
    print("[✗] Signature verification failed:", e)
