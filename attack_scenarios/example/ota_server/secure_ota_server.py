from flask import Flask, request, render_template, redirect, url_for, send_file
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion
import os
import zipfile  # 추가된 모듈
import io
import socket  # 추가된 모듈
import json  # 추가된 모듈

app = Flask(__name__, template_folder='templates')  # Correct folder name

# Directory to monitor for OTA files
OTA_DIR = "updates"
app.config['UPLOAD_FOLDER'] = OTA_DIR

# Ensure the OTA directory exists
os.makedirs(OTA_DIR, exist_ok=True)
client = Client(callback_api_version=CallbackAPIVersion.VERSION2)
client.username_pw_set("mose", "3103")


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == '1234':
        # Redirect to the upload page after successful login
        return redirect(url_for('upload_page'))
    else:
        # Reload the login page with an error message
        return render_template('login.html', error="Invalid username or password")

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        if 'firmware' not in request.files:  # Check if the file part is in the request
            return render_template('upload.html', error="No file part in the request")
        file = request.files['firmware']
        if file.filename == '':  # Check if a file was selected
            return render_template('upload.html', error="No selected file")
        try:
            client.connect("203.246.114.61", 12010)
            client.loop_start()
            
            # Dynamically retrieve the server's IP address
            server_ip = f"{socket.gethostbyname(socket.gethostname())}:5000"
            json_data = {"update_file_name": file.filename, "server_ip": server_ip}
            
            # Serialize the JSON data properly
            client.publish("updates", json.dumps(json_data).encode(), qos=2, retain=True)
            print(f"Update notice sent: {json_data}")
            
            client.loop_stop()
            client.disconnect()
            # Save the file to the 'firmwares' directory
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return render_template('login.html', success=f"File '{file.filename}' uploaded successfully")
        except Exception as e:
            return render_template('login.html', error=f"Failed to save file: {str(e)}")

@app.route("/get_update", methods=["GET"])
def get_update():
    update_file_name = request.args.get("update_file_name")  # Fix parameter retrieval

    # Check for missing parameters
    if not update_file_name:
        return "Missing 'update_file_name' parameter", 400

    # Decode URL-encoded filename and sanitize it
    file_path = os.path.join(OTA_DIR, update_file_name)
    zip_path = os.path.join(OTA_DIR, "update_package.zip")

    if not os.path.exists(file_path):
            return "Update file not found", 404
    
    try:
        # Create a ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            zipf.write(file_path, arcname=update_file_name)

        # Send the ZIP file as a response 
        zip_buffer.seek(0)  # 읽기 위치를 처음으로

        return send_file(
            zip_buffer,
            download_name="update_package.zip",
            as_attachment=True,
            mimetype='application/zip'
        )
    except Exception as e:
        return f"Error creating or sending ZIP file: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True, threaded = True)

