from flask import Flask, render_template, request, send_file, flash
from werkzeug.utils import secure_filename
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

app = Flask(__name__)
app.secret_key = "ciphervaultsecret"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_key(passphrase):
    if len(passphrase) < 4 or len(passphrase) > 10:
        raise ValueError("Password must be 4 to 10 characters long.")
    hashed = hashlib.sha256(passphrase.encode()).digest()
    return hashed[:16]

def encrypt_file(input_path, key, output_path):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(input_path, "rb") as f:
        plaintext = f.read()
    padded = pad(plaintext, AES.block_size)
    ciphertext = cipher.iv + cipher.encrypt(padded)
    with open(output_path, "wb") as f:
        f.write(ciphertext)

def decrypt_file(input_path, key, output_path):
    with open(input_path, "rb") as f:
        ciphertext = f.read()
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    with open(output_path, "wb") as f:
        f.write(plaintext)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        password = request.form.get("password")
        if not password:
            flash("Password is required!", "error")
            return render_template("index.html")
        try:
            key = generate_key(password)
        except ValueError as ve:
            flash(str(ve), "error")
            return render_template("index.html")

        if "file" not in request.files:
            flash("No file selected!", "error")
            return render_template("index.html")
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected!", "error")
            return render_template("index.html")

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if action == "encrypt":
            output_path = filepath + ".enc"
            encrypt_file(filepath, key, output_path)
            return send_file(output_path, as_attachment=True)
        elif action == "decrypt":
            if not filename.lower().endswith(".enc"):
                flash("Please upload a .enc file for decryption!", "error")
                return render_template("index.html")
            output_path = filepath[:-4]  # remove .enc
            decrypt_file(filepath, key, output_path)
            return send_file(output_path, as_attachment=True)

    return render_template("index.html")

# DO NOT add app.run() here → Railway uses gunicorn