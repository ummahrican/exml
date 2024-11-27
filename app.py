from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    redirect,
    url_for,
)
import pandas as pd
import xml.etree.ElementTree as ET
import os
import logging
import uuid

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "output_xmls"

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def excel_to_xmls(excel_file, xml_template_path, output_dir):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        logging.info(f"Successfully read {len(df)} rows from {excel_file}")
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return

    try:
        # Read the XML template
        with open(xml_template_path, "r") as file:
            xml_template = file.read()
        logging.info(f"Successfully read XML template from {xml_template_path}")
    except Exception as e:
        logging.error(f"Error reading XML template: {e}")
        return

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")

    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        try:
            # Convert the row to a dictionary
            row_dict = row.to_dict()

            # Populate the XML template with the data from the dictionary
            xml_content = xml_template
            for key, value in row_dict.items():
                placeholder = f"{{{key}}}"
                if placeholder in xml_content:
                    xml_content = xml_content.replace(placeholder, str(value))
                else:
                    logging.warning(
                        f"Placeholder {placeholder} not found in XML template for row {index}"
                    )

            # Create the XML tree
            root = ET.fromstring(xml_content)
            tree = ET.ElementTree(root)

            # Write the XML tree to a file
            output_file = os.path.join(output_dir, f"output_{index + 1}.xml")
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            logging.info(f"Successfully wrote XML file: {output_file}")
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

    # Create unique directories for each upload
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
