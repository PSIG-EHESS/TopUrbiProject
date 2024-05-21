import os
import csv
import xml.etree.ElementTree as ET
import codecs

def read_csv(csv_file):
    metadata = {}
    with codecs.open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        print("CSV Headers:", headers)  # Debugging line to check headers
        for row in reader:
            entry_id = row['entry_id'].strip().lower()
            cleaned_row = {}
            for key, value in row.items():
                if isinstance(value, list):
                    cleaned_row[key] = [v.strip() for v in value if isinstance(v, str)]
                else:
                    cleaned_row[key] = value.strip() if isinstance(value, str) else ""
            metadata[entry_id] = cleaned_row
    return metadata


# Function to remove namespaces from XML tags
def strip_namespace(element):
    for elem in element.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]

# Function to update XML files
def update_xml(xml_files, metadata, rootpath):
    for xml_file in xml_files:
        xml_path = os.path.join(rootpath, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Get the namespace URI
        namespace_uri = root.tag.split('}')[0] + '}'

        # Remove the namespace prefix from the tags
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]

        entries_found = 0  # Counter for debugging
        for entry in root.findall('.//entry'):
            entries_found += 1
            entry_id = entry.get('{http://www.w3.org/XML/1998/namespace}id')
            if entry_id:
                entry_id = entry_id.strip().lower()
                #print(f"Found entry with xml:id={entry_id}")  # Debugging line
                if entry_id in metadata:
                    #print(f"Updating entry: {entry_id}")  # Debugging line
                    entry_data = metadata[entry_id]
                    corresp_entry = entry_data['corresp_entry']
                    fs = ET.Element('fs')
                    for key, value in entry_data.items():
                        if key != 'entry_id' and key != 'corresp_entry':
                            f = ET.Element('f')
                            f.set('name', key)
                            f.set('fval', value)
                            fs.append(f)
                            #print(f"Added <f> element with name='{key}' and fval='{value}'")  # Debugging line
                    entry.insert(0, fs)  # Insert fs before the first child element of entry
                    #print(f"Added <fs> element at the beginning of entry")  # Debugging line
                    sense = entry.find('sense')
                    if sense is not None:
                        entry.remove(sense)
                        entry.append(sense)  # Move sense to the end of entry
                else:
                    print(f"No matching entry_id for {entry_id} in metadata")  # Debugging line
            else:
                print("Entry does not have xml:id attribute")  # Debugging line
        print(f"Total entries found in {xml_file}: {entries_found}")  # Debugging line

        # Write the updated XML back with the namespace
        ET.register_namespace('', namespace_uri)
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)

        print(f"Written updated XML to {xml_path}")  # Debugging line



# Main function
def main():
    rootpath = "F:/EHESS/TopUrbiGit/TEI/"
    csv_path = "F:/EHESS/TopUrbiGit/input/entry-meta.csv"
    xml_files = ['Alcedo_vol_1.xml', 'Alcedo_vol_2.xml', 'Alcedo_vol_3.xml', 'Alcedo_vol_4.xml', 'Alcedo_vol_5.xml']

    metadata = read_csv(csv_path)
    #print("Metadata keys (entry_id values):", list(metadata.keys()))  # Debugging line
    update_xml(xml_files, metadata, rootpath)

if __name__ == "__main__":
    main()
