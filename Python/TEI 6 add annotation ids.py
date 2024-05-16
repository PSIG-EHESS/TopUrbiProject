from lxml import etree
import glob
import os

rootpath = "F:/EHESS/TopUrbiGit/TEI/"

# Define the tags to update
tags_to_update = ['district', 'settlement', 'orgName', 'geogName', 'persName']

# Function to add xml:id attribute
def add_xml_id(element, vol_number, unique_number):
    xml_id = f"annot-{vol_number}-{unique_number}"
    # Insert as the first attribute
    attribs = element.attrib
    if 'xml:id' not in attribs:
        # Creating a new ordered dictionary with xml:id as the first attribute
        new_attribs = {'xml:id': xml_id}
        new_attribs.update(attribs)
        element.attrib.clear()
        element.attrib.update(new_attribs)

# Loop through volumes 1 to 5
for vol_number in range(1, 6):
    file_pattern = os.path.join(rootpath, f"Alcedo_vol_{vol_number}.xml")
    file_list = glob.glob(file_pattern)
    
    if not file_list:
        print(f"No files found for pattern: {file_pattern}")
        continue
    
    unique_counter = 1

    for file_path in file_list:
        print(f"Processing file: {file_path}")
        
        tree = etree.parse(file_path)
        root = tree.getroot()

        for tag in tags_to_update:
            elements = root.findall(f'.//{tag}')
            for element in elements:
                add_xml_id(element, vol_number, unique_counter)
                unique_counter += 1

        # Save the modified XML back to file
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"Updated file: {file_path}")

print("XML files updated successfully.")
