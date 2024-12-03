import os
import pandas as pd
import logging


def read_excel_file(excel_file):
    try:
        return pd.read_excel(excel_file)
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return None


def read_xml_template(xml_template_path):
    try:
        with open(xml_template_path, "r") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading XML template: {e}")
        return None


def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)
