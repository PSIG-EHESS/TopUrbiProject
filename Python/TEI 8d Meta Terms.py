import csv
import xml.etree.ElementTree as ET

def create_xml_element(tag, text=None, attrib=None):
    elem = ET.Element(tag, attrib if attrib else {})
    if text:
        elem.text = text
    return elem

def convert_csv_to_xml(csv_file_path, xml_file_path):
    # Create the root element and the initial structure
    root = ET.Element('list', {'type': 'index', 'xml:id': 'TopUrbiAmericanisms'})

    # Descriptions in multiple languages
    descriptions = {
        'es': "Esta lista contiene información estructurada sobre los términos del diccionario de americanismos del vol. 5 del diccionario de Alcedo, así como un par de términos en todos los volúmenes que no corresponden a elementos geográficos concretos sino tipos/conceptos.",
        'en': "This list contains structured information about the terms from the dictionary of Americanisms of vol. 5 of the Alcedo dictionary, as well as a couple of terms in all volumes that do not correspond to specific geographical elements but rather types/concepts.",
        'fr': "Cette liste contient des informations structurées sur les termes du dictionnaire des américanismes du volume 5 du dictionnaire d'Alcedo, ainsi que quelques termes dans tous les volumes qui ne correspondent pas à des éléments géographiques spécifiques mais plutôt à des types/concepts."
    }

    for lang, desc in descriptions.items():
        desc_elem = create_xml_element('desc', desc, {'xml:lang': lang})
        root.append(desc_elem)

    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')

        # Print the fieldnames to debug the headers
        print(f"CSV Headers: {reader.fieldnames}")

        for row in reader:
            try:
                # Print the current row to debug
                #print(f"Processing row: {row}")

                item_elem = create_xml_element('item', None, {'xml:id': row['termID']})

                label_elem = create_xml_element('label', row['Nombre'])
                item_elem.append(label_elem)

                fs_elem = create_xml_element('fs')
                f1_elem = create_xml_element('f', None, {'name': 'corresp_entry', 'fVal': f"Alcedo_vol{row['volume']}.xml#{row['corresp_entry']}"})
                f2_elem = create_xml_element('f', None, {'name': 'type', 'fVal': f"#{row['featuretype']}"})
                fs_elem.extend([f1_elem, f2_elem])

                item_elem.append(fs_elem)
                root.append(item_elem)

            except KeyError as e:
                print(f"KeyError: {e}")
                print(f"Available keys: {list(row.keys())}")
                raise

    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)

# Usage
rootpath = "F:/EHESS/TopUrbiGit/"
csv_file_path = rootpath+'input/Meta_Terms.csv'
xml_file_path = rootpath+'TEI/'+'list_Americanisms.xml'
convert_csv_to_xml(csv_file_path, xml_file_path)
