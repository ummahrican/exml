from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    redirect,
    url_for,
)
import uuid
import logging
import os
from file_utils import read_excel_file, read_xml_template, ensure_directory_exists
from xml_utils import populate_xml_template, write_xml_file, validate_xml_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "output_xmls"

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def excel_to_xmls(excel_file, xml_template_path, output_dir):
    df = read_excel_file(excel_file)
    if df is None:
        return

    xml_template = read_xml_template(xml_template_path)
    if xml_template is None:
        return

    ensure_directory_exists(output_dir)

    for index, row in df.iterrows():
        try:
            row_dict = row.to_dict()
            xml_content = populate_xml_template(xml_template, row_dict)
            first_value = row.iloc[0]
            output_file = os.path.join(output_dir, f"{first_value}.xml")
            write_xml_file(xml_content, output_file)
            if not validate_xml_file(output_file):
                continue
        except Exception as e:
            logging.error(f"Error processing row {index}: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "excelFile" not in request.files or "xmlTemplate" not in request.files:
        return "No file part"

    excel_file = request.files["excelFile"]
    xml_template = request.files["xmlTemplate"]

    if excel_file.filename == "" or xml_template.filename == "":
        return "No selected file"

    unique_id = str(uuid.uuid4())
    upload_dir = os.path.join(app.config["UPLOAD_FOLDER"], unique_id)
    output_dir = os.path.join(app.config["OUTPUT_FOLDER"], unique_id)

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    excel_path = os.path.join(upload_dir, excel_file.filename)
    xml_template_path = os.path.join(upload_dir, xml_template.filename)

    excel_file.save(excel_path)
    xml_template.save(xml_template_path)

    excel_to_xmls(excel_path, xml_template_path, output_dir)

    return redirect(url_for("download_files", unique_id=unique_id))


@app.route("/download/<unique_id>")
def download_files(unique_id):
    output_dir = os.path.join(app.config["OUTPUT_FOLDER"], unique_id)
    files = os.listdir(output_dir)
    return render_template("download.html", files=files, unique_id=unique_id)


@app.route("/download/<unique_id>/<filename>")
def download_file(unique_id, filename):
    output_dir = os.path.join(app.config["OUTPUT_FOLDER"], unique_id)
    return send_from_directory(output_dir, filename)


if __name__ == "__main__":
    app.run(debug=True)
