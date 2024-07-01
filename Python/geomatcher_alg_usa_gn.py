import re
import csv
from fuzzywuzzy import fuzz
import pandas as pd

def normalize(inputstring):
    inputstring = re.sub(r'[\.,;:-]', '', str(inputstring))  # clean punct
    inputstring = re.sub(r'á', 'a',  str(inputstring))
    inputstring = re.sub(r'é', 'e',  str(inputstring))
    inputstring = re.sub(r'í', 'i',  str(inputstring))
    inputstring = re.sub(r'ó', 'o',  str(inputstring))
    inputstring = re.sub(r'ú', 'u',  str(inputstring))
    inputstring = re.sub(r'vv', 'w',  str(inputstring))
    inputstring = re.sub(r'  ', ' ',  str(inputstring))
    inputstring = inputstring.lower()
    inputstring = re.sub(r'Nuev[oa]', r'New', inputstring)
    inputstring = re.sub(r'  ', ' ', inputstring)
    inputstring = re.sub(r'uu', 'w', inputstring)
    inputstring = re.sub(r'  ', ' ', inputstring)
    inputstring = re.sub(r'Y', 'I', inputstring)
    inputstring = re.sub(r'  ', ' ', inputstring)
    return inputstring

def stopwordremove(inputstring):
    inputstring = re.sub(r' de ', ' ', inputstring)
    inputstring = re.sub(r' la ', ' ', inputstring)
    inputstring = re.sub(r' el ', ' ', inputstring)
    inputstring = re.sub(r' del ', ' ', inputstring)
    inputstring = re.sub(r' las ', ' ', inputstring)
    inputstring = re.sub(r' los ', ' ', inputstring)
    inputstring = re.sub(r'Nuestra Señora ', ' ', inputstring)
    inputstring = re.sub(r'  ', ' ', inputstring)
    return inputstring

csvin_path = 'F:\\EHESS\\Workbench\\processing\\Input\\x_usa.csv'
csvmatching_path = 'F:\\EHESS\\Workbench\\processing\\Input\\ref_usa_gn.csv'
regionlist = ['Carolina', 'Chesapeake', 'Mid Atlantic', 'New England', 'Georgia', 'Middleground']

dfA = pd.read_csv(csvin_path, sep=';', dtype={"entry_id": "string", "Normname": "string", "featuretype": "string", "prov-group": "string", "Province": "string", "District": "string", "Lat": "string", "Lon": "string"})
dfB = pd.read_csv(csvmatching_path, sep=';', dtype={"gn_id": "string", "name": "string", "place": "string", "county": "string", "state": "string", "state_grp": "string"})

# Print column names to check if they are loaded correctly
print("dfA columns:", dfA.columns)
print("dfB columns:", dfB.columns)

with open("F:\\EHESS\\Workbench\\processing\\Output\\alcedo_usa_gn_matches.csv", 'w+', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    writer.writerow(["step", "entry_id", "gz_id", "toponymA", "toponymB", "districtA", "districtB", "provinceA", "provinceB"])

    for region in regionlist:
        print("Processing region "+region)
        for i in range(dfA.shape[0]):
            if (dfA.iloc[i]['prov-group'] == region and pd.notna(dfA.iloc[i]['Normname']) and pd.notna(dfA.iloc[i]['District']) and pd.notna(dfA.iloc[i]['Province'])):
                toponymA = normalize(dfA.iloc[i]['Normname'])
                districtA = normalize(dfA.iloc[i]['District'])
                provinceA = normalize(dfA.iloc[i]['Province'])
                idA = dfA.iloc[i]['entry_id']
                for j in range(dfB.shape[0]):
                    if (pd.notna(dfB.iloc[j]['state_grp']) and pd.notna(dfB.iloc[j]['name']) and pd.notna(dfB.iloc[j]['county']) and pd.notna(dfB.iloc[j]['state'])):
                        if dfB.iloc[j]['state_grp'] == region:
                            toponymB = normalize(dfB.iloc[j]['name'])
                            districtB = normalize(dfB.iloc[j]['county'])
                            provinceB = normalize(dfB.iloc[j]['state'])
                            idB = dfB.iloc[j]['gn_id']
                            toporatio = fuzz.ratio(toponymA, toponymB)
                            districtratio = fuzz.ratio(districtA, districtB)
                            #if districtratio > 85:
                                #print(str(districtratio)+', '+districtA+', '+districtB)
                            if toponymA == toponymB and (districtratio > 85 and provinceA == provinceB):
                                writer.writerow(["Step CountyA1", idA, idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
                            elif toponymA == toponymB and (districtratio > 85):
                                writer.writerow(["Step CountyA2", idA, idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
                            elif toponymA == toponymB and (districtratio <= 85 and provinceA == provinceB):
                                writer.writerow(["Step ProvA", idA,  idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
                            elif toponymA == toponymB and (districtratio <= 85 and provinceA != provinceB):
                                writer.writerow(["Step RegionA", idA, idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
                            elif toporatio > 85 and (districtratio > 85 and provinceA == provinceB):
                                writer.writerow(["Step CountyB1", idA, idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
                            elif toporatio > 85 and (districtratio > 85):
                                writer.writerow(["Step CountyB2", idA, idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
                            elif toporatio > 85 and (districtratio <= 85 and provinceA == provinceB):
                                writer.writerow(["Step ProvB", idA, idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
                            elif toporatio > 85 and (districtratio <= 85 and provinceA != provinceB):
                                writer.writerow(["Step RegionB", idA, idB, toponymA, toponymB, districtA, districtB, provinceA, provinceB])
