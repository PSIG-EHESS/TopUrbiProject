import re
from bs4 import BeautifulSoup

#all Def by ChatGPT 3.5:
def remove_nonprintable(text):
    # Remove non-printable characters using regex
    return re.sub(r'\x01', '', text)
def replace_match(match):
    # Group 1: toponym["1"]
    # Group 2: optional [A-Z][a-z]+
    return '<PLACE subtype="supplied_term" type="{}" key="{}">€placeNameß{}{}€/placeNameß</PLACE>'.format(
        typeq,
        toponym["3"],
        match.group(1),
        match.group(2) if match.group(2) else ''
    )

def count_characters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # Remove XML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove line breaks
        text = text.replace('\n', '')
        return len(text)


rootpath="F:/EHESS/TopUrbiGit/Alcedo/Annotated/"
filename_list = ['vol_1_annotated','vol_2_annotated','vol_3_annotated','vol_4_annotated','vol_5_annotated']
#filename_list = ['vol_1_annotated','vol_2_annotated']
#filename_list = ['vol_3_annotated','vol_4_annotated','vol_5_annotated']
type_list=['Settlement','Structure','Territory','Landmark']
countstrings = ["<Territory", "<Settlement", "<Landmark"]
substring_counts = {substring: 0 for substring in countstrings}


