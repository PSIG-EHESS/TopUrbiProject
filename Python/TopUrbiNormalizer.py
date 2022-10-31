# -*- coding: utf-8 -*-
import re


def normalize_basic(inputstring):
    inputstring=re.sub(r'[\.,;:-]', '', inputstring) # clean punct
    inputstring=re.sub(r'á', 'a', inputstring)
    inputstring=re.sub(r'é', 'e', inputstring)
    inputstring=re.sub(r'í', 'i', inputstring)
    inputstring=re.sub(r'ó', 'o', inputstring)
    inputstring=re.sub(r'ú', 'u', inputstring)
    inputstring=re.sub(r'vv', 'w', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
    inputstring = inputstring.lower()
    return inputstring


def normalize_homophones(inputstring):
    inputstring=re.sub(r'x([aeiouáéíóú])', r'j\1', inputstring)
    inputstring=re.sub(r'X([aeiouáéíóú])', r'J\1', inputstring)
    inputstring=re.sub(r'g([éeií])', r'j\1', inputstring)
    inputstring=re.sub(r'G([éeíi])', r'J\1', inputstring)
    inputstring=re.sub(r'gu', 'hu', inputstring)
    inputstring=re.sub(r'Gu', 'Hu', inputstring)
    inputstring=re.sub(r'v', 'b', inputstring)
    inputstring=re.sub(r'tz', 'z', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
    return inputstring


def normalize_near_homophones(inputstring):
    inputstring=re.sub(r'y', 'i', inputstring)
    inputstring=re.sub(r'tz', 'z', inputstring)
    inputstring=re.sub(r'z', 's', inputstring)
    inputstring=re.sub(r's([éeíi])', r'c\1', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
    inputstring=re.sub(r'Y', 'I', inputstring)
    inputstring=re.sub(r'Tz', 'Z', inputstring)
    inputstring=re.sub(r'Z', 'S', inputstring)
    inputstring=re.sub(r'S([éeíi])', r'C\1', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
    return inputstring

def normalize_soupify(inputstring):
    inputstring=re.sub(r'([^c])h([aeiouáéíóú])([^eaéá])', r'\1\2\3', inputstring) #h átona
    inputstring=re.sub(r'([cC])ua', '\1oa', inputstring)
    inputstring=re.sub(r'ñ', r'n', inputstring)
    inputstring=re.sub(r'Ñ', r'N', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)tan\b', r'\1tlan', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)tla\b', r'\1tlan', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)cinco\b', r'\1cingo', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)zinco\b', r'\1cingo', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
    return inputstring

def delete_stopwords(inputstring):
    inputstring=re.sub(r'\bde\b', r' ', inputstring)
    inputstring=re.sub(r'\bdel\b', r' ', inputstring)
    inputstring=re.sub(r'\bla\b', r' ', inputstring)
    inputstring=re.sub(r'\bel\b', r' ', inputstring)
    inputstring=re.sub(r'\bl[oa]s\b', r' ', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
    
def oneword(inputstring):
    inputstring=re.sub(r'[^A-ZÑa-záéíóúüñç]','', inputstring)
    return inputstring


mytext = 'asdfghjklqwe'


