# -*- coding: utf-8 -*-
import csv, re
from lxml import etree
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

Main_path = "F:\\EHESS\\"
Master_path = "F:\\EHESS\\Workbench\\Alcedo_Working_master\\"
Output_path = "F:\\EHESS\\TopUrbiGit\\Analysis\\"
ns='{http://www.tei-c.org/ns/1.0}'

    #Function used to get content of all entry elements
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

    #Get Entry_IDs
def detection_Entry_ID(entry):
  entry_str = etree.tostring(entry)
  soup = BeautifulSoup(entry_str, "lxml")
  return soup.entry['xml:id']


    #Detect entry text with tags stripped
def detection_Sense(entry):
  node = etree.strip_tags(entry,'*')
  return entry.text

    #Detect Value of structured metadata
def detection_Value(symbol):
  symbol_str = etree.tostring(symbol)
  soup = BeautifulSoup(symbol_str, "lxml")
  return soup.symbol['value']


searchpattern=input("Qué palabra buscas (sólo una palabra)?")
length_before=int(input("Cuántas palabras anteriores?")) or 0
length_after = int(input("Cuántas palabras posteriores?")) or 0
threshold = int(input("Entra valor fuzzy (1-100; default=85).")) or 85
##searchpattern="Colchagua"
##length_before=4
##length_after = 2

def fuzzy_replace(keyword_str, text_str, threshold):
    l = len(keyword_str.split())
    splitted = re.split(r'([A-ZÑa-záéíóúüñç-]+)',text_str) #split, keep linebreaks
    for i in range(len(splitted)-l+1):
        temp = "".join(splitted[i:i+l])
        matchvalue = fuzz.ratio(keyword_str, temp)
        if  matchvalue >= threshold:
            head="".join(splitted[:i-length_before-3])
            before = "".join(splitted[i-length_before-3:i])
            match="".join(splitted[i:i+1])
            after = "".join(splitted[i+1:i+4+length_after])
            tail = "".join(splitted[i+4+length_after:])
            text_str= before + match + after
            splitted = re.split(r'([A-ZÑa-záéíóúüñç-]+)',text_str)
            text_str= text_str.replace(match," §"+match+"§ ")
            text_str= text_str.replace("\r?\n"," ")
            text_str=text_str+" @"+str(matchvalue)+"@ "
            print(text_str)
    return text_str



                
with open(Output_path+"analysis-"+searchpattern+".csv", 'w+', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    writer.writerow(["xml:id","Normname","before","foundpattern","after","matchratio","searchpattern"])                
    for vol in range(1,6):
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(Master_path+"alcedo-"+str(vol)+"-utf8.xml", parser)
        data = get_entries(doc)
        for entry in data:
            if entry.tag==ns+'entry':
                for child in entry:
                    for cchild in child:
                        #print(cchild)
                        if cchild.tag==ns+'f' and cchild.attrib['type']=='entrytype':
                            for ccchild in cchild:
                                entrytype_value=''+detection_Value(ccchild)
                        if cchild.tag==ns+'f' and cchild.attrib['type']=='featuretype':
                            for ccchild in cchild:
                                featuretype_value=''+detection_Value(ccchild)
                        if cchild.tag==ns+'f' and cchild.attrib['type']=='normname':
                            for ccchild in cchild:
                                normname_value=''+detection_Value(ccchild)
                entry_content=detection_Sense(entry)
                entry_content = fuzzy_replace(searchpattern, entry_content, threshold)
                #print(entry_content)
                pattern = re.compile(r'([^§]+?)§([^§]+?)§ ([^@]+?)@([^@]+?)@',re.IGNORECASE)
                results = pattern.findall (entry_content)
                #print(m)
                for item in results:
                    patternresult_row = []
                    #print(item[0])
                    patternresult_row.append(detection_Entry_ID(entry))
                    patternresult_row.append(normname_value)
                    patternresult_row.append(item[0])
                    patternresult_row.append(item[1])
                    patternresult_row.append(item[2])
                    patternresult_row.append(item[3])
                    patternresult_row.append(searchpattern)
                    writer.writerow(patternresult_row)
