from lxml import etree
import glob
import os

rootpath = "F:/EHESS/TopUrbiGit/TEI/"

# Define the tags to update
tags_to_update = ['district', 'settlement', 'orgName', 'geogName', 'persName']

# XML namespace for xml:id
xml_ns = "http://www.w3.org/XML/1998/namespace"

# Function to add xml:id attribute
def add_xml_id(element, vol_number, unique_number):
    xml_id = f"annot-{vol_number}-{unique_number}"
    attribs = element.attrib
    if '{http://www.w3.org/XML/1998/namespace}id' not in attribs:
        #print(f"Adding xml:id={xml_id} to <{element.tag}> with current attributes: {attribs}")
        # Set the xml:id attribute using the namespace
        element.set(f"{{{xml_ns}}}id", xml_id)
    else:
        print(f"Element <{element.tag}> already has xml:id, skipping")

# Function to get namespaces
def get_namespaces(xml_file):
    events = "start", "start-ns"
    ns = {}
    for event, elem in etree.iterparse(xml_file, events):
        if event == "start-ns":
            ns[elem[0]] = elem[1]
    return ns

# Loop through volumes 1 to 5
for vol_number in range(3, 6):
    file_pattern = os.path.join(rootpath, f"Alcedo_vol_{vol_number}.xml")
    file_list = glob.glob(file_pattern)
    
    if not file_list:
        print(f"No files found for pattern: {file_pattern}")
        continue
    
    unique_counter = 1

    for file_path in file_list:
        print(f"Processing file: {file_path}")
        
        try:
            namespaces = get_namespaces(file_path)
            tree = etree.parse(file_path)
            root = tree.getroot()
        except etree.XMLSyntaxError as e:
            print(f"Failed to parse {file_path}: {e}")
            continue

        for tag in tags_to_update:
            elements = root.findall(f'.//{{*}}{tag}', namespaces)
            if not elements:
                print(f"No <{tag}> elements found in {file_path}")
            else:
                print(f"Found {len(elements)} <{tag}> elements in {file_path}")
            for element in elements:
                add_xml_id(element, vol_number, unique_counter)
                unique_counter += 1

        # Save the modified XML back to file
        backup_file_path = file_path + '.bak'
        os.rename(file_path, backup_file_path)  # Backup the original file
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"Updated file: {file_path}, backup created: {backup_file_path}")

print("XML files updated successfully.")
