import csv, os
import xml.etree.ElementTree as ET

rootpath = "F:/EHESS/TopUrbiGit/"

def load_replacements(csv_file):
    replacements = {}
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:  # Ensure there are at least 2 values in the row
                key_value, norm_value = row[:2]  # Unpack first two values
                replacements[key_value] = norm_value
    return replacements

def strip_namespace(element):
    for elem in element.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]  # Strip namespace
        for key in list(elem.attrib.keys()):
            if '}' in key:
                if not key.startswith('{http://www.w3.org/XML/1998/namespace}'):
                    new_key = key.split('}', 1)[1]
                    elem.attrib[new_key] = elem.attrib.pop(key)
                else:
                    # Normalize xml: attributes to their short form
                    new_key = 'xml:' + key.split('}', 1)[1]
                    elem.attrib[new_key] = elem.attrib.pop(key)

def replace_xml_values(xml_file, replacements, target_tags):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    strip_namespace(root)  # Strip namespaces
    for element in root.iter():
        if element.tag in target_tags:
            for key, value in element.attrib.items():
                if value in replacements:
                    element.set(key, replacements[value])
    return tree

def save_xml(tree, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure directory exists

    # Write XML to a temporary file to adjust newlines and correct the <TEI> tag
    temp_output_file = output_file + ".tmp"
    tree.write(temp_output_file, encoding="utf-8", xml_declaration=True)

    # Read the temporary file and write to the final output file with the desired adjustments
    with open(temp_output_file, 'r', encoding='utf-8') as infile:
        content = infile.read()
        # Replace double newlines with single newlines
        content = content.replace('\r\n\r\n', '\r\n')
        # Correct the <TEI> tag with namespaces
        content = content.replace(
            '<TEI schemaLocation=',
            '<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation='
        )
        # Ensure the XML declaration uses double quotes
        content = content.replace("<?xml version='1.0' encoding='utf-8'?>", '<?xml version="1.0" encoding="utf-8"?>')

    with open(output_file, 'w', encoding='utf-8', newline='\r\n') as outfile:
        outfile.write(content)

    # Remove the temporary file
    os.remove(temp_output_file)

if __name__ == "__main__":
    csv_file = rootpath + "Input/key to norm.csv"
    target_tags = ['district', 'settlement', 'orgName', 'term', 'geogName']

    for i in range(1, 6):
        xml_file = rootpath + "Alcedo/Annotated/vol_" + str(i) + "_annotated_TEId.xml"
        output_file = rootpath + "TEI/Alcedo_vol_" + str(i) + ".xml"

        replacements = load_replacements(csv_file)
        modified_tree = replace_xml_values(xml_file, replacements, target_tags)
        save_xml(modified_tree, output_file)
        print(f"Replacement done for vol_{i}.")
