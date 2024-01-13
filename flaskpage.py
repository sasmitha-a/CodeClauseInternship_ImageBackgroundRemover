import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from rembg import remove
from PIL import Image

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=["GET","POST"])
def upload():
    try:
        # Initialize the variables
        output_path_jpg = None
        output_path_webp = None

        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        allowed_extensions = {"png", "jpg", "jpeg", "gif"}
        if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
            return jsonify({"error": "Invalid file type"}), 400

        # Save the uploaded file
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Perform background removal
        input_image = Image.open(file_path)
        output_image = remove(input_image)

        # Convert image to RGB mode
        output_image = output_image.convert("RGB")

        # Save the output image as JPEG
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        # Constructing the correct output file name
        output_filename = f"{os.path.splitext(file.filename)[0]}_output.jpg"
        output_path = os.path.join(output_folder, output_filename)
        output_image.save(output_path, "JPEG")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return render_template("upload.html", input_image_path= file_path, output_path=output_path, os=os)

  

@app.route("/output/<filename>")
def get_output_image(filename):
    return send_from_directory("output", filename)

if __name__ == "__main__":
    app.run(debug=True)
