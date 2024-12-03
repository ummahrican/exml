import os
import logging
from lxml import etree
from typing import Dict
from utils.file_utils import read_excel_file, read_xml_template


def populate_xml_template(xml_template: str, row_dict: Dict[str, str]) -> str:
    for key, value in row_dict.items():
        xml_template = xml_template.replace(f"{{{key}}}", str(value))
    return xml_template


def write_xml_file(xml_content: str, output_file: str):
    try:
        # Parse the XML content
        root = etree.fromstring(xml_content)

        # Remove the namespace prefix from the root element
        root.tag = etree.QName(root.tag).localname

        # Write the XML file, preserving the namespace declaration
        with open(output_file, "wb") as f:
            f.write(
                etree.tostring(
                    root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
                )
            )
    except Exception as e:
        logging.error(f"Error writing XML file {output_file}: {e}")
        raise


def excel_to_xmls(excel_file, xml_template_path, output_dir):
    df = read_excel_file(excel_file)
    xml_template = read_xml_template(xml_template_path)

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        xml_content = populate_xml_template(xml_template, row_dict)
        output_file = os.path.join(output_dir, f"{row.iloc[0]}.xml")
        write_xml_file(xml_content, output_file)
