from flask import Flask, request, render_template, redirect, url_for, jsonify
import os

app = Flask(__name__, template_folder='templates')  # Correct folder name

# Directory to monitor for OTA files
OTA_DIR = "firmwares"
app.config['UPLOAD_FOLDER'] = OTA_DIR

# Ensure the OTA directory exists
os.makedirs(OTA_DIR, exist_ok=True)

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
            # Save the file to the 'firmwares' directory
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return render_template('upload.html', success=f"File '{file.filename}' uploaded successfully")
        except Exception as e:
            return render_template('upload.html', error=f"Failed to save file: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

