import os
import pytest
from app import app


# Set the test environment for Flask
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["OUTPUT_FOLDER"] = "output_xmls"
    client = app.test_client()
    yield client
    # Cleanup after the test (delete any files created during tests)
    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        for file in os.listdir(app.config["UPLOAD_FOLDER"]):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)
            if os.path.isfile(file_path):
                os.remove(file_path)


# Test if the index route renders correctly
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Upload Excel and XML Template" in response.data


# Test if file upload works
def test_upload(client):
    # Mocking an Excel and XML template file upload
    with (
        open("tests/test_files/test_excel.xlsx", "rb") as excel_file,
        open("tests/test_files/test_template.xml", "rb") as xml_template,
    ):
        response = client.post(
            "/upload",
            data={
                "excelFile": (excel_file, "test_excel.xlsx"),
                "xmlTemplate": (xml_template, "test_template.xml"),
            },
        )
    assert response.status_code == 302  # Redirects to download page
