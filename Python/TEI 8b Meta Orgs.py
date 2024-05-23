import csv
import xml.etree.ElementTree as ET

def create_xml_element(tag, text=None, attrib=None):
    elem = ET.Element(tag, attrib if attrib else {})
    if text:
        elem.text = text
    return elem

def convert_csv_to_xml(csv_file_path, xml_file_path):
    # Create the root element and the initial structure
    root = ET.Element('listOrg', {'xml:id': 'TopUrbiOrgs'})

    # Descriptions in multiple languages
    descriptions = {
        'es': "Esta lista contiene las organizaciones y los grupos humanos concretos referenciados en el Diccionario de Alcedo tal como se han identificado por los miembros del proyecto. La lista inicial contiene solo aquellas organizaciones que tienen entrada propia en el diccionario. Luego pueden agregarse también aquellas referenciadas en el texto.",
        'en': "This list contains the organizations and specific human groups referenced in the Alcedo Dictionary as identified by the project members. The initial list includes only those organizations that have their own entry in the dictionary. Later, those referenced in the text may also be added.",
        'fr': "Cette liste contient les organisations et les groupes humains spécifiques référencés dans le Dictionnaire d'Alcedo tels qu'ils ont été identifiés par les membres du projet. La liste initiale contient uniquement les organisations qui ont leur propre entrée dans le dictionnaire. Par la suite, celles référencées dans le texte peuvent également être ajoutées."
    }

    for lang, desc in descriptions.items():
        desc_elem = create_xml_element('desc', desc, {'xml:lang': lang})
        root.append(desc_elem)

    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            try:
                org_elem = create_xml_element('org')
                orgName_attrs = {'xml:id': row['GroupID'], 'type': row['type']}
                orgName_elem = create_xml_element('orgName', None, orgName_attrs)
                
                term_elem = create_xml_element('term', row['featuretype'], {'type': 'organizationtype', 'target': f"#{row['featuretype']}"})
                orgName_elem.append(term_elem)

                org_elem.append(orgName_elem)

                if row['idno_base'] and row['gazetteermatch']:
                    idno_elem = create_xml_element('idno', f"{row['idno_base']}{row['gazetteermatch']}", {'type': 'uri'})
                    org_elem.append(idno_elem)

                location_elem = create_xml_element('location', None, {'resp': row['reviewer']})
                district_elem = create_xml_element('district', row['Province'], {'type': 'container'})
                region_elem = create_xml_element('region', row['Region'], {'type': 'container'})
                note_elem = create_xml_element('note', f"{row['conf_loc_verbal']}.")
                geo_elem = create_xml_element('geo', f"{row['Lat']} {row['Lon']}", {'decls': '#geoWGS'})
                
                location_elem.extend([district_elem, region_elem, note_elem, geo_elem])
                org_elem.append(location_elem)

                linkGrp_elem = create_xml_element('linkGrp', None, {'type': 'corresponding_entries'})
                if row['corresp_entry']:
                    link_elem = create_xml_element('link', None, {'target': f"Alcedo_vol{row['volume']}.xml#{row['corresp_entry']}"})
                    linkGrp_elem.append(link_elem)
                    org_elem.append(linkGrp_elem)

                # Creating note groups
                noteGrp_es_elem = create_xml_element('noteGrp')
                noteGrp_en_elem = create_xml_element('noteGrp')
                noteGrp_fr_elem = create_xml_element('noteGrp')

                notes_es = [
                    ('review', row['review-note-es']),
                    ('categorical', row['category-note-es']),
                    ('imaginary', row['imaginary-note-es']),
                    ('artifact', row['artifact-note-es']),
                    ('historical', row['historical-note-es'])
                ]
                notes_en = [
                    ('review', row['review-note-en']),
                    ('categorical', row['category-note-en']),
                    ('imaginary', row['imaginary-note-en']),
                    ('artifact', row['artifact-note-en']),
                    ('historical', row['historical-note-en'])
                ]
                notes_fr = [
                    ('review', row['review-note-fr']),
                    ('categorical', row['category-note-fr']),
                    ('imaginary', row['imaginary-note-fr']),
                    ('artifact', row['artifact-note-fr']),
                    ('historical', row['historical-note-fr'])
                ]

                for note_type, note_value in notes_es:
                    if note_value:
                        note_elem = create_xml_element('note', note_value, {'xml:lang': 'es', 'type': note_type})
                        noteGrp_es_elem.append(note_elem)

                for note_type, note_value in notes_en:
                    if note_value:
                        note_elem = create_xml_element('note', note_value, {'xml:lang': 'en', 'type': note_type})
                        noteGrp_en_elem.append(note_elem)

                for note_type, note_value in notes_fr:
                    if note_value:
                        note_elem = create_xml_element('note', note_value, {'xml:lang': 'fr', 'type': note_type})
                        noteGrp_fr_elem.append(note_elem)

                org_elem.extend([noteGrp_es_elem, noteGrp_en_elem, noteGrp_fr_elem])
                root.append(org_elem)

            except KeyError as e:
                print(f"KeyError: {e}")
                print(f"Available keys: {list(row.keys())}")
                raise

    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)


# Usage
rootpath = "F:/EHESS/TopUrbiGit/"
csv_file_path = rootpath+'input/Meta_Groups.csv'
xml_file_path = rootpath+'TEI/'+'list_Orgs.xml'
convert_csv_to_xml(csv_file_path, xml_file_path)
