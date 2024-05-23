import csv
import xml.etree.ElementTree as ET

def create_xml_element(tag, text=None, attrib=None):
    elem = ET.Element(tag, attrib if attrib else {})
    if text:
        elem.text = text
    return elem

def convert_csv_to_xml(csv_file_path, xml_file_path):
    # Create the root element and the initial structure
    root = ET.Element('list', {'type': 'gloss', 'xml:id': 'TopUrbiConcepts'})

    # Descriptions in multiple languages
    descriptions = {
        'es': "Esta lista contiene conceptos harmonizados para definir términos anotados en los volúmenes del Diccionario, así como metaconceptos que agrupan otros conceptos. Los metaconceptos se distinguen por ser expresados en inglés y no español. La mayoría de las glosas fueron producidas por inteligencia artificial (ChatGPT).",
        'en': "This list contains harmonized concepts to define terms annotated in the volumes of the Dictionary, as well as metaconcepts that group other concepts. The metaconcepts are distinguished by being expressed in English and not in Spanish. The majority of glosses has been produced with AI (ChatGPT).",
        'fr': "Cette liste contient des concepts harmonisés pour définir les termes annotés dans les volumes du Dictionnaire, ainsi que des métaconcepts qui regroupent d'autres concepts. Les métaconcepts se distinguent par le fait qu'ils sont exprimés en anglais et non en espagnol. La majorité des gloses a été produite avec l'IA (ChatGPT)."
    }

    for lang, desc in descriptions.items():
        desc_elem = create_xml_element('desc', desc, {'xml:lang': lang})
        root.append(desc_elem)

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')

        for row in reader:
            item_attrib = {'xml:id': row['Nombre']}
            if row['term_general']:
                item_attrib['corresp'] = f"#{row['term_general']}"

            item_elem = create_xml_element('item', attrib=item_attrib)

            label_elem = create_xml_element('label', row['Nombre'])
            item_elem.append(label_elem)

            for lang in ['es', 'en', 'fr']:
                desc_elem = create_xml_element('item', row[f'Description-{lang}'], {'xml:lang': lang})
                item_elem.append(desc_elem)

            if row['AAT']:
                idno_elem = create_xml_element('idno', f"http://vocab.getty.edu/page/aat/{row['AAT']}", {'type': 'URI'})
                item_elem.append(idno_elem)

            fs_elem = create_xml_element('fs')
            term_group_fields = [
                ('term-group', row['term-group1']),
                ('general-term-group', row['term-group2']),
                ('most-general-term-group', row['term-group3'])
            ]

            for name, value in term_group_fields:
                f_elem = create_xml_element('f', attrib={'name': name, 'fVal': f"#{value}"})
                fs_elem.append(f_elem)

            item_elem.append(fs_elem)
            root.append(item_elem)

    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)

# Usage
rootpath = "F:/EHESS/TopUrbiGit/"
csv_file_path = rootpath+'input/Meta_Concepts.csv'
xml_file_path = rootpath+'TEI/'+'list_Concepts.xml'
convert_csv_to_xml(csv_file_path, xml_file_path)
