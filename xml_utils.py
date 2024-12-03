import xml.etree.ElementTree as ET
import logging
import os
import re
from typing import Dict


def populate_xml_template(xml_template: str, row_dict: Dict[str, str]) -> str:
    """
    Replace placeholders in XML template with values from the row dictionary.

    Args:
        xml_template (str): The XML template string
        row_dict (Dict[str, str]): Dictionary of key-value pairs for replacement

    Returns:
        str: XML template with placeholders replaced
    """
    for key, value in row_dict.items():
        placeholder = f"{{{key}}}"
        if placeholder not in xml_template:
            logging.warning(f"Placeholder {placeholder} not found in XML template")
        xml_template = xml_template.replace(placeholder, str(value))
    return xml_template


def extract_xml_metadata(xml_content: str) -> Dict[str, str]:
    """
    Extract XML metadata including declaration and processing instructions.

    Args:
        xml_content (str): Full XML content

    Returns:
        Dict[str, str]: Dictionary of metadata elements
    """
    metadata = {}

    # Extract XML declaration
    declaration_match = re.search(r"<\?xml.*?\?>", xml_content, re.DOTALL)
    if declaration_match:
        metadata["declaration"] = declaration_match.group(0)

    # Extract all processing instructions
    processing_instructions = re.findall(r"<\?[^>]+\?>", xml_content, re.DOTALL)
    metadata["processing_instructions"] = [
        pi for pi in processing_instructions if pi != metadata.get("declaration")
    ]

    return metadata


def write_xml_file(xml_content: str, output_file: str) -> None:
    """
    Write XML content to a file, preserving metadata and namespaces.

    Args:
        xml_content (str): Full XML content to write
        output_file (str): Path to output XML file
    """
    try:
        # Extract metadata before parsing
        metadata = extract_xml_metadata(xml_content)

        # Parse the XML content
        root = ET.fromstring(xml_content)

        # Determine and handle namespace
        if "}" in root.tag:
            namespace_uri = root.tag.split("}", 1)[0].strip("{")
            root.tag = root.tag.split("}", 1)[1]

            # Remove namespace prefixes from all tags
            for elem in root.iter():
                if "}" in elem.tag:
                    elem.tag = elem.tag.split("}", 1)[1]

            # Restore namespace declaration
            root.set("xmlns:ns0", namespace_uri)

        # Write the file with preserved metadata
        with open(output_file, "wb") as f:
            # Write XML declaration if exists
            if metadata.get("declaration"):
                f.write(metadata["declaration"].encode("utf-8") + b"\n")

            # Write processing instructions
            for pi in metadata.get("processing_instructions", []):
                f.write(pi.encode("utf-8") + b"\n")

            # Write the XML tree
            ET.ElementTree(root).write(f, encoding="utf-8")

    except Exception as e:
        logging.error(f"Error writing XML file {output_file}: {e}")
        raise


def validate_xml_file(output_file: str) -> bool:
    """
    Validate the syntax of an XML file.

    Args:
        output_file (str): Path to the XML file to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        ET.parse(output_file)
        logging.info(f"Successfully validated XML file: {output_file}")
        return True
    except ET.ParseError as e:
        logging.error(f"XML syntax error in file {output_file}: {e}")
        os.remove(output_file)  # Remove the invalid XML file
        return False
