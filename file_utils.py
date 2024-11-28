import pandas as pd
import logging
import os


def read_excel_file(excel_file):
    try:
        df = pd.read_excel(excel_file)
        logging.info(f"Successfully read {len(df)} rows from {excel_file}")
        return df
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return None


def read_xml_template(xml_template_path):
    try:
        with open(xml_template_path, "r") as file:
            xml_template = file.read()
        logging.info(f"Successfully read XML template from {xml_template_path}")
        return xml_template
    except Exception as e:
        logging.error(f"Error reading XML template: {e}")
        return None


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
