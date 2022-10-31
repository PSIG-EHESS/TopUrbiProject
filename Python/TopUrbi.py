import re, csv, os, math
from fuzzywuzzy import fuzz

# -*- coding: utf-8 -*-
Territories_list = ["Provincia","Corregimiento",r"Alcaldía mayor","Territorio",r"Pais",r"Jurisdicción","Partido","Obispado","Arzobispado","Nuevo Reyno","Reyno","Condado","Colonia"]
Landmarks_list = ["Rio","Costa","Isla","Bahía","Ensenada","Punta","Puerto","Cabo","Monte","Islote","Laguna","Lago","Sierra"]
Settlements_list = ["Pueblo","Ciudad","Villa","Capital","Aldea","Fuerte",r"Población"]
Ambiguous_list = ["Puerto",r"Nación","Valle"]
Entrytype_list = ["Pueblo","Rio","None","Isla","Ciudad",r"Nación","Provincia","Punta","Puerto","Villa",r"Bahía","Laguna","Cabo","Monte","Islas","Condado","Fuerte","Ensenada","Valle","Capital","Islote",r"Jurisdicción","Lago","Baxo","Montañas","Partido","Islotes",r"Alcaldía mayor","Brazo","Punta de tierra","Llanura","Isleta","Estrecho","Extremidad","Cordillera","Cerro","Montaña","Sierra","País","Baxos","Canal","Banco","Fortaleza",r"Volcán","Lagunas","Golfo","Territorio","Montes","Salto","Caleta","Mar","Mina",r"Peñasco","Aldea","Angostura","Bancos","Entrada",r"Páramo","Reyno","Pedazo","Sitio","Cayo",r"Farallón","Promontorio","Rios","Sierras","Boca","Colonia","Estero","Parte","Playa",r"Playón","Castillo","Despoblado","Llanuras","Minas","Parage",r"Población","Real de minas","Barra",r"Caño",r"Cantón","Ciénega","Cueva","Desierto","Establecimiento","Fuente","Llano","Paso",r"Peña",r"Peñascos",r"Península","Remolino","Santuario","Abertura","Asiento de minas","Bosque","Cabeza","Cayos","Cerros","Distrito","Estanque","Estrechura","Isletas","Presidio","Pueblos","Ramo","Abra","Altos",r"Archipiélago","Arroyo","Asiento ","Atalaya","Barrio","Brazos","Caida","Camino","Cascada","Casta","Ciudades","Colinas","Confluente","Cordilleras","Costa","Cruz","Curato","Feudo","Lugar","Manantiales",r"Médanos","Mineral","Morro","Mote","Obrage","Pasage",r"Peñas",r"Plantación","Potreros","Puente","Rada","Rancho","Raudal",r"República","Salinas","Selva","Seno","Terreno","Torrente","Vado","Parroquia",r"Reducción"]
Metadataelement_list = ["featuretype","entrytype","gazetteermatch"]

    #"Function used to remove blank new lines within entries"
def clean_text(entry):
    entry = entry.replace("\r\n", "")
    entry = entry.replace("\n", "")
    entry = re.sub('\s{2,}', ' ', entry)
    return entry


def replace_pattern(text):
    for pattern in pattern_list:
        text=re.sub(pattern[0],pattern[1], text)
    return(text)

def find_pattern(text):
    for pattern in pattern_list:
        text=re.find(pattern, text)
    return(text)

def get_entries(doc):
    root = doc.getroot()
    data = []
    for element in root.getiterator(ns+"entry"):
        data.append(element)
        #print(element.attrib['xml:id'])
        for child in element:
            if child == "{http://www.tei-c.org/ns/1.0}fs":
                for cchild in child:
                     data.append(cchild)
                     for ccchild in cchild:
                         data.append(ccchild)
    return data
