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
