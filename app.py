from flask import Flask, request, render_template, send_file, redirect, url_for
import uuid
import os
from pathlib import Path
import logging
from utils.file_utils import ensure_directory_exists
from utils.xml_utils import excel_to_xmls

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "output_xmls"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    excel_file = request.files.get("excelFile")
    xml_template = request.files.get("xmlTemplate")

    if not excel_file or not xml_template:
        return "Please upload both files.", 400

    unique_id = str(uuid.uuid4())
    upload_dir = Path(app.config["UPLOAD_FOLDER"]) / unique_id
    output_dir = Path(app.config["OUTPUT_FOLDER"]) / unique_id

    ensure_directory_exists(upload_dir)
    ensure_directory_exists(output_dir)

    excel_path = upload_dir / excel_file.filename
    xml_template_path = upload_dir / xml_template.filename
    excel_file.save(excel_path)
    xml_template.save(xml_template_path)

    excel_to_xmls(str(excel_path), str(xml_template_path), str(output_dir))

    return redirect(url_for("download_files", unique_id=unique_id))


@app.route("/download/<unique_id>")
def download_files(unique_id):
    output_dir = os.path.join(app.config["OUTPUT_FOLDER"], unique_id)
    files = os.listdir(output_dir)
    return render_template("download.html", files=files, unique_id=unique_id)


@app.route("/download/<unique_id>/<filename>")
def download_file(unique_id, filename):
    output_dir = os.path.join(app.config["OUTPUT_FOLDER"], unique_id)
    return send_file(os.path.join(output_dir, filename))


if __name__ == "__main__":
    app.run(debug=True)