for filename in filename_list:
    with open(rootpath+filename+".xml", "rb") as file:
        original_content = file.read().decode("utf-8")

    # Replacement patterns
    replacement_patterns = [
            #7 Temporarily change <pb/> and <cb/> to ease capturing in later replace patterns.
        {
            "search": r"<([cp]b[^<]+?)/>",
            "replace": r"€\1/ß"
        },
        {
            "search": r'Concept_Group',
            "replace": r'Concept_org'
        },
        # 1 Wrap Compound Concepts of same type ( <Concept_Territory>Provincia</Concept_Territory> y <Concept_Territory>País</Concept_Territory> )
        {
            "search": r'(<Concept_)([^< ]+?)( type="[^"]+?">)([^<]+?)(</Concept_\2>)(,? [yoúe] )\1\2\3([^<]+?)\5',
            "replace": r'<Compoundterm subtype="explicit_term" type="\2" key="@\4 @\7"><term subtype="explicit_term" type="\2" key="\4">\4</term>\6<term subtype="explicit_term" type="\2" key="\7">\7</term></Compoundterm>'
        },
        # 2 Wrap Compound concepts of mixed type ( <Concept_District>distrito</Concept_District> y <Concept_Territory>jurisdicción</Concept_Territory> )
        {
            "search": r'(<Concept_)([^< ]+?)( type="[^"]+?">)([^<]+?)(</Concept_\2>)(,? [yoúe] )<Concept_([^< ]+)[^<]+?>([^<]+?)</Concept_\7>',
            "replace": r'<Compoundterm subtype="explicit_term" type="@\2 @\7" key="@\4 @\8"><term subtype="explicit_term" type="\2" key="\4">\4</term>\6<term subtype="explicit_term" type="\7" key="\8">\8</term></Compoundterm>'
        },
        #3 Remove Compoundterm compounds of Concept_Group  ( <Compoundterm type="Group" key="@Mulatos @Mestizos"><term type="Group" key="Mulatos">Mulatos</term> y <term type="Group" key="Mestizos">Mestizos</term></Compoundterm> )
        {
            "search": r"<Compoundterm type[^<]+?@?Group[^<]+?>([^<]+?)</Compoundterm>",
            "replace": r"\1"
        },
        #3
        {
            "search": r'key="([^"]+?)€[^ß]+?/ß([^"]+?)"',
            "replace": r'key="\1\2"'
        },
        #3
        {
            "search": r'key="([^"]+?)€[^ß]+?/ß([^"]+?)"',
            "replace": r'key="\1\2"'
        },
        #Replace compounds of complex group terms (Nación bárbara y feroz de Indios infieles)
        {
            "search": r'<Compound><Concept_Group>([^<]+?)</Concept_Group>([^<]+?)<Concept_Group>(?P<third>[^<]+?)</Concept_Group>(?P<back>(?P<fourth>([^<]+?)?)<Concept_Group>(?P<fifth>([^<]+?))(</Concept_Group>)?)</Compound>',
            "replace": r'<Compoundterm subtype="explicit_term" type="Group" key="\1\2\g<third>\g<fourth>\g<fifth>"><term subtype="explicit_term" type="Group" key="\1">\1</term>\2<term subtype="explicit_term" type="Group" key="\g<third>">\g<third></term>\g<back></Compoundterm>'
            },
            {
            "search": r'<Compound><Concept_Group>([^<]+?)</Concept_Group>([^<]+?)<Concept_Group>(?P<third>[^<]+?)</Concept_Group>(?P<back></Compound>)',
            "replace": r'<Compoundterm subtype="explicit_term" type="Group" key="\1\2\g<third>"><term subtype="explicit_term" type="Group" key="\1">\1</term>\2<term subtype="explicit_term" type="Group" key="\g<third>">\g<third></term></Compoundterm>'
            },    
        #4 Remove Compoundterm for last pair in enumerations of concepts (</Concept_Landmark>, <Compoundterm type="Landmark" key="@barrancas @montes"><term type="Landmark" key="barrancas">barrancas</term> y <term type="Landmark" key="montes">montes</term></Compoundterm>)
        {
            "search": r"(<Concept_[^<]+?>[^<]+?</Concept_[^<]+?>, )<Compoundterm type[^<]+?>([^<]+?)</Compoundterm>",
            "replace": r"\1"
        },
        #5 Replace non-compound concepts with <term> ( <Concept_Settlement>Pueblo</Concept_Settlement> )
        {
            "search": r'(<Concept_)([^< ]+?)( type="[^"]+?">)([^<]+?)(</Concept_\2>)',
            "replace": r'<term subtype="explicit_term" type="\2" key="\4">\4</term>'
        },
        #Replace breaks that made it into attribute values
        #3
        {
            "search": r'key="([^"]+?)€[^ß]+?/ß([^"]+?)"',
            "replace": r'key="\1\2"'
        },
        #3
        {
            "search": r'key="([^"]+?)€[^ß]+?/ß([^"]+?)"',
            "replace": r'key="\1\2"'
        },
        #6 Wrap toponym-composites with variant toponyms. ( <Territory>Nueva Francia</Territory> o <Territory>Canadá</Territory> ) 
        {
            "search": r"<(?P<p1>((Territory)?(Settlement)?(Landmark)?(Structure)?))>(?P<p2>[^<]+?)<(?P<p3>/\1)>(?P<conn>,? [oú] (?:del? ?l?[oa]?s? )?)<(?P<p5>\1)>(?P<p6>[^<]+?)<(?P<p7>/\1)>",
            "replace": r'<placeName subtype="Compound" type="\g<p1>" key="@\g<p2> @\g<p6>">€placeNameß\g<p2>€/placeNameß\g<conn>€placeNameß\g<p6>€/placeNameß</placeName>'
        },
        #add type territory to isla-territories
        {
            "search": r'type="Landmark" key="([iI]slas?">[iI]slas?)</term> de <placeName type="Territory">([^<]+?)</placeName>',
            "replace": r'type="@Landmark @Territory" key="\1</term> de <placeName type="Territory">\2</placeName>'
        },
        #8 Wrap type-toponym-compounds of coinciding type (Ciudad de Guatemala) ojo
        {
            "search": r'(<)(term subtype="explicit_term" type=\")([^<]+?)(\"[^<]+?>)([^<]+?)(</)(term>)( )(<[^<]+/>)?(del? ?)?(<[^<]+/>)?(l[oa]s? )?(<)\3(>[^<]+?)(</)\3(>)',
            "replace": r"<PLACE>\g<0></PLACE>"
        },
        #9 Wrap type-toponym-compounds in simple compounds (Provincia y Corregimiento de Chancay) ojo
        {
            "search": r'(<)(Compoundterm subtype="explicit_term" type=\")([^<]+?)(\"[^<]+?>)(?:(?!(<Compoundterm)).)*?(</)(Compoundterm>)( )(<[^<]+/>)?(del? ?)?(<[^<]+/>)?(l[oa]s? )?(<)\3(>[^<]+?)(</)\3(>)',
            "replace": r"<PLACE>\g<0></PLACE>"
        },
        #10 Wrap type-toponym-compounds in mixed-compound terms (Pueblo y Curato de Autlan) ojo
        {
            "search": r'(<Compoundterm subtype="explicit_term" type=\"@)([^<]+?)( )(@)([^<]+?)(\"[^<]+?>)(?:(?!(<Compoundterm)).)*?(</)(Compoundterm>)( )(<[^<]+/>)?(del? ?)?(<[^<]+/>)?(l[oa]s? )?(<)\2?\5?(>[^<]+?)(</)\2?\5?(>)',
            "replace": r"<PLACE>\g<0></PLACE>"
        },
        #11 Wrap island-territory compounds (isla de Cuba) ojo
        {
            "search": r'(<term subtype="explicit_term" type=\")([^<]+?)(\"[^<]+?[iI]sla[^<]+?>)([^<]+?)(</term>)( )(<[^<]+/>)?(del? ?)?(<[^<]+/>)?(l[oa]s? )?(<)Territory(>[^<]+?)(</)Territory(>)',
            "replace": r"<PLACE>\g<0></PLACE>"
        },
        # Wrap type-toponym-compounds in simple District-Settlement/Territory cases (Partido de Tarija; Parroquia de James) ojo
        {
            "search": r'(<term subtype="explicit_term" type=\")District(\"[^<]+?>)([^<]+?)(</term>)( )(<[^<]+/>)?(del? ?)?(<[^<]+/>)?(l[oa]s? )?(<)(Territory)?(Settlement)?(>[^<]+?)(</)(Territory)?(Settlement)?(>)',
            "replace": r"<PLACE>\g<0></PLACE>"
        },
        # Wrap type-toponym-compounds in simple compound District-Settlement/Territory cases (distrito y Partido de Tarija; distrito y Parroquia de James) ojo
        {
            "search": r'(<Compoundterm subtype="explicit_term" type=\")District(\"[^<]+?>)(?:(?!(<Compoundterm)).)*?(</)(Compoundterm>)( )(<[^<]+/>)?(del? ?)?(<[^<]+/>)?(l[oa]s? )?(<)(Territory)?(Settlement)?(>[^<]+?)(</)(Territory)?(Settlement)?(>)',
            "replace": r"<PLACE>\g<0></PLACE>"
        },
        # Temporarily change wrapped < > to ease capturing in later replace patterns (v1).
        {
            "search": r"(<)(?P<elem>(Territory)?(Settlement)?(Structure)?(Landmark)?)>(?P<back>[^<]+?)</\2>(?P<back2></placeName>)",
            "replace": r'€placeName type="\g<elem>ß"\g<back>€/placeNameß</placeName>'
        },
        # Temporarily change wrapped < > to ease capturing in later replace patterns (v2).
        {
            "search": r"<placeName>(<)(?P<elem>(Territory)?(Settlement)?(Structure)?(Landmark)?)>(?P<back>[^<]+?)</\2>",
            "replace": r'€placeName type="\g<elem>"ß\g<back>€/placeNameß'
        },
        # Temporarily change wrapped < > to ease capturing in later replace patterns (v3). WTF is this?
        {
            "search": r"(<)(?P<elem>(Territory)?(Settlement)?(Structure)?(Landmark)?)(?P<back>[^<]+?</)\2(?P<back2>></PLACE>)",
            "replace": r'\1placeName type="\g<elem>"\g<back>placeName\g<back2>'
        },
        # Remove <PLACE/> false type-toponym-compounds at beginning of entries
        {
            "search": r"(<sense>)<PLACE>(.+?)</PLACE>",
            "replace": r"\1\2"
        },
        #Replace breaks that made it into attribute values
        #3
        {
            "search": r'key="([^"]+?)€[^ß]+?/ß([^"]+?)"',
            "replace": r'key="\1\2"'
        },
        #3
        {
            "search": r'key="([^"]+?)€[^ß]+?/ß([^"]+?)"',
            "replace": r'key="\1\2"'
        },
    ]




    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"original: {substring}: {count}")

    ################################################################################################
    ###Part compounds
    # Apply the replacement patterns
    modified_content = original_content
    for pattern in replacement_patterns:
        modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
    original_content = modified_content
    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Compounds: {substring}: {count}")


    ################################################################################################
    ###Part enumerations and lists
    replacement_patterns_1a = [
        ##Second pattern group
        #Wrap second item in enumeration of toponyms of same type
        {
            "search": r'(<PLACE>)(<term[^<]*?type=")([^<]+?)(" key=")([^"]+?)(s">)([^<]+?)(</term>)([^<]+?)(<placeName type=")\3(">)(?P<topo1>[^<]+?)(</placeName>)(</PLACE>)(?P<conn2>,? ?y?e? d?e? ?)(<)\3(>)(?P<topo2>[^<]+?)(</)\3(>)',
            "replace": r'<term type="\3" key="\5s">\7</term>\9<PLACE subtype="inferred_term" type="\3" key="\5">€placeName type="\3"ß\g<topo1>€/placeNameß</PLACE>\g<conn2><PLACE subtype="inferred_term" type="\3"key="\5">€placeName type="\3"ß\g<topo2>€/placeNameß</PLACE>µ'
        },
        #Add type and keys to <PLACE>
        {
            "search": r'<PLACE><term type="([^<]+?)"( [^<]*?)key="([^<]+?)">',
            "replace": r'<PLACE type="\1"\2key="\3"><term type="\1" key="\3">'
            },
        #Add type and keys to <PLACE>2
        {
            "search": r'<PLACE><Compoundterm type="([^<]+?)"( [^<]*?)key="([^<]+?)">',
            "replace": r'<PLACE type="\1"\2key="\3"><Compoundterm type="\1" key="\3">'
            },
        #Wrap third item in enumeration of toponyms of same type
        {
            "search": r'<PLACE subtype="inferred_term" type="([^<]+?)" key="([^<]+?)">€placeName type="\1"ß([^<]+?)€/placeNameß</PLACE>µ(,? ?y?e? d?e? ?[^<]{0,7})<\1>([^<]+?)</\1>',
            "replace": r'<PLACE subtype="inferred_term" type="\1" key="\2">€placeName type="\1"ß\3€/placeNameß</PLACE>\4<PLACE subtype="inferred_term" type="\1" key="\2">€placeName type="\1"ß\5€/placeNameß</PLACE>µ\1µ\2µµ'

        },
    ]

    # Apply the replacement patterns
    modified_content = original_content
    for pattern in replacement_patterns_1a:
        modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
    original_content = modified_content
    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Enumerations_ini: {substring}: {count}")
        
    replacement_patterns_1b = [
            # add type to first item in list
        {
            "search": r'(?P<front><list subtype="(?P<subtype>(?!mixed)(?!people)(?!organization)[^"]+?)".+?\r\n.*?)(?P<back>(<item>)(.+?)(</item>\r\n))',
            "replace": r'\g<front>µ\g<subtype>µµ\g<back>'
        },
        # add type to first item after list-head
        {
            "search": r'(?P<front><headx subtype="(?P<subtype>[^"]+?)".+?\r\n.*?)(?P<back>(<item>)(.+?)(</item>\r\n))',
            "replace": r'\g<front>µ\g<subtype>µµ\g<back>'
        },
    ]
    # Apply the replacement patterns
    modified_content = original_content
    for pattern in replacement_patterns_1b:
        modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
    original_content = modified_content

    #First looping interlude 
    for typeq in type_list:
        replacement_patterns2 = [
            # Wrap subsequent items in enumeration of toponyms of the same type - must loop
            {
                "search": r'µ([^<µ]+?)µ([^<µ]+?)µµ(,? ?y?e? d?e? ?[^<]{0,7})<\1>([^<]+?)</\1>',
                "replace": r'\3 <PLACE subtype="inferred_term" type="\1" key="\2">€placeName type="\1"ß\4€/placeNameß</PLACE>µ\1µ\2µµ'
            },
            # Subsequent list items
            {
                "search": r'(?P<front>µ[^µ]+?µµ)(?P<back>(€[^ß]+?ß)?(<item>.*?)</item>\r\n)',
                "replace": r'\g<front>\§\g<back>\g<front>'
            },
            # Subsequent list items
            {
                "search": r'(?P<fore>(µ)(?P<type>[^µ]+?)(µµ\\§))(?P<front>(€[^ß]+?ß)?<item>.*?)<'+typeq+'>(?P<topo>.+?)</'+typeq+'>(?P<back>.*?</item>)',
                "replace": r'\g<front><PLACE subtype="inferred_term" type="'+typeq+'" key="\g<type>">€placeName type="'+typeq+'"ß\g<topo>€/placeNameß</PLACE>\g<back>'
            },
        ]
        while True:
            modified_content = original_content
            for pattern in replacement_patterns2:
                modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)

            if modified_content == original_content:
                break  # No more matches, exit the loop
            original_content = modified_content
    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Lists: {substring}: {count}")


    ################################################################################################
    ###Part minor fixes

        # Define the next replacement patterns
    replacement_patterns3 = [
        #Fix heavily compounded districts: original input "(de la )<Concept_District>distrito</Concept_District> y <Concept_Territory>jurisdicción</Concept_Territory>
        #de la <Concept_Settlement>Ciudad</Concept_Settlement> de <Territory>San Felipe</Territory>"
        {
            "search": r'(<Compoundterm )(type="@[^<]+?)( @[^<]+?"[^<]+?>)([^<]+?</Compoundterm> del? ?l?a? )(<term type="Settlement"[^<]+?>[^<]+?</term>[^<]+?)<Territory>(?P<topo1>[^<]+?)</Territory>',
            "replace": r'<PLACE \2\3\1\2\3\4\5€placeName type="Territory"ß\g<topo1>€/placeNameß</PLACE>'
            },
        #Fix same-type-compounded districts: original input "<Concept_Territory>Provincia</Concept_Territory> y <Concept_Territory>jurisdicción</Concept_Territory> de la
        #<Concept_Settlement>Ciudad</Concept_Settlement> de <Territory>San Felipe</Territory>"
        {
            "search": r'(<Compoundterm )(type="[^@]+?)("[^<]+?>)([^<]+?</Compoundterm> del? ?l?a? )(<term type="Settlement"[^>]+?>[^<]+?</term>[^<]+?)<Territory>(?P<topo1>[^<]+?)</Territory>',
            "replace": r'<PLACE \2\3\1\2\3\4\5€placeName type="Territory"ß\g<topo1>€/placeNameß</PLACE>'
            },
         #Fix lesser compounded districts: original input "(de la )<Concept_Territory>jurisdicción</Concept_Territory> de la <Concept_Settlement>Ciudad</Concept_Settlement> de <Territory>San Felipe</Territory>"
        {
            "search": r'(<term subtype="[^"]+?" type="Territory".*?key=")([^<]+?)(">[^<]+?</term>[^<]+?)(<term type="Settlement"[^<]+?>[^<]+?</term>[^<]+?)<Territory>(?P<topo1>[^<]+?)</Territory>',
            "replace": r'<PLACE subtype="explicit_term" type="Territory" key="\2">\1\2\3\4\5€placeName type="Territory"ß\g<topo1>€/placeNameß</PLACE>'
            },   
        {
            "search": r'µ[^µ<]+?µ[^µ<]+?µµ',
            "replace": r''
            },
        {
            "search": r'µ[^µ<]+?µµ',
            "replace": r''
            },
        {
            "search": r'\\§',
            "replace": r''
            },
        ]

    #Next group of patterns
    modified_content = original_content
    for pattern in replacement_patterns3:
        modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
    original_content = modified_content
    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Minor fixes: {substring}: {count}")

    ##################################################################################################
    #####Part unique toponyms
    toponym_list = [
        {"1": r'Perú', "2": 'Territory', "3": 'Reyno'},
        {"1": r'América', "2": 'Territory', "3": 'Continente'},
        {"1": r'Indias', "2": 'Territory', "3": 'Continente'},
        {"1": r'Carolina', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Georgia', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Europa', "2": 'Territory', "3": 'Continente'},
        {"1": r'España', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Italia', "2": 'Territory', "3": 'País'},
        {"1": r'Virginia', "2": 'Territory', "3": '@Provincia @Colonia'},
        {"1": r'Portugal', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Alemania', "2": 'Territory', "3": 'País'},
        {"1": r'Francia', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Chile', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Inglaterra', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Andalucía', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Vizcaya', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Castilla', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Galicia', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Cataluña', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Aragón', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Brasil', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Canadá', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Acadia', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Florida', "2": 'Territory', "3": 'Provincia'},
        {"1": r'San Juan de los Llanos', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Antioquia', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Chocó', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Florida', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Venezuela', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Nueva Andalucía', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Guayana', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Tierra Firme', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Tierra-Firme', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Tierrafirme', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Bahía de Massachussetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Bahía de Masachussetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Bahía de Massachusetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Bahía de Masachusetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Bahía de Massachussets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Bahía de Masachussets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Bahía de Massachusets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Bahía de Masachusets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Massachussetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Masachussetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Massachusetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Masachusetts', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Massachussets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Masachussets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Massachusets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Masachusets', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Estremadura', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Extremadura', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Rioxa', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Rioja', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Vera-Cruz', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Vera Cruz', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Veracruz', "2": 'Settlement', "3": 'Ciudad'},
        
        {"1": r'Tlascala', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Tlaxcala', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Antilles', "2": 'Landmark', "3": 'Islas'},
        {"1": r'Paraguay', "2": 'Landmark', "3": 'Río'},
        {"1": r'Apurimac', "2": 'Landmark', "3": 'Río'},
        {"1": r'Rimac', "2": 'Landmark', "3": 'Río'},
        {"1": r'Biobio', "2": 'Landmark', "3": 'Río'},
        {"1": r'Atrato', "2": 'Landmark', "3": 'Río'},
        {"1": r'Meta', "2": 'Landmark', "3": 'Río'},
        {"1": r'Apure', "2": 'Landmark', "3": 'Río'},
        {"1": r'Uruguay', "2": 'Landmark', "3": 'Río'},
        {"1": r'Orinoco', "2": 'Landmark', "3": 'Río'},
        {"1": r'Magdalena', "2": 'Landmark', "3": 'Río'},
        {"1": r'Portuguesa', "2": 'Landmark', "3": 'Río'},
        {"1": r'Putumayo', "2": 'Landmark', "3": 'Río'},
        {"1": r'Ohio', "2": 'Landmark', "3": 'Río'},
        {"1": r'Amazonas', "2": 'Landmark', "3": 'Río'},
        {"1": r'Madera', "2": 'Landmark', "3": 'Río'},
        {"1": r'Marañ[oó]n', "2": 'Landmark', "3": 'Río'},
        {"1": r'Pampas', "2": 'Landmark', "3": 'Llanuras'},
        {"1": r'Andes', "2": 'Landmark', "3": 'Cordillera'},
        {"1": r'Lima', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Buenos A[iy]res', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santiago de Chile', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Guatemala', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Maule', "2": 'Landmark', "3": 'Río'},
        {"1": r'Tinguiririca', "2": 'Landmark', "3": 'Río'},
        {"1": r'Caracas', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cuzco', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Charcas', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santa Cruz de la Sierra', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Sta\. Cruz de la Sierra', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cochabamba', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Montevideo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Colonia del Sacramento', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Córdova', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Córdoba', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cordova', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cordoba', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Salta', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Potosí', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Potosi', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Tarija', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Huamanga', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Truxillo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Trujillo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Tarma', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cuenca', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Corrientes', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Rioxa', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Rioja', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Catamarca', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santiago del Estero', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Arica', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Arequipa', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Caxamarca', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Cuenca', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Quito', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Guayaquil', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Popayán', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Popayan', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'San Juan de Pasto', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Tunja', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Honda', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Pamplona', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Mompox', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Mompos', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Mómpox', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Mómpos', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Cartagena', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cartaxena', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Merida', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Mérida', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Maracaibo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Sa?n?ta\.? Marta', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Barinas nueva', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Coro', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Barcelona', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cumaná', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cumana', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Guayana', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Panamá', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Panama', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Portovelo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Portobelo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Veragua', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santo Domingo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Sto\. Domingo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'S\. Domingo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Habana', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Havana', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cuba', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Guatemala', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Comayagua', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Leon', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'León', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cartago', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'San Pablo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Todos Santos', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'río Janeiro', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Fernambuco', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Pernambuco', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Nueva Yorck', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Boston', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Bostón', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Filadelfia', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Baltimore', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Montreal', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Quebec', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Halifax', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Nueva Orleans', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Durango', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Monterrei', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Monterrey', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Monterei', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Monterey', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Sinaloa', "2": 'Settlement', "3": 'Villa'},
        {"1": r'Guadalaxara', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Guadalajara', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Zacatecas', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Guanajuato', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Michoacan', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Michoacán', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Oaxaca', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Antequera', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Puebla', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Puebla de los Angeles', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Guanaxuato', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Acapulco', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'México', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Toluca', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'San Luis Potosí', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'San Luis Potosi', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cholula', "2": 'Settlement', "3": 'Ciudad'},

        {"1": r'Monclova', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Saltillo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cayena', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Madrid', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'París', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Londres', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Roma', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Venecia', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Sevilla', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Manila', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Barcelona', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Toledo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Alcántara', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Alcalá', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Avila', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Segovia', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Burgos', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Salamanca', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cadiz', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Lerida', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Malaga', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Mexico', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santa Fe', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santa Fe de Bogotá', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'nuevo mundo', "2": 'Territory', "3": 'Reyno'},
	{"1": r'nuevo Mundo', "2": 'Territory', "3": 'Reyno'},
        {"1": r'nueva España', "2": 'Territory', "3": 'Reyno'},
        {"1": r'nuevo México', "2": 'Territory', "3": 'Reyno'},
        {"1": r'nuevo Reyno de León', "2": 'Territory', "3": 'Reyno'},
        {"1": r'nuevo Reyno de Granada', "2": 'Territory', "3": 'Reyno'},
        {"1": r'nueva Inglaterra', "2": 'Territory', "3": 'Provincia'},
        {"1": r'nueva Escocia', "2": 'Territory', "3": 'Provincia'},
        {"1": r'nueva Francia', "2": 'Territory', "3": 'Provincia'},
	{"1": r'Queretaro', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Cádiz', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Lérida', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Málaga', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'México', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santa Fé', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Santa Fé de Bogotá', "2": 'Settlement', "3": 'Ciudad'},
	{"1": r'Nuevo Mundo', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Nuevo mundo', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Nueva España', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Nuevo México', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Nuevo Reyno de León', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Nuevo Reyno de Granada', "2": 'Territory', "3": 'Reyno'},
        {"1": r'Nueva Inglaterra', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Nueva Escocia', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Nueva Francia', "2": 'Territory', "3": 'Provincia'},
        {"1": r'Valladolid', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Oviedo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Bilbao', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Coruña', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Valencia', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Zamora', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Granada', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Trinidad de Buenos Aires', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Trinidad de Buenos Ayres', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Zaragoza', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Badajoz', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r'Medina del Campo', "2": 'Settlement', "3": 'Ciudad'},
        {"1": r"Misisipi", "2": "Landmark", "3": "Río"},
        {"1": r"Africa", "2": "Territory", "3": "Continente"},
        {"1": r"Ambato", "2": "Territory", "3": "Provincia"},
        {"1": r"America", "2": "Territory", "3": "Continente"},
        {"1": r"America Septentrional", "2": "Territory", "3": "Continente"},
        {"1": r"Araure", "2": "Territory", "3": "Jurisdicción"},
        {"1": r"Asangaro", "2": "Territory", "3": "Provincia"},
        {"1": r"Asia", "2": "Territory", "3": "Continente"},
        {"1": r"Asturias", "2": "Territory", "3": "Provincia"},
        {"1": r"Bahía de Marañan", "2": "Territory", "3": "Capitanía"},
        {"1": r"Barbada", "2": "Territory", "3": "Isla"},
        {"1": r"Barinas", "2": "Territory", "3": "Provincia"},
        {"1": r"Bridgetown", "2": "Territory", "3": "Partido"},
        {"1": r"Buenos-Ayres", "2": "Territory", "3": "Provincia"},
        {"1": r"Caicos", "2": "Territory", "3": "Islas"},
        {"1": r"California", "2": "Territory", "3": "Provincia"},
        {"1": r"Californias", "2": "Territory", "3": "Provincia"},
        {"1": r"Campeche", "2": "Territory", "3": "Provincia"},
        {"1": r"Canada", "2": "Territory", "3": "Provincia"},
        {"1": r"Castilla la Vieja", "2": "Territory", "3": "Reyno"},
        {"1": r"Caxamarquilla", "2": "Territory", "3": "Provincia"},
        {"1": r"Chachapoyas", "2": "Territory", "3": "Provincia"},
        {"1": r"Chaco", "2": "Territory", "3": "Provincia"},
        {"1": r"Chalco", "2": "Territory", "3": "Provincia"},
        {"1": r"Chancay", "2": "Territory", "3": "Provincia"},
        {"1": r"Chiapa", "2": "Territory", "3": "Provincia"},
        {"1": r"Chiloé", "2": "Territory", "3": "Provincia"},
        {"1": r"Chimbo", "2": "Territory", "3": "Provincia"},
        {"1": r"China", "2": "Territory", "3": "País"},
        {"1": r"Cinaloa", "2": "Territory", "3": "Provincia"},
        {"1": r"Concepción", "2": "Territory", "3": "Obispado"},
        {"1": r"Conchucos", "2": "Territory", "3": "Provincia"},
        {"1": r"Connecticut", "2": "Territory", "3": "Colonia"},
        {"1": r"Coquimbo", "2": "Territory", "3": "Provincia"},
        {"1": r"Darién", "2": "Territory", "3": "Provincia"},
        {"1": r"Dominica", "2": "Territory", "3": "Isla"},
        {"1": r"Dorado", "2": "Territory", "3": "Región"},
        {"1": r"Esmeraldas", "2": "Territory", "3": "Provincia"},
        {"1": r"estados unidos", "2": "Territory", "3": "País"},
        {"1": r"Estados Unidos de América", "2": "Territory", "3": "Provincia"},
        {"1": r"Estados unidos de la América", "2": "Territory", "3": "País"},
        {"1": r"Filipinas", "2": "Territory", "3": "Islas"},
        {"1": r"Flandes", "2": "Territory", "3": "Provincia"},
        {"1": r"Fuego", "2": "Territory", "3": "Isla"},
        {"1": r"gran Bretaña", "2": "Territory", "3": "País"},
        {"1": r"gran tierra", "2": "Territory", "3": "Partido"},
        {"1": r"Guadalabquen", "2": "Territory", "3": "Partido"},
        {"1": r"Guadalupe", "2": "Territory", "3": "Isla"},
        {"1": r"Guamanga", "2": "Territory", "3": "Provincia"},
        {"1": r"Guinea", "2": "Territory", "3": "Región"},
        {"1": r"Guipúzcoa", "2": "Territory", "3": "Provincia"},
        {"1": r"Holanda", "2": "Territory", "3": "País"},
        {"1": r"Honduras", "2": "Territory", "3": "Provincia"},
        {"1": r"Ibarra", "2": "Territory", "3": "Provincia"},
        {"1": r"Ilheos", "2": "Territory", "3": "Capitanía"},
        {"1": r"Imperio Mexicano", "2": "Territory", "3": "Imperio"},
        {"1": r"India", "2": "Territory", "3": "Región"},
        {"1": r"India Oriental", "2": "Territory", "3": "Región"},
        {"1": r"Isla de la Laxa", "2": "Territory", "3": "Provincia"},
        {"1": r"Jamayca", "2": "Territory", "3": "Isla"},
        {"1": r"Jersey Occidental", "2": "Territory", "3": "Provincia"},
        {"1": r"Jujui", "2": "Territory", "3": "Jurisdicción"},
        {"1": r"Labrador", "2": "Territory", "3": "Provincia"},
        {"1": r"Leiba", "2": "Territory", "3": "Provincia"},
        {"1": r"Loxa", "2": "Territory", "3": "Provincia"},
        {"1": r"Luisiana", "2": "Territory", "3": "Provincia"},
        {"1": r"Mainas", "2": "Territory", "3": "Provincia"},
        {"1": r"Mancha", "2": "Territory", "3": "Provincia"},
        {"1": r"Marañan", "2": "Territory", "3": "Capitanía"},
        {"1": r"Margarita", "2": "Territory", "3": "Isla"},
        {"1": r"Mariquita", "2": "Territory", "3": "Provincia"},
        {"1": r"Martinica", "2": "Territory", "3": "Isla"},
        {"1": r"Maryland", "2": "Territory", "3": "Colonia"},
        {"1": r"Mechoacán", "2": "Territory", "3": "Provincia"},
        {"1": r"Muzo", "2": "Territory", "3": "Provincia"},
        {"1": r"Navarra", "2": "Territory", "3": "Reyno"},
        {"1": r"Nicaragua", "2": "Territory", "3": "Provincia"},
        {"1": r"Nueva Galicia", "2": "Territory", "3": "Reyno"},
        {"1": r"Nueva Jersey", "2": "Territory", "3": "Colonia"},
        {"1": r"Nueva Vizcaya", "2": "Territory", "3": "Reyno"},
        {"1": r"nueva York", "2": "Territory", "3": "Colonia"},
        {"1": r"Nuevo Reyno", "2": "Territory", "3": "Reyno"},
        {"1": r"Oruro", "2": "Territory", "3": "Provincia"},
        {"1": r"Palma", "2": "Territory", "3": "Jurisdicción"},
        {"1": r"Pará", "2": "Territory", "3": "Capitanía"},
        {"1": r"Paria", "2": "Territory", "3": "Provincia"},
        {"1": r"Pasto", "2": "Territory", "3": "Provincia"},
        {"1": r"Pedraza", "2": "Territory", "3": "Jurisdicción"},
        {"1": r"Pensilvania", "2": "Territory", "3": "Colonia"},
        {"1": r"Piritu", "2": "Territory", "3": "Provincia"},
        {"1": r"Piritú", "2": "Territory", "3": "Provincia"},
        {"1": r"Piura", "2": "Territory", "3": "Provincia"},
        {"1": r"Puerto Rico", "2": "Territory", "3": "Isla"},
        {"1": r"Puerto Seguro", "2": "Territory", "3": "Capitanía"},
        {"1": r"Puertorico", "2": "Territory", "3": "Isla"},
        {"1": r"Puerto-rico", "2": "Territory", "3": "Isla"},
        {"1": r"Rey", "2": "Territory", "3": "Condado"},
        {"1": r"río Jeneyro", "2": "Territory", "3": "Capitanía"},
        {"1": r"Riobamba", "2": "Territory", "3": "Provincia"},
        {"1": r"Sagadahoc", "2": "Territory", "3": "Colonia"},
        {"1": r"San Christóval", "2": "Territory", "3": "Isla"},
        {"1": r"San Gil", "2": "Territory", "3": "Jurisdicción"},
        {"1": r"San Salvador", "2": "Territory", "3": "Provincia"},
        {"1": r"Santa Cruz de la Sierra", "2": "Territory", "3": "Provincia"},
        {"1": r"Santiago de las Atalayas", "2": "Territory", "3": "Jurisdicción"},
        {"1": r"Sinú", "2": "Territory", "3": "Partido"},
        {"1": r"Sonora", "2": "Territory", "3": "Provincia"},
        {"1": r"Surinam", "2": "Territory", "3": "Colonia"},
        {"1": r"Terranova", "2": "Territory", "3": "Isla"},
        {"1": r"Tocaima", "2": "Territory", "3": "Provincia"},
        {"1": r"Topia", "2": "Territory", "3": "Provincia"},
        {"1": r"Trinidad", "2": "Territory", "3": "Isla"},
        {"1": r"Valles", "2": "Territory", "3": "Provincia"},
        {"1": r"Vírgenes", "2": "Territory", "3": "Islas"},
        {"1": r'Paraná', "2": 'Landmark', "3": 'Río'}
    ]

    # Supply type and key for unique Toponym
    for typeq in type_list:
        for toponym in toponym_list:
            if typeq == str(toponym["2"]):
                modified_content = re.sub(
                    r'<{}>({})(\s?[A-Z][a-z]+)?</{}>'.format(typeq, re.escape(toponym["1"]), typeq),
                    replace_match,
                    modified_content
                )
                original_content = modified_content

            # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Unique Topo: {substring}: {count}")

    ################################################################################################
    ###Part role-based definition
    role_list=[
        {"1": r'[gG]obernador',
        "2": r'Gobierno'},
        {"1": r'[Oo]bispo',
        "2": r'Obispado'},
        {"1": r'Iglesia',
        "2": r'Obispado'},
        {"1": r'[Aa]rzobispo',
         "2": r'Obispado'},
        {"1": r'[mM]itra',
        "2": r'Obispado'},
        {"1": r'[oO]idor',
        "2": r'Audiencia'},
        {"1": r'Presidente',
        "2": r'Audiencia'},
        {"1": r'Presidencia',
        "2": r'Audiencia'},
        {"1": r'[aA]lcalde [mM]ayor',
        "2": r'Alcaldía Mayor'},
        {"1": r'[cC]orregidor',
        "2": r'Corregimiento'},
        {"1": r'Zoque',
        "2": r'Reyno'},
        {"1": r'Zipa',
        "2": r'Reyno'},
        {"1": r'[vV]irr?ey',
        "2": r'Reyno'},
        {"1": r'Reyn?a?',
        "2": r'Reyno'},
        {"1": r'[eE]mperador',
        "2": r'Imperio'},
    ]
    ##Wrap cases where the territory-type is defined by a preceding role (Gobernador, Rey...)
    for role in role_list:
        modified_content = original_content
        modified_content = re.sub('(?P<b1>'+str(role["1"])+')' +'(?P<b2> del? ?l?a? )<Territory>'+'(?P<b3>[^<]+?)'+'</Territory>','\g<b1>\g<b2><PLACE subtype="supplied_term" type="Territory" key="'+str(role["2"])+'">€placeNameß\g<b3>€/placeNameß</PLACE>', modified_content)
        original_content = modified_content
    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Role defined: {substring}: {count}")



    ################################################################################################
    ###Part minor fixes 2
    # Define the next replacement patterns
    replacement_patterns4 = [
        #key masculin feminin plural
        {
            "search": r'key="([^"]+?[^as])(s?)">',
            "replace": r'gender="m\2" key="\1\2">'
        },
        {
            "search": r'key="([^"]+?a)(s?)">',
            "replace": r'gender="f\2" key="\1\2">'
        },
        {
            "search": r'(gender=")ms" (?P<cap>key="([Nn]aciones)?([cC]iudades)?([Pp]oblaciones)?([jJ]urisdicciones)?(Capitales)?(Extremidades)?(Alcaldías [Mm]ayores)?">)',
            "replace": r'gender="fs" \g<cap>'
        },
        {
            "search": r'(gender=")m" (?P<cap>key="([Nn]ación)?([cC]iudad)?([Pp]oblación)?([jJ]urisdicción)?(Capital)?(Extremidad)?(Alcaldía [Mm]ayor)?">)',
            "replace": r'gender="f" \g<cap>'
        },
        {
            "search": r'µ.*?µµ.*?</list>',
            "replace": r'</list>'
        },
        {
            "search": r'µ.*?µµ\\§<item>',
            "replace": r'<item>'
        },
        {
            "search": r'</PLACE>µ',
            "replace": r'</PLACE>'
        },
        ]
    #Next group of patterns
    modified_content = original_content
    for pattern in replacement_patterns4:
        modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
    original_content = modified_content

    #Supply type and key in enumerations following PLACE
    for typeq in type_list:
        while True:
            modified_content = original_content
            modified_content = re.sub(r'(?P<front><PLACE[^>]*?key="(?P<key>([^>]+?))"([^>]+?)>([^>]+?)</PLACE>)(?P<conn>(,? y? ?(?:del? ?l[oa]s? )?)(<'+typeq+'>))(?P<topo>[^>]+?)</'+typeq+'>',
                                      r'\g<front>\g<conn><PLACE subtype="inferred_term" type="'+typeq+'" key="\g<key>">€placeNameß\g<topo>€/placeNameß</PLACE>', modified_content)
            if modified_content == original_content:
                break  # No more matches, exit the loop
            original_content = modified_content


    ################################################################################################
    ###Part relative connected types
    connector_list_f = ['con las? de', 'en las? de', 'es las? de', 'son las? de', 'como las? de', 'de las? de', 'y las? de', 'entre las de', 'a la de']
    connector_list_m = ['con el de', 'es el de', 'y el de', 'son el de', 'en el de', 'del de', 'al de','como el de', 'con los de', 'y los de', 'en los de', 'es los de', 'son los de', 'de los de', 'como los de', 'entre los de']

    # Resolve relative mentions (de la de; al de; con la de...)
    for typeq in type_list:
        for connector in connector_list_f:
            while True:
                modified_content = original_content
                modified_content = re.sub('(?P<front>subtype="([^"]+?)" type="'+typeq+'" gender="fs?" key="(?P<key>[^"]+?)"(?:(?!(type="'+typeq+'" gender="fs?")).)*?'+connector+'( l?[oa]?s? ?))<'+typeq+'>(?P<topo>[^<]+?)</'+typeq+'>',
                                          '\g<front><PLACE subtype="inferred_term" type="'+typeq+'" gender="f" key="\g<key>">€placeNameß\g<topo>€/placeNameß</PLACE>', modified_content)
                if modified_content == original_content:
                    break  # No more matches, exit the loop
                original_content = modified_content
    # Resolve relative mentions (de la de; al de; con la de...)
        for connector in connector_list_m:
            while True:
                modified_content = original_content
                modified_content = re.sub('(?P<front>subtype="([^"]+?)" type="'+typeq+'" gender="ms?" key="(?P<key>[^"]+?)"(?:(?!(type="'+typeq+'" gender="ms?")).)*?,? ?'+connector+'( l?[oa]?s? ?))<'+typeq+'>(?P<topo>[^<]+?)</'+typeq+'>',
                                          '\g<front><PLACE subtype="inferred_term" type="'+typeq+'" gender="m" key="\g<key>">€placeNameß\g<topo>€/placeNameß</PLACE>', modified_content)
                if modified_content == original_content:
                    break  # No more matches, exit the loop
                original_content = modified_content
    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Relative mentions ini: {substring}: {count}")


    ################################################################################################
    ###Part relative connected enumerations
    replacement_patterns5 = [
        #Wrap second item in enumeration of toponyms of same type (after relative type resolution)
        {"search": r'(<PLACE>)(<term[^<]*? type=")([^<]+?)(" gender="[^"]*?" key=")([^"]+?)(s?">[^<]+?</term>[^<]+?[€<]placeName type="\3"[ß>][^<]+?[€<]/placeName[ß>]</PLACE>)([^<>]{0,12}?y?e? d?e? ?[^<]{0,7}?)<\3>([^<]+?)</\3>',
         "replace": r'\1\2\3\4\5\6\7<PLACE subtype="inferred_term" type="\3" gender="x" key="\5">€placeName type="\3"ß\8€/placeNameß</PLACE>µ'},
        #Wrap third item in enumeration of toponyms of same type (after relative type resolution)
        {"search": r'<PLACE subtype="[^"]+?" type="([^<]+?)" gender="[^"]*?" key="([^<]+?)">€placeName type="\1"ß([^<]+?)€/placeNameß</PLACE>µ([^<>]{0,12}?y?e? d?e? ?[^<]{0,7}?)<\1>([^<]+?)</\1>',
         "replace": r'<PLACE subtype="inferred_term" type="\1" gender="x" key="\2">€placeName type="\1"ß\3€/placeNameß</PLACE>\4<PLACE subtype="inferred_term" type="\1" key="\2">€placeName type="\1"ß\5€/placeNameß</PLACE>µ\1µ\2µµ'},
        ]
    #Next group of patterns
    modified_content = original_content
    for pattern in replacement_patterns5:
        modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
    original_content = modified_content

    #Second looping interlude
    for typeq in type_list:
        replacement_patterns6 = [
            # Wrap subsequent items in enumeration of toponyms of the same type (after relative type resolution) - must loop
            {"search": r'µ([^<µ]+?)µ([^<µ]+?)µµ(,? ?y?e? d?e? ?[^<]{0,7})<\1>([^<]+?)</\1>',
             "replace": r'\3<PLACE subtype="inferred_term" type="\1" key="\2" gender="x">€placeName type="\1"ß\4€/placeNameß</PLACE>µ\1µ\2µµ'}]
        while True:
            modified_content = original_content
            for pattern in replacement_patterns6:
                modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)

            if modified_content == original_content:
                break  # No more matches, exit the loop
            original_content = modified_content
    # Search for each substring and count its
    for substring in countstrings:
        substring_counts[substring] = len(re.findall(re.escape(substring), original_content))
    # Print the counts
    for substring, count in substring_counts.items():
        print(f"Relative enumerations:{substring}: {count}")

    ################################################################################################
    ###Part minor fixes 3
    # Define the next replacement patterns
    replacement_patterns7 = [

        {
            "search": r'µ[^µ\n]+?µ[^µ\n]+?µµ',
            "replace": r''
        },
        {
            "search": r'€',
            "replace": r'<'
        },
        {
            "search": r'ß',
            "replace": r'>'
        },
        {
            "search": r'µ',
            "replace": r''
        },
        {
            "search": r'<PLACE(><Compoundterm)([^>]+?)(>)',
            "replace": r'<PLACE\2\1\2\3'
        },
        {
            "search": r'<PLACE(><term)([^>]+?)(>)',
            "replace": r'<PLACE\2\1\2\3'
        },
        {
            "search": r'(<PLACE[^>]*? type=")([^"]+?)("[^>]*?)><placeName>',
            "replace": r'\1\2\3><placeName type="\2">'
        },        
        {
            "search": r'term subtype="explicit_term"',
            "replace": r'term'
        },
        {
            "search": r'<Territory>(?P<topo>(?:(?!(<Territory>)).)*?)</Territory>',
            "replace": r'<district subtype="unresolved_term"><placeName>\g<topo></placeName></district>'
        },
        {
            "search": r'<Settlement>(?P<topo>(?:(?!(<Settlement)).)*?)</Settlement>',
            "replace": r'<settlement subtype="unresolved_term"><placeName>\g<topo></placeName></settlement>'
        },
        {
            "search": r'<Structure>(?P<topo>(?:(?!(<Structure)).)*?)</Structure>',
            "replace": r'<objectName subtype="unresolved_term"><placeName>\g<topo></placeName></objectName>'
        },
        {
            "search": r'<Landmark>(?P<topo>(?:(?!(<Landmark)).)*?)</Landmark>',
            "replace": r'<geogName subtype="unresolved_term"><placeName>\g<topo></placeName></geogName>'
        },
        {
            "search": r'Compoundterm',
            "replace": r'term'
        },
        {
            "search": r' ?gender="[^"]+?"',
            "replace": r''
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="Territory" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2">\g<topo></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="Settlement" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<settlement subtype="\1" type="\2">\g<topo></settlement>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="Landmark" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<geogName subtype="\1" type="\2">\g<topo></geogName>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="Structure" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<objectName subtype="\1" type="\2">\g<topo></objectName>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="District" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2">\g<topo></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Settlement @Territory" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2"><settlement subtype="\1">\g<topo></settlement></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Territory @Settlement" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2"><settlement subtype="\1">\g<topo></settlement></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Settlement @Structure" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<settlement subtype="\1" type="\2"><objectName subtype="\1">\g<topo></objectName></settlement>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Structure @Settlement" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<settlement subtype="\1" type="\2"><objectName subtype="\1">\g<topo></objectName></settlement>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Landmark @Territory" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2"><geogName subtype="\1">\g<topo></geogName></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Territory @Landmark" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2"><geogName subtype="\1">\g<topo></geogName></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@District @Territory" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2">\g<topo></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Territory @District" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2">\g<topo></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@District @Settlement" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2"><settlement subtype="\1">\g<topo></settlement></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Settlement @District" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<district subtype="\1" type="\2"><settlement subtype="\1">\g<topo></settlement></district>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Structure @Landmark" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<geogName subtype="\1" type="\2"><objectName subtype="\1">\g<topo></objectName></geogName>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Landmark @Structure" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<geogName subtype="\1" type="\2"><objectName subtype="\1">\g<topo></objectName></geogName>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Settlement @Landmark" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<settlement subtype="\1" type="\2"><geogName subtype="\1">\g<topo></geogName></settlement>'
        },
        {
            "search": r'<PLACE subtype="([^"]+?)" type="@Landmark @Settlement" key="([^"]+?)">(?P<topo>(?:(?!(<PLACE)).)*?)</PLACE>',
            "replace": r'<settlement subtype="\1" type="\2"><geogName subtype="\1">\g<topo></geogName></settlement>'
        },

        {
            "search": r'key="@([^"]+?) @([^"]+?)"',
            "replace": r'key="\1"'
        },
        {
            "search": r'<term type="@([^"]+?) @([^"]+?)"[^>]*?>(?P<back><term[^>]+?>(?:(?!(<term>)).)*?</term>(?:(?!(<term>)).)*?<term[^>]+?>(?:(?!(</term>)).)*?</term>)</term>',
            "replace": r'\g<back>'
        },
            {
            "search": r'type="@([^"]+?) @([^"]+?)"',
            "replace": r'type="\1 y \2"'
        },
        {
            "search": r'<Compound>(?P<back><term[^>]+?>(?:(?!(<term>)).)*?</term>(?:(?!(<term>)).)*?<term[^>]+?>(?:(?!(</term>)).)*?</term>)</Compound>',
            "replace": r'<term subtype="Compound">\g<back></term>'
        },

        {
            "search": r'<headx',
            "replace": r'<item><label'
        },
        {
            "search": r'</headx>',
            "replace": r'</label></item>'
        },
        {
            "search": r'<item><label subtype="[^"]"/>',
            "replace": r''
        },
        {
            "search": r'(="[^"]*?)<[^>]+?>([^"]*?")',
            "replace": r'\1\2'
        },
        {
            "search": r'(="[^"]*?)<[^>]+?>([^"]*?")',
            "replace": r'\1\2'
        },
        #simple compound variant toponyms (Complex are done above!)
        {
            "search": r'<term type="Landmark" key="([^"]+?)">(?:(?!(</term>)).)*?</term>( ?del? ?l?[oa]?s? )<placeName subtype="Compound" type="Landmark"(.+?)</placeName></placeName>',
            "replace": r'<geogName subtype="explicit_term" type="\1"><term type="Landmark" key="\1">\1</term>\3<placeName subtype="Compound" type="Landmark"\4</placeName></placeName></geogName>'
        },
        {
            "search": r'<term type="Structure" key="([^"]+?)">(?:(?!(</term>)).)*?</term>( ?del? ?l?[oa]?s? )<placeName subtype="Compound" type="Structure"(.+?)</placeName></placeName>',
            "replace": r'<objectName subtype="explicit_term" type="\1"><term type="Structure" key="\1">\1</term>\3<placeName subtype="Compound" type="Structure"\4</placeName></placeName></objectName>'
        },
        {
            "search": r'<term type="Settlement" key="([^"]+?)">(?:(?!(</term>)).)*?</term>( ?del? ?l?[oa]?s? )<placeName subtype="Compound" type="Settlement"(.+?)</placeName></placeName>',
            "replace": r'<settlement subtype="explicit_term" type="\1"><term type="Settlement" key="\1">\1</term>\3<placeName subtype="Compound" type="Settlement"\4</placeName></placeName></settlement>'
        },
        {
            "search": r'<term type="District" key="([^"]+?)">(?:(?!(</term>)).)*?</term>( ?del? ?l?[oa]?s? )<placeName subtype="Compound" type="Settlement"(.+?)</placeName></placeName>',
            "replace": r'<settlement subtype="explicit_term" type="\1"><term type="District" key="\1">\1</term>\3<placeName subtype="Compound" type="Settlement"\4</placeName></placeName></settlement>'
        },
        {
            "search": r'<term type="District" key="([^"]+?)">(?:(?!(</term>)).)*?</term>( ?del? ?l?[oa]?s? )<placeName subtype="Compound" type="Territory"(.+?)</placeName></placeName>',
            "replace": r'<district subtype="explicit_term" type="\1"><term type="District" key="\1">\1</term>\3<placeName subtype="Compound" type="Territory"\4</placeName></placeName></district>'
        },
        {
            "search": r'<term type="Territory" key="([^"]+?)">(?:(?!(</term>)).)*?</term>( ?del? ?l?[oa]?s? )<placeName subtype="Compound" type="Territory"(.+?)</placeName></placeName>',
            "replace": r'<district subtype="explicit_term" type="\1"><term type="Territory" key="\1">\1</term>\3<placeName subtype="Compound" type="Territory"\4</placeName></placeName></district>'
        },
        {
            "search": r'([^>][^> ]( ?del? ?l?[oa]?s? )?)<placeName subtype="Compound" type="Landmark"(.+?)</placeName></placeName>',
            "replace": r'\1<geogName subtype="unresolved_term"><placeName subtype="Compound" type="Landmark"\3</placeName></placeName></geogName>'
        },
                {
            "search": r'([^>][^> ]( ?del? ?l?[oa]?s? )?)<placeName subtype="Compound" type="Settlement"(.+?)</placeName></placeName>',
            "replace": r'\1<settlement subtype="unresolved_term"><placeName subtype="Compound" type="Settlement"\3</placeName></placeName></settlement>'
        },
                {
            "search": r'([^>][^> ]( ?del? ?l?[oa]?s? )?)<placeName subtype="Compound" type="Structure"(.+?)</placeName></placeName>',
            "replace": r'\1<objectName subtype="unresolved_term"><placeName subtype="Compound" type="Structure"\3</placeName></placeName></objectName>'
        },
                {
            "search": r'([^>][^> ]( ?del? ?l?[oa]?s? )?)<placeName subtype="Compound" type="Territory"(.+?)</placeName></placeName>',
            "replace": r'\1<district subtype="unresolved_term"><placeName subtype="Compound" type="Structure"\3</placeName></placeName></district>'
        },
        ###
                {
            "search": r'(<term type="[^"]+?" )type=[^>]+?><term type="([^"]+?)" key="([^"]+?)">(.+?)</term>(.+?)<term type="([^"]+?)" key="([^"]+?)">(.+?)</term></term>',
            "replace": r'\1subtype="Compound" key="\3 y \7"><term type="\2" key="\3">\4</term>\5<term type="\6" key="\7">\8</term></term>'
        },
                {
            "search": r'(_term" )type(="[^"]+?")',
            "replace": r'\1key\2'
        },
                {
            "search": r'<item><label.+?/>',
            "replace": r''
        },
                {
            "search": r'<geogName',
            "replace": r'<geogName type="landmark"'
        },        
                {
            "search": r'<objectName',
            "replace": r'<geogName type="structure"'
        },
                {
            "search": r'</objectName>',
            "replace": r'</geogName>'
        },
]
    #Next group of patterns
    modified_content = original_content
    for pattern in replacement_patterns7:
        modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
    original_content = modified_content





    ################################################################################################
    ###Write to file
    # Write the modified content back to the file with proper encoding
    with open(rootpath+filename+"_TEId.xml", "w", encoding="utf-8") as file:
        modified_content = remove_nonprintable(modified_content)
        modified_content = re.sub(r"\r\n\r\n", r"\r\n", modified_content)
        file.write(modified_content)

    print("Replacement completed.")


    #Ensuring that the number of characters in the actual text remains unchanged.
    input_file_path = rootpath+filename+".xml"
    output_file_path = rootpath+filename+"_TEId.xml"

    input_count = count_characters(input_file_path)
    output_count = count_characters(output_file_path)

    print("Number of characters in input file:", input_count)
    print("Number of characters in output file:", output_count)

    if input_count == output_count:
        print("The number of characters in the input and output files are the same.")
    else:
        print("The number of characters in the input and output files are different.")
        print("Difference:", input_count - output_count)


    
