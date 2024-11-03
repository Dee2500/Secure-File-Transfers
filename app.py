from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Generate a key for encryption (in production, store this securely)
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Log the received file details
    print(f"Received file: {file.filename}, size: {len(file.read())} bytes")

    # Reset the file pointer
    file.seek(0)

    # Encrypt the file
    file_data = file.read()
    encrypted_data = cipher.encrypt(file_data)

    # Save the encrypted file
    encrypted_filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename + '.enc')
    with open(encrypted_filename, 'wb') as f:
        f.write(encrypted_data)

    return jsonify({"message": "File uploaded and encrypted successfully!"}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    encrypted_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.enc')

    if not os.path.exists(encrypted_filename):
        return jsonify({"error": "File not found"}), 404

    # Decrypt the file
    with open(encrypted_filename, 'rb') as f:
        encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)

    # Save the decrypted file temporarily for download
    temp_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(temp_filename, 'wb') as f:
        f.write(decrypted_data)

    return jsonify({"message": "Download ready", "filename": filename}), 200

if __name__ == '__main__':
    app.run(debug=True)
