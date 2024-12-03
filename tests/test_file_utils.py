import os
from utils.file_utils import read_excel_file, read_xml_template, ensure_directory_exists
import pandas as pd


# Test if the Excel file is read correctly
def test_read_excel_file():
    excel_path = "tests/test_files/test_excel.xlsx"
    df = read_excel_file(excel_path)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# Test reading an XML template
def test_read_xml_template():
    xml_path = "tests/test_files/test_template.xml"
    template = read_xml_template(xml_path)
    assert template.startswith("<?xml")  # Ensures XML content is returned


# Test if a directory is created when it doesn't exist
def test_ensure_directory_exists():
    test_dir = "tests/test_dir"
    if os.path.exists(test_dir):
        os.rmdir(test_dir)  # Clean up before test
    ensure_directory_exists(test_dir)
    assert os.path.exists(test_dir)
    os.rmdir(test_dir)  # Clean up after test
