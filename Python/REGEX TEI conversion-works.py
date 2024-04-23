import re

rootpath="F:/EHESS/TopUrbiGit/Alcedo/Annotated/"

type_list=['Settlement','Structure','Territory','Landmark']

toponym_list = [
    {"1": r'Perú', "2": 'Territory', "3": 'Reyno'},
    {"1": r'América', "2": 'Territory', "3": ''},
    {"1": r'Indias', "2": 'Territory', "3": ''},
    {"1": r'Carolina', "2": 'Territory', "3": ''},
    {"1": r'Europa', "2": 'Territory', "3": ''},
    {"1": r'España', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Italia', "2": 'Territory', "3": ''},
    {"1": r'Virginia', "2": 'Territory', "3": '@Provincia @Colonia'},
    {"1": r'Portugal', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Alemania', "2": 'Territory', "3": ''},
    {"1": r'Francia', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Chile', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Inglaterra', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Andalucía', "2": 'Territory', "3": 'Región'},
    {"1": r'Vizcaya', "2": 'Territory', "3": 'Región'},
    {"1": r'Castilla', "2": 'Territory', "3": ''},
    {"1": r'Nuevo [mM]undo', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Nueva España', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Brasil', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Nueva Inglaterra', "2": 'Territory', "3": ''},
    {"1": r'Florida', "2": 'Territory', "3": 'Provincia'},
    {"1": r'Venezuela', "2": 'Territory', "3": 'Provincia'},
    {"1": r'Guayana', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Nuevo México', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Nuevo Reyno de León', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Nuevo Reyno de Granada', "2": 'Territory', "3": 'Reyno'},
    {"1": r'Antilles', "2": 'Landmark', "3": 'Islas'},
    {"1": r'Paraguay', "2": 'Landmark', "3": 'Río'},
    {"1": r'Apurimac', "2": 'Landmark', "3": 'Río'},
    {"1": r'Rimac', "2": 'Landmark', "3": 'Río'},
    {"1": r'Biobio', "2": 'Landmark', "3": 'Río'},
    {"1": r'Atrato', "2": 'Landmark', "3": 'Río'},
    {"1": r'Meta', "2": 'Landmark', "3": 'Río'},
    {"1": r'Uruguay', "2": 'Landmark', "3": 'Río'},
    {"1": r'Orinoco', "2": 'Landmark', "3": 'Río'},
    {"1": r'Amazonas', "2": 'Landmark', "3": 'Río'},
    {"1": r'Marañ[oó]n', "2": 'Landmark', "3": 'Río'},
    {"1": r'Pampas', "2": 'Landmark', "3": 'Llanuras'},
    {"1": r'Andes', "2": 'Landmark', "3": 'Cordillera'},
    {"1": r'Paraná', "2": 'Landmark', "3": 'Río'}
]
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


# Read the content of the file "TEST-REPLACE.xml" with proper encoding
with open(rootpath+"TEST_REPLACE-input.xml", "rb") as file:
    original_content = file.read().decode("utf-8")

# Define the replacement patterns
replacement_patterns = [
    #7 Temporarily change <pb/> and <cb/> to ease capturing in later replace patterns.
    {
        "search": r"<([cp]b[^<]+?)/>",
        "replace": r"€\1/ß"
    },
    # 1 Wrap Compound Concepts of same type ( <Concept_Territory>Provincia</Concept_Territory> y <Concept_Territory>País</Concept_Territory> )
    {
        "search": r"(<Concept_)([^<]+?)>([^<]+?)(</Concept_)\2>(,? [yoúe] )\1\2>([^<]+?)\4\2>",
        "replace": r'<Compoundterm subtype="explicit" type="\2" key="@\3 @\6"><term subtype="explicit" type="\2" key="\3"ß\3</term>\5<term subtype="explicit" type="\2" key="\6"ß\6</term></Compoundterm>'
    },
    # 2 Wrap Compound concepts of mixed type ( <Concept_District>distrito</Concept_District> y <Concept_Territory>jurisdicción</Concept_Territory> )
    {
        "search": r"(<Concept_)([^<]+?)>([^<]+?)(</Concept_)\2>(,? [yoúe] )\1([^<]+?)>([^<]+?)\4\6>",
        "replace": r'<Compoundterm subtype="explicit" type="@\2 @\6" key="@\3 @\7"><term subtype="explicit" type="\2" key="\3"ß\3</term>\5<term subtype="explicit" type="\6" key="\7"ß\7</term></Compoundterm>'
    },
    #3 Remove Compoundterm compounds of Concept_Group  ( <Compoundterm type="Group" key="@Mulatos @Mestizos"><term type="Group" key="Mulatos">Mulatos</term> y <term type="Group" key="Mestizos">Mestizos</term></Compoundterm> )
    {
        "search": r"<Compoundterm type[^<]+?@?Group[^<]+?>([^<]+?)</Compoundterm>",
        "replace": r"\1"
    },
    #Replace compounds of complex group terms (Nación bárbara y feroz de Indios infieles)
    {
        "search": r'<Compound><Concept_Group>([^<]+?)</Concept_Group>([^<]+?)<Concept_Group>(?P<third>[^<]+?)</Concept_Group>(?P<back>(?P<fourth>([^<]+?)?)<Concept_Group>(?P<fifth>([^<]+?))(</Concept_Group>)?)</Compound>',
        "replace": r'<Compoundterm subtype="explicit" type="Group" key="\1\2\g<third>\g<fourth>\g<fifth>"><term subtype="explicit" type="Group" key="\1"ß\1</term>\2<term subtype="explicit" type="Group" key="\g<third>"ß\g<third></term>\g<back></Compoundterm>'
        },
        {
        "search": r'<Compound><Concept_Group>([^<]+?)</Concept_Group>([^<]+?)<Concept_Group>(?P<third>[^<]+?)</Concept_Group>(?P<back></Compound>)',
        "replace": r'<Compoundterm subtype="explicit" type="Group" key="\1\2\g<third>"><term subtype="explicit" type="Group" key="\1"ß\1</term>\2<term subtype="explicit" type="Group" key="\g<third>"ß\g<third></term</Compoundterm>'
        },    
    #4 Remove Compoundterm for last pair in enumerations of concepts (</Concept_Landmark>, <Compoundterm type="Landmark" key="@barrancas @montes"><term type="Landmark" key="barrancas">barrancas</term> y <term type="Landmark" key="montes">montes</term></Compoundterm>)
    {
        "search": r"(<Concept_[^<]+?>[^<]+?</Concept_[^<]+?>, )<Compoundterm type[^<]+?>([^<]+?)</Compoundterm>",
        "replace": r"\1"
    },
    #5 Replace non-compound concepts with <term> ( <Concept_Settlement>Pueblo</Concept_Settlement> )
    {
        "search": r"(<Concept_)([^<]+?)>([^<]+?)(</Concept_)\2>",
        "replace": r'<term subtype="explicit" type="\2" key="\3">\3</term>'
    },
    #6 Wrap toponym-composites with variant toponyms. ( <Territory>Nueva Francia</Territory> o <Territory>Canadá</Territory> )
    {
        "search": r"<(?P<p1>((Territory)?(Settlement)?(Landmark)?(Structure)?))>(?P<p2>[^<]+?)<(?P<p3>/\1)>(?P<conn>,? [oú] (?:del? ?l[oa]s? )?)<(?P<p5>\1)>(?P<p6>[^<]+?)<(?P<p7>/\1)>",
        "replace": r'<placeName subtype="explicit" type="\g<p1>" key="@\g<p2> @\g<p6>">€placeNameß\g<p2>€/placeNameß\g<conn>€placeNameß\g<p6>€/placeNameß</placeName>'
    },
    #add type territory to isla-territories
    {
        "search": r'type="Landmark" key="([iI]slas?">[iI]slas?)</term> de <placeName type="Territory">([^<]+?)</placeName>',
        "replace": r'type="@Landmark @Territory" key="\1</term> de <placeName type="Territory">\2</placeName>'
    },
    #add type settlement to presidios
    {
        "search": r'(<term subtype="explicit" type=")(Settlement)(" key="[Pp]residio">[pP]residio</term>)',
        "replace": r'\1@\2 @Structure\3'
    },
    #8 Wrap type-toponym-compounds of coinciding type (Ciudad de Guatemala) ojo
    {
        "search": r'(<)(term subtype="explicit" type=\")([^<]+?)(\"[^<]+?>)([^<]+?)(</)(term>)( )(€[^<]+/ß)?(del? ?)?(€[^<]+/ß)?(l[oa]s? )?(<)\3(>[^<]+?)(</)\3(>)',
        "replace": r"<PLACE>\g<0></PLACE>"
    },
    #9 Wrap type-toponym-compounds in simple compounds (Provincia y Corregimiento de Chancay) ojo
    {
        "search": r'(<)(Compoundterm subtype="explicit" type=\")([^<]+?)(\"[^<]+?>)([^<]+?)(</)(Compoundterm>)( )(€[^<]+/ß)?(del? ?)?(€[^<]+/ß)?(l[oa]s? )?(<)\3(>[^<]+?)(</)\3(>)',
        "replace": r"<PLACE>\g<0></PLACE>"
    },
    #10 Wrap type-toponym-compounds in mixed-compound terms (Pueblo y Curato de Autlan) ojo
    {
        "search": r'(<Compoundterm subtype="explicit" type=\"@)([^<]+?)( )(@)([^<]+?)(\"[^<]+?>)([^<]+?)(</Compoundterm>)( )(€[^<]+/ß)?(del? ?)?(€[^<]+/ß)?(l[oa]s? )?(<)\2?\5?(>[^<]+?)(</)\2?\5?(>)',
        "replace": r"<PLACE>\g<0></PLACE>"
    },
    #11 Wrap island-territory compounds (isla de Cuba) ojo
    {
        "search": r'(<term subtype="explicit" type=\")([^<]+?)(\"[^<]+?[iI]sla[^<]+?>)([^<]+?)(</term>)( )(€[^<]+/ß)?(del? ?)?(€[^<]+/ß)?(l[oa]s? )?(<)Territory(>[^<]+?)(</)Territory(>)',
        "replace": r"<PLACE>\g<0></PLACE>"
    },
    # Wrap type-toponym-compounds in simple District-Settlement/Territory cases (Partido de Tarija; Parroquia de James) ojo
    {
        "search": r'(<term subtype="explicit" type=\")District(\"[^<]+?>)([^<]+?)(</term>)( )(€[^<]+/ß)?(del? ?)?(€[^<]+/ß)?(l[oa]s? )?(<)(Territory)?(Settlement)?(>[^<]+?)(</)(Territory)?(Settlement)?(>)',
        "replace": r"<PLACE>\g<0></PLACE>"
    },
    # Wrap type-toponym-compounds in simple compound District-Settlement/Territory cases (distrito y Partido de Tarija; distrito y Parroquia de James) ojo
    {
        "search": r'(<Compoundterm subtype="explicit" type=\")District(\"[^<]+?>)([^<]+?)(</Compoundterm>)( )(€[^<]+/ß)?(del? ?)?(€[^<]+/ß)?(l[oa]s? )?(<)(Territory)?(Settlement)?(>[^<]+?)(</)(Territory)?(Settlement)?(>)',
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

    ##Second resolution group
    #Wrap second item in enumeration of toponyms of same type
    {
        "search": r'(<PLACE>)(<term.*?type=")([^<]+?)(" key=")([^"]+?)(s">)([^<]+?)(</term>)([^<]+?)(<placeName type=")\3(">)(?P<topo1>[^<]+?)(</placeName>)(</PLACE>)(?P<conn2>,? ?y?e? )(<)\3(>)(?P<topo2>[^<]+?)(</)\3(>)',
        "replace": r'<term type="\3" key="\5s">\5s</term> de <PLACE type="\3" subtype="inferred" key="\5">€placeName type="\3"ß\g<topo1>€/placeNameß</PLACE>\g<conn2><PLACE type="\3" subtype="inferred" key="\5">€placeName type="\3"ß\g<topo2>€/placeNameß</PLACE>µ'
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
    #Wrap third item in list of toponyms of same type
    {
        "search": r'<PLACE type="([^<]+?)" subtype="inferred" key="([^<]+?)">€placeName type="\1"ß([^<]+?)€/placeNameß</PLACE>µ(,? ?y?e? [^<]{0,7})<\1>([^<]+?)</\1>',
        "replace": r'<PLACE type="\1" subtype="inferred" key="\2">€placeName type="\1"ß\3€/placeNameß</PLACE>\4<PLACE type="\1" subtype="inferred" key="\2">€placeName type="\1"ß\5€/placeNameß</PLACE>µ\1µ\2µµ'

    },

        # add type to first item in list
    {
        "search": r'(?P<front><list subtype="(?P<subtype>(?!mixed)(?!people)(?!organization)[^"]+?)".+?\r\n)(?P<back>(<item>)(.+?)?(.+?)((.+?)?</item>\r\n))',
        "replace": r'\g<front>µ\g<subtype>µµ\g<back>'
    },
]


################################################################################################

# Apply the replacement patterns
modified_content = original_content
for pattern in replacement_patterns:
    modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
original_content = modified_content


#First looping interlude
for typeq in type_list:
    replacement_patterns2 = [
        # Wrap subsequent items in enumeration of toponyms of the same type - must loop
        {
            "search": r'µ([^<µ]+?)µ([^<µ]+?)µµ(,? ?y?e? [^<]{0,7})<\1>([^<]+?)</\1>',
            "replace": r'\3 <PLACE type="\1" subtype="inferred" key="\2">€placeName type="\1"ß\4€/placeNameß</PLACE>µ\1µ\2µµ'
        },
        # Subsequent list items
        {
            "search": r'(?P<front>µ[^µ]+?µµ)(?P<back>(<item>.*?)</item>\r\n)',
            "replace": r'\g<front>\§\g<back>\g<front>'
        },
        # Subsequent list items
        {
            "search": r'(?P<fore>(µ)(?P<type>[^µ]+?)(µµ\\§))(?P<front><item>.*?)<'+typeq+'>(?P<topo>.+?)</'+typeq+'>(?P<back>.*?</item>)',
            "replace": r'\g<front><PLACE type="'+typeq+'" subtype="inferred" key="\g<type>">€placeName type="'+typeq+'"ß\g<topo>€/placeNameß</PLACE>\g<back>'
        },
    ]
    while True:
        modified_content = original_content
        for pattern in replacement_patterns2:
            modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)

        if modified_content == original_content:
            break  # No more matches, exit the loop
        original_content = modified_content


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
        "search": r'(<term type="Territory" key=")([^<]+?)(">[^<]+?</term>[^<]+?)(<term type="Settlement"[^<]+?>[^<]+?</term>[^<]+?)<Territory>(?P<topo1>[^<]+?)</Territory>',
        "replace": r'<PLACE type="Territory" key="\2">\1\2\3\4\5€placeName type="Territory"ß\g<topo1>€/placeNameß</PLACE>'
        },   
    {
        "search": r'µ[^µ<]+?µ[^µ<]+?µµ',
        "replace": r''
        },
##    {
##        "search": r'',
##        "replace": r''
##        },
    ]

#Next group of patterns
modified_content = original_content
for pattern in replacement_patterns3:
    modified_content = re.sub(pattern["search"], pattern["replace"], modified_content)
original_content = modified_content



#Supply type and key for  unique Toponym
for typeq in type_list:
    for toponym in toponym_list:
        if str(toponym["2"])==typeq:
            modified_content = original_content
            modified_content = re.sub('<'+typeq+'>'+str(toponym["1"])+'( [A-Z][a-z]+)?</'+typeq+'>','<PLACE type="'+typeq+'" subtype="inferred" key="'+str(toponym["3"])+'">€placeNameß'+str(toponym["1"])+'\1€/placeNameß</PLACE>', modified_content)
            #print("search for "+'<'+typeq+'>'+str(toponym["1"])+'( [A-Z][a-z]+)?</'+typeq+'>')
            original_content = modified_content

##Wrap cases where the territory-type is defined by a preceding role (Gobernador, Rey...)
for role in role_list:
    modified_content = original_content
    modified_content = re.sub('(?P<b1>'+str(role["1"])+')' +'(?P<b2> del? ?l?a? )<Territory>'+'(?P<b3>[^<]+?)'+'</Territory>','\g<b1>\g<b2><PLACE type="Territory" subtype="inferred" key="'+str(role["2"])+'">€placeNameß\g<b3>€/placeNameß</PLACE>', modified_content)
    original_content = modified_content



# Define the next replacement patterns
replacement_patterns4 = [
    #key masculin feminin plural
    {
        "search": r'key="([^"]+?[oe])(s?)">',
        "replace": r'gender="m\2" key="\1\2">'
    },
    {
        "search": r'key="([^"]+?a)(s?)">',
        "replace": r'gender="f\2" key="\1\2">'
    },
    {
        "search": r'(gender=")ms" (?P<cap>key="(naciones)?(ciudades)?(poblaciones)?">)',
        "replace": r'(gender=")fs" \g<cap>'
    },
##    {
##        "search": r'',
##        "replace": r''
##        },
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
                                  r'\g<front>\g<conn><PLACE type="'+typeq+'" key="\g<key>" type="'+typeq+'" subtype="inferred">€placeNameß\g<topo>€/placeNameß</PLACE>', modified_content)
        if modified_content == original_content:
            break  # No more matches, exit the loop
        original_content = modified_content



connector_list_f = ['con la de ', 'en la de ', 'de la de ', 'a la de ']
connector_list_m = ['con el de ', 'en el de ', 'del de ', 'al de ']

### Resolve relative mentions (de la de; al de; con la de...)
##for typeq in type_list:
##    for connector in connector_list_f:
##        modified_content = original_content
##        modified_content = re.sub('<PLACE type="'+typeq+'" key="(?P<key>[^"]+?)" gender="f">([^<]+?)</PLACE>(?:(?!<PLACE).*?)*?'+connector+'<'+typeq+'>(?P<topo>[^<]+?)</'+typeq+'>',
##                                  connector+'<PLACE type="'+typeq+' subtype="inferred" key="\g<key>" gender="f">\g<topo></PLACE>äää')
##        original_content = modified_content



modified_content = modified_content.replace("\r\r", "\r")
# Write the modified content back to the file with proper encoding
with open(rootpath+"TEST_REPLACE-output.xml", "w", encoding="utf-8") as file:

    file.write(modified_content)

print("Replacement completed.")
