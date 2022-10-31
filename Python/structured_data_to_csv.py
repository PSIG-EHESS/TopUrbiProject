# -*- coding: utf-8 -*-
import csv, re
from bs4 import BeautifulSoup
from lxml import html, etree

Output_path = "F:\\EHESS\\TopUrbiGit\\Analysis\\"
Master_path = "F:\\EHESS\\Workbench\\Alcedo_Working_master\\"
ns='{http://www.tei-c.org/ns/1.0}'


parser = etree.XMLParser(remove_blank_text=True)
doc = etree.parse(Master_path+"alcedo-2-utf8.xml", parser)

    #"Function used to remove blank new lines within entries"
def clean_text(entry):
    entry = entry.replace("\r\n", "")
    entry = entry.replace("\n", "")
    entry = re.sub('\s{2,}', ' ', entry)
    return entry

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



###Detect elements###

    #Detect entry text with tags stripped
def detection_Sense(entry):
  node = etree.strip_tags(entry,'*')
  #node = clean_text(node)
  return entry.text

    #Get Entry_ID
def detection_Entry_ID(entry):
  entry_str = etree.tostring(entry)
  soup = BeautifulSoup(entry_str, "lxml")
  return soup.entry['xml:id']

    #Get Top Headword
def detection_Headword(entry):
  entry_str = etree.tostring(entry)
  soup = BeautifulSoup(entry_str, "lxml")
  return soup.entry['n']

    #Detect Value of structured metadata
def detection_Value(symbol):
  symbol_str = etree.tostring(symbol)
  soup = BeautifulSoup(symbol_str, "lxml")
  return soup.symbol['value']


    #Create dictionary from structured data
def entry_dictionary():
    for variable in headrow_list:
        entry_dict[variable] = eval(variable)
    print(entry_dict)


    
#Main script

headrow_list = ["entry_id","entry_headword","normname_value","entrytype_value","featuretype_value","gazetteermatch_value","entry_content"]

with open(Output_path+"/alcedo_structured.csv", 'w+', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    writer.writerow(headrow_list)                
    for vol in range(1,6):
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(Master_path+"alcedo-"+str(vol)+"-utf8.xml", parser)
        data = get_entries(doc)
        for entry in data:
            if entry.tag==ns+'entry':
                gazetteermatch_value=''
                entry_dict ={}
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
                        if cchild.tag==ns+'f' and cchild.attrib['type']=='gazetteermatch':
                            #print("found")
                            for ccchild in cchild:
                                gazetteermatch_value=''+detection_Value(ccchild)
                                #print(gazetteermatch_value)
                entry_id=detection_Entry_ID(entry)
                #print(entry_id)
                entry_headword=detection_Headword(entry)
                entry_content=detection_Sense(entry)
                #entry_dictionary()
                writer.writerow([entry_id,entry_headword,normname_value,entrytype_value,featuretype_value,gazetteermatch_value,entry_content])


