# fake_ota_server.py

from flask import Flask, send_file

app = Flask(__name__)

@app.route("/ota")
def send_fake_file():
    return send_file("fake_ota_update.bin", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
