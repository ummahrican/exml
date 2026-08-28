import logging
import os
from zipfile import BadZipFile

import pandas as pd

logger = logging.getLogger(__name__)


def read_excel_file(excel_file):
    try:
        return pd.read_excel(excel_file)
    except (OSError, ValueError, BadZipFile) as e:
        # OSError: missing/unreadable path. ValueError: unrecognised format.
        # BadZipFile: truncated or corrupt .xlsx.
        logger.error(f"Error reading Excel file: {e}")
        return None


def read_xml_template(xml_template_path):
    try:
        with open(xml_template_path, "r") as file:
            return file.read()
    except (OSError, UnicodeDecodeError) as e:
        # OSError: missing/unreadable path. UnicodeDecodeError: not text.
        logger.error(f"Error reading XML template: {e}")
        return None


def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)
