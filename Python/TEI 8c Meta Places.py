import csv
import xml.etree.ElementTree as ET

def create_xml_element(tag, text=None, attrib=None):
    elem = ET.Element(tag, attrib if attrib else {})
    if text:
        elem.text = text
    return elem

def convert_csv_to_xml(csv_file_path, xml_file_path):
    # Create the root element and the initial structure
    root = ET.Element('listPlace', {'xml:id': 'indexPlaces'})

    # Descriptions in multiple languages
    descriptions = {
        'en': "The location of reviewed places (status indicated in note) are established by the project members and does not follow Alcedo if his indications are problematic or mistaken. The location of unreviewed places is usually simply taken from the document, although frequently in normalized form and some supplied or inferred elements.",
        'es': "La ubicación de los lugares revisados (estatus indicado en nota) es establecida por los miembros del proyecto y no sigue a Alcedo si sus indicaciones son problemáticas o erróneas. La ubicación de los lugares no revisados generalmente se toma simplemente del documento, aunque frecuentemente en forma normalizada y con algunos elementos suministrados o inferidos.",
        'fr': "La localisation des lieux révisés (status indiqué dans note) est établie par les membres du projet et ne suit pas Alcedo si ses indications sont problématiques ou erronées. La localisation des lieux non révisés est généralement simplement prise du document, bien que souvent sous une forme normalisée et avec certains éléments fournis ou inférés."
    }

    for lang, desc in descriptions.items():
        desc_elem = create_xml_element('desc', desc, {'xml:lang': lang})
        root.append(desc_elem)

    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            try:
                place_attrs = {'xml:id': row['PlaceID']}
                if row['corresp_Place']:
                    place_attrs['corresp'] = f"#{row['corresp_Place']}"
                
                place_elem = create_xml_element('place', None, place_attrs)
                
                # Determine the tag based on majortype
                majortype = row['majortype']
                if majortype == 'territory':
                    inner_tag = 'district'
                    inner_elem = create_xml_element(inner_tag)
                elif majortype == 'settlement':
                    inner_tag = 'settlement'
                    inner_elem = create_xml_element(inner_tag)
                elif majortype == 'structure':
                    inner_tag = 'geogName'
                    inner_elem = create_xml_element(inner_tag, attrib={'type': 'structure'})
                elif majortype == 'landmark':
                    inner_tag = 'geogName'
                    inner_elem = create_xml_element(inner_tag, attrib={'type': 'landmark'})
                else:
                    raise ValueError(f"Unexpected majortype: {majortype}")

                placeName_elem = create_xml_element('placeName', row['nombre'])
                inner_elem.append(placeName_elem)

                term_elem = create_xml_element('term', row['featuretype'], {'type': 'featuretype', 'target': f"#{row['featuretype']}"})
                inner_elem.append(term_elem)

                if row['idno_base'] and row['gazetteermatch']:
                    idno_elem = create_xml_element('idno', f"{row['idno_base']}{row['gazetteermatch']}", {'type': 'uri'})
                    inner_elem.append(idno_elem)

                location_elem = create_xml_element('location', None, {'resp': row['reviewer']})
                district_elem = create_xml_element('district', row['Province'], {'type': 'container'})
                region_elem = create_xml_element('region', row['Region'], {'type': 'container'})
                note_elem = create_xml_element('note', f"{row['conf_loc_verbal']}.", {'type': 'location_representation'})

                location_elem.extend([district_elem, region_elem, note_elem])
                
                if row['Lat'] and row['Lon']:
                    geo_elem = create_xml_element('geo', f"{row['Lat']} {row['Lon']}", {'decls': '#geoWGS'})
                    location_elem.append(geo_elem)

                inner_elem.append(location_elem)

                linkGrp_elem = create_xml_element('linkGrp', None, {'type': 'corresponding_entries'})
                link_elem = create_xml_element('link', None, {'target': f"Alcedo_vol{row['volume']}.xml#{row['corresp_entry']}"})
                linkGrp_elem.append(link_elem)
                inner_elem.append(linkGrp_elem)

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

                inner_elem.extend([noteGrp_es_elem, noteGrp_en_elem, noteGrp_fr_elem])
                place_elem.append(inner_elem)
                root.append(place_elem)

            except KeyError as e:
                print(f"KeyError: {e}")
                print(f"Available keys: {list(row.keys())}")
                raise

    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)



# Usage
rootpath = "F:/EHESS/TopUrbiGit/"
csv_file_path = rootpath+'input/Meta_Places.csv'
xml_file_path = rootpath+'TEI/'+'list_Places.xml'
convert_csv_to_xml(csv_file_path, xml_file_path)
