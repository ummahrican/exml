import xml.etree.ElementTree as ET
import logging
import os


def populate_xml_template(xml_template, row_dict):
    xml_content = xml_template
    for key, value in row_dict.items():
        placeholder = f"{{{key}}}"
        if placeholder in xml_content:
            xml_content = xml_content.replace(placeholder, str(value))
        else:
            logging.warning(f"Placeholder {placeholder} not found in XML template")
    return xml_content


def write_xml_file(xml_content, output_file):
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Preserve the namespace in the root tag
    namespace_uri = root.tag.split("}", 1)[0].strip("{")

    # Remove the ns0 prefix from all tags
    root.tag = root.tag.split("}", 1)[1]
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]  # Remove the namespace part

    # Add the namespace declaration back to the root tag
    root.set("xmlns:ns0", namespace_uri)

    # Write the XML tree to a file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def validate_xml_file(output_file):
    try:
        ET.parse(output_file)
        logging.info(f"Successfully validated XML file: {output_file}")
    except ET.ParseError as e:
        logging.error(f"XML syntax error in file {output_file}: {e}")
        os.remove(output_file)  # Remove the invalid XML file
        return False
    return True
