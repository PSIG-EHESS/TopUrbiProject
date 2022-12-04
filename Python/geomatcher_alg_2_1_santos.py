# -*- coding: utf-8 -*-
import re, csv
from fuzzywuzzy import fuzz
import pandas as pd

def normalize(inputstring):
    inputstring=re.sub(r'[\.,;:-]', '', str(inputstring)) # clean punct
    inputstring=re.sub(r'á', 'a',  str(inputstring))
    inputstring=re.sub(r'é', 'e',  str(inputstring))
    inputstring=re.sub(r'í', 'i',  str(inputstring))
    inputstring=re.sub(r'ó', 'o',  str(inputstring))
    inputstring=re.sub(r'ú', 'u',  str(inputstring))
    inputstring=re.sub(r'vv', 'w',  str(inputstring))
    inputstring=re.sub(r'  ', ' ',  str(inputstring))
    inputstring = inputstring.lower()
    inputstring=re.sub(r'x([aeiouáéíóú])', r'j\1', inputstring)
    inputstring=re.sub(r'X([aeiouáéíóú])', r'J\1', inputstring)
    inputstring=re.sub(r'g([éeií])', r'j\1', inputstring)
    inputstring=re.sub(r'G([éeíi])', r'J\1', inputstring)
    inputstring=re.sub(r'gu', 'hu', inputstring)
    inputstring=re.sub(r'Gu', 'Hu', inputstring)
    inputstring=re.sub(r'v', 'b', inputstring)
    inputstring=re.sub(r'tz', 'z', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
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
    inputstring=re.sub(r'([^c])h([aeiouáéíóú])([^eaéá])', r'\1\2\3', inputstring) #h átona
    inputstring=re.sub(r'([cC])ua', r'\1oa', inputstring)
    inputstring=re.sub(r'ñ', r'n', inputstring)
    inputstring=re.sub(r'Ñ', r'N', inputstring)
    inputstring=re.sub(r'v', r'u', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)tan\b', r'\1tlan', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)tla\b', r'\1tlan', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)cinco\b', r'\1cingo', inputstring)
    inputstring=re.sub(r'([A-ZÑa-záéíóúüñç-]+)zinco\b', r'\1cingo', inputstring)

    inputstring=re.sub(r'  ', ' ', inputstring)
    return inputstring

def stopwordremove(inputstring):
    inputstring=re.sub(r' de ', ' ', inputstring)
    inputstring=re.sub(r' la ', ' ', inputstring)
    inputstring=re.sub(r' el ', ' ', inputstring)
    inputstring=re.sub(r' del ', ' ', inputstring)
    inputstring=re.sub(r' las ', ' ', inputstring)
    inputstring=re.sub(r' los ', ' ', inputstring)
    inputstring=re.sub(r'Nuestra Señora ', ' ', inputstring)
    inputstring=re.sub(r'  ', ' ', inputstring)
    return inputstring

csvin_path = 'F:\\EHESS\\Workbench\\processing\\Input\\alcedo.csv'
csvmatching_path = 'F:\\EHESS\\Workbench\\processing\\Input\\hgis_gz.csv'
regionlist = ['Luisiana','Guayana','CHA','CHL','GUA','SDO','NGR','VEN','PER','QUI','RPL','Popayan','NES','Maracaibo','Tierra Firme','Nueva Vizcaya','Quivira','Collado','Santa Cruz de la Sierra','Nuevo Reyno de Granada']
#regionlist = []
#regionlist = ['CHL','GUA']



dfA = pd.read_csv(csvin_path, sep=';', dtype={"ID": "string","entry_id": "string","entry_headword": "string","normname_value": "string","entrytype_value": "string","featuretype_value": "string","Province": "string",
                                              "District": "string","Region_Alcedo": "string","matchingregion": "string","Nation": "string","Matchingresource": "string","Match": "string","majortype": "string"})
dfB =  pd.read_csv(csvmatching_path, sep=';', dtype={"gz_id": "string", "label": "string", "nombre": "string", "santo": "string","var1": "string", "var2": "string", "var3": "string", "var4": "string", "nombrehoy": "string", "Tipo": "string", "Partido": "string", "Provincia": "string", "REG": "string", "Pais": "string", "Lat": "string", "Lon":"string", "matched":"string"})

