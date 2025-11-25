from flask import Flask, render_template, request, send_file, flash
from werkzeug.utils import secure_filename
import os
from crypto_utils import generate_key, encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = "ciphervaultsecret"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if action == "encrypt":
            output_path = filepath + ".enc"
            encrypt_file(filepath, key, output_path)
            return send_file(output_path, as_attachment=True)

        elif action == "decrypt":
            if not filename.endswith(".enc"):
                flash("Please upload a .enc file only!", "error")
                return render_template("index.html")

            output_path = filepath.replace(".enc", "")
            decrypt_file(filepath, key, output_path)
            return send_file(output_path, as_attachment=True)

    return render_template("index.html")

