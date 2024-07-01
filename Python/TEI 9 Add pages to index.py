import xml.etree.ElementTree as ET
import csv, re

# List of XML files to process
rootpath = "F:/EHESS/TopUrbiGit/TEI/"
xml_files = ['Alcedo_vol_1.xml', 'Alcedo_vol_2.xml', 'Alcedo_vol_3.xml', 'Alcedo_vol_4.xml', 'Alcedo_vol_5.xml']


# Function to extract namespace from the root element
def get_namespace(element):
    match = re.match(r'\{.*\}', element.tag)
    return match.group(0) if match else ''

# Function to process each XML file and extract the required data
def process_xml_files(xml_files):
    data = []

    for xml_file in xml_files:
        print(f"Processing file: {xml_file}")
        # Parse the XML file with UTF-8 encoding
        tree = ET.parse(rootpath+xml_file, parser=ET.XMLParser(encoding="utf-8"))
        root = tree.getroot()

        namespace = get_namespace(root)
        #print(f"Namespace: {namespace}")
        previous_pb = None

        for elem in root.iter():
            #print(f"Tag: {elem.tag}, Attributes: {elem.attrib}")
            if elem.tag == f'{namespace}pb':
                previous_pb = elem
            elif elem.tag == f'{namespace}entry' and '{http://www.w3.org/XML/1998/namespace}id' in elem.attrib:
                entry_id = elem.attrib['{http://www.w3.org/XML/1998/namespace}id']
                if previous_pb is not None:
                    facs = previous_pb.attrib.get('facs', '')
                    n = previous_pb.attrib.get('n', '')
                    data.append([entry_id, facs, n])
                    #print(f"Added entry: {entry_id}, {facs}, {n}")
    
    return data

# Process the XML files and extract the data
data = process_xml_files(xml_files)

# Write the extracted data to a CSV file with UTF-8 encoding
csv_file = 'output.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ID', 'Facsimile', 'Pagenumber'])
    csvwriter.writerows(data)

print(f"Data has been successfully written to {csv_file}")
