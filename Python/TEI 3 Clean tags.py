import re


replacement_patterns = [
    {
        "search": r' gender="[^"]+?"',
        "replace": r''
    },
    {
        "search": r'<Territory>(.+?)</Territory>',
        "replace": r'<district key="\1"><placeName type="Territory">\1</placeName></district>'
    },
    {
        "search": r'<Settlement>(.+?)</Settlement>',
        "replace": r'<settlement key="\1"><placeName type="Settlement">\1</placeName></settlement>'
    },
    {
        "search": r'<Structure>(.+?)</Structure>',
        "replace": r'<objectName key="\1"><placeName type="Structure">\1</placeName></objectName>'
    },
    {
        "search": r'<Landmark>(.+?)</Landmark>',
        "replace": r'<geogFeat key="\1"><placeName type="Landmark">\1</placeName></geogFeat>'
    },
    {
        "search": r' Compoundterm',
        "replace": r'term'
    },

    {
        "search": r' <PLACE([^>]+?) type="Territory"([^>]+?)>(.+?)</PLACE>',
        "replace": r'<district\1\2>\3</district>'
    },
    {
        "search": r' <PLACE([^>]+? )type="Settlement("[^>]+?>).+?</PLACE>',
        "replace": r'<settlement\1\2>\3</settlement>'
    },
    {
        "search": r' <PLACE([^>]+? )type="Landmark("[^>]+?>).+?</PLACE>',
        "replace": r'<geogFeat\1\2>\3</geogFeat>'
    },
    {
        "search": r' <PLACE([^>]+? )type="Structure("[^>]+?>).+?</PLACE>',
        "replace": r'<objectName\1\2>\3</objectName>'
    },
    
]

for filename in filename_list:
    with open(rootpath+filename+"_TEId.xml", "r", encoding="utf-8") as file:
        # Apply the replacement patterns
        modified_content = original_content
        for pattern in replacement_patterns:
            modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
        original_content = modified_content