#dfA.set_index(['entry_id'], inplace = True)
#dfB.set_index(['gz_id'], inplace = True)

with open("F:\\EHESS\\Workbench\\processing\\Output\\alcedo_hgis_matches.csv", 'w+', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    writer.writerow(["step","entry_id","gz_id","toponymA","toponymB","typeA","typeB","districtA","districtB","provinceA","provinceB","ratio","Lat","Lon"])
    for region in regionlist:
        for i in range(0,dfA.shape[0]):
            if dfA.loc[i,'matchingregion']==region and dfA.loc[i,'Match'] == "none":
                toponymA = normalize(dfA.loc[i,'normname_value'])
                toponymA2 = normalize(dfA.loc[i,'entry_headword'])
                districtA = normalize(dfA.loc[i,'District'])
                provinceA = normalize(dfA.loc[i,'Province'])
                toponymA = stopwordremove(toponymA)
                toponymA2 = stopwordremove(toponymA2)
                districtA = stopwordremove(districtA)
                provinceA = stopwordremove(provinceA)
                typeA = dfA.loc[i,'featuretype_value']
                idA = dfA.loc[i,'entry_id']
                #print(toponymA)
                for i in range(0,dfB.shape[0]):
                    if dfB.loc[i,'REG']==region and dfB.loc[i,'matched']=="no":
                        #print(dfB.loc[i,'label'])
                        toponymB = normalize(dfB.loc[i,'santo'])
                        districtB = normalize(dfB.loc[i,'Partido'])
                        provinceB = normalize(dfB.loc[i,'Provincia'])
                        toponymB = stopwordremove(toponymB)
                        districtB = stopwordremove(districtB)
                        provinceB = stopwordremove(provinceB)
                        
                        typeB = dfB.loc[i,'Tipo']
                        idB = dfB.loc[i,'gz_id']
                        LatB = normalize(dfB.loc[i,'Lat'])
                        LonB = normalize(dfB.loc[i,'Lon'])
                        toporatio1 = fuzz.ratio(toponymA, toponymB)
                        distdistratio = fuzz.ratio(districtA, districtB)
                        distprovratio = fuzz.ratio(districtA, provinceB)
                        provdistratio = fuzz.ratio(provinceA, districtB)
                        provprovratio = fuzz.ratio(provinceA, provinceB)
                        
                        if toponymA == toponymB and (districtA==provinceB or districtA==districtB or provinceA == districtB):
                            writer.writerow(["Step Ia1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,"100",LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")


                      
                        elif toponymA2 == toponymB and (districtA==provinceB or districtA==districtB or provinceA == districtB):
                            writer.writerow(["Step Ia4",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,"100",LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")

                        elif toponymA == toponymB and (distprovratio >85 or distdistratio > 85 or provdistratio >85):
                            writer.writerow(["Step IIa1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,"100",LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")

                        elif toporatio1 > 85 and (districtA==provinceB or districtA==districtB or provinceA == districtB):
                            writer.writerow(["Step IIIa1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,str(toporatio1),LatB,LonB,str(toporatio1)])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")

                        elif toporatio1 > 85 and (distprovratio >85 or distdistratio > 85 or provdistratio >85):
                            writer.writerow(["Step IVa1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,str(toporatio1),LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")


                        elif toponymA == toponymB and (provinceA == provinceB):
                            writer.writerow(["Step Ib1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,"100",LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")
                            writer.writerow(["Step Ib6",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,"100",LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")

                        elif toponymA == toponymB and (provprovratio > 85):
                            writer.writerow(["Step IIb1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,"100",LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")
                        elif toponymA2 == toponymB and (provprovratio > 85):
                            writer.writerow(["Step IIb4",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,"100",LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")                            

                        elif toporatio1 > 85 and (provinceA == provinceB):
                            writer.writerow(["Step IIIb1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,str(toporatio1),LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")

                  

                        elif toporatio1 > 85 and (provprovratio > 85):
                            writer.writerow(["Step IVb1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,str(toporatio1),LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")


#only matchingregion
                        elif toporatio1 ==100:
                            writer.writerow(["Step RegA1",idA,idB,toponymA,toponymB,typeA,typeB,districtA,districtB,provinceA,provinceB,str(toporatio1),LatB,LonB])
                            print(toponymA+", "+toponymB+" in "+districtB+", "+provinceB+" matched!")

