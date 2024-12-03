import os
import logging
import re
from lxml import etree
from typing import Dict
from utils.file_utils import read_excel_file, read_xml_template


def populate_xml_template(xml_template: str, row_dict: Dict[str, str]) -> str:
    try:
        return xml_template.format(**row_dict)
    except KeyError as e:
        logging.error(f"Missing key in row data: {e}")
        raise


def write_xml_file(xml_content: str, output_file: str):
    try:
        # Extract the prolog (all <? ... ?> declarations at the top of the XML)
        prolog_pattern = r"^(<\?.*?\?>\s*)+"
        match = re.match(prolog_pattern, xml_content, re.DOTALL)
        prolog = match.group(0) if match else ""

        # Remove the prolog from the XML content for parsing
        xml_content = xml_content[len(prolog) :].strip() if prolog else xml_content

        # Parse the remaining XML content
        root = etree.fromstring(xml_content)

        # Remove the namespace prefix from the root element
        root.tag = etree.QName(root.tag).localname

        # Generate the XML tree as a string
        tree = etree.tostring(root, pretty_print=True, encoding="UTF-8").decode("utf-8")

        # Add the prolog back to the content
        full_content = f"{prolog}{tree}"

        # Write to the file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_content)
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
