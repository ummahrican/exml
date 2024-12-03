from utils.xml_utils import populate_xml_template


def test_populate_xml_template():
    template = "<root><name>{name}</name><age>{age}</age></root>"
    row_dict = {"name": "John", "age": 30}
    result = populate_xml_template(template, row_dict)
    assert result == "<root><name>John</name><age>30</age></root>"
