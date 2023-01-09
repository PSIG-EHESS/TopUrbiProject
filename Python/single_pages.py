# -*- coding: utf-8 -*-
import csv, re, TopUrbi

Main_path = "F:\\EHESS\\Workbench\\"
Master_path = "F:\\EHESS\\Workbench\\Alcedo_Working_master\\"
Output_path = "F:\\EHESS\\Workbench\\processing\\output\\"


    #Already executed lists
##pattern_list= [(r"Ainíaraez\b",r"Aimaraez\b"),(r"Almaraez\b",r"Aimaraez\b"),(r"Andahuailás\b",r"Andahuailas\b"),(r"Andahuallas\b",r"Andahuailas\b"),(r"Antioquía\b",r"Antioquia\b"),(r"Apoiabamba\b",r"Apolobamba\b"),(r"Azüchitlán\b",r"Azuchitlán\b"),(r"Carokna\b",r"Carolina\b"),(r"Cauchucos\b",r"Conchucos\b"),(r"Caxamarcá\b",r"Caxamarca\b"),(r"Caxamarquiíla\b",r"Caxamarquilla\b"),(r"Cáxatambo\b",r"Caxatambo\b"),(r"Chako\b",r"Chaco\b"),(r"Chancáy\b",r"Chancay\b"),(r"Chichieapa\b",r"Chichicapa\b"),(r"Chiiapa\b",r"Chilapa\b"),(r"Chillan\b",r"Chillán\b"),(r"Chiloe\b",r"Chiloé\b"),(r"Chavalo\b",r"Otavalo\b"),(r"Chiametlán\b",r"Chiametlan\b"),(r"Chiripa\b",r"Chiripo\b"),(r"Cholúla\b",r"Cholula\b"),(r"Cicasicá\b",r"Cicasica\b"),(r"Cinagaa\b",r"Cinagua\b"),(r"Cinaioa\b",r"Cinaloa\b"),(r"Cinalóa\b",r"Cinaloa\b"),(r"Ciñaloa\b",r"Cinaloa\b"),(r"Coachucos\b",r"Conchucos\b"),(r"Cochabama\b",r"Cochabamba\b"),(r"Composrela\b",r"Compostela\b"),(r"Compóstela\b",r"Compostela\b"),(r"Conaesuyos\b",r"Condesuyos\b"),(r"Costaricá\b",r"Costarica\b"),(r"Darcen\b",r"Darién\b"),(r"Erasil\b",r"Brasil\b"),(r"Gtiazacapan\b",r"Guazacapan\b"),(r"Marvland\b",r"Maryland\b"),(r"Massadiusséf\b",r"Massachussets\b"),(r"Condeñuyos\b",r"Condesuyos\b"),(r"Conneófcicut\b",r"Connecticut\b"),(r"Contínent\b",r"Continent\b"),(r"Cóntinent\b",r"Continent\b"),(r"Copiapo\b",r"Copiapó\b"),(r"Coyoacan\b",r"Coyoacán\b"),(r"Cozamaloapán\b",r"Cozamaloapan\b"),(r"Cuatemala\b",r"Guatemala\b"),(r"Cuernaváca\b",r"Cuernavaca\b"),(r"Cucatlán\b",r"Cuicatlán\b"),(r"Culcatlán\b",r"Cuicatlan\b"),(r"Cunnecticut\b",r"Connecticut\b"),(r"Delávvare\b",r"Delavvare\b"),(r"Eahía\b",r"Bahía\b"),(r"Earecaja\b",r"Larecaja\b"),(r"Espiritu\b",r"Espíritu\b"),(r"Gaira\b",r"Gairá\b"),(r"Gayra\b",r"Gayrá\b"),(r"Ghinchasuyu\b",r"Chinchasuyo\b"),(r"Gnamalies\b",r"Guamalíes\b"),(r"GuadakazarGuadalcázar\b",r"\b"),(r"Guachionango\b",r"Guachinango\b"),(r"Guajuapn\b",r"Guajuapa\b"),(r"Gualavita\b",r"Guatavita\b"),(r"Güarochiri\b",r"Guarochiri\b"),(r"Guattatlauca\b",r"Guatlatlauca\b"),(r"Guauchiaango\b",r"Guauchinango\b"),(r"Gollahuas\b",r"Collahuas\b"),(r"Guayaña\b",r"Guayana\b"),(r"Guayaría\b",r"Guayana\b"),(r"Guayaua\b",r"Guayana\b"),(r"Gueiozingo\b",r"Guejozingo\b"),(r"Gurmalies\b",r"Guamalíes\b"),(r"Hampihire\b",r"Hampshire\b"),(r"Huáilas\b",r"Huailas\b"),(r"Huamaíies\b",r"Huamalíes\b"),(r"Huamaliectamp\b",r"Huamalíes\b"),(r"Huameíula\b",r"Huamelula\b"),(r"Guanaco\b",r" Guanuco\b"),(r"Huárochiri\b",r"Huarochiri\b"),(r"ítamaraca\b",r"Itamaraca\b"),(r"Ixmiquilpán\b",r"Ixmiquilpan\b"),(r"Jaen\b",r"Jaén\b"),(r"labaté\b",r"Ubaté\b"),(r"Larecaia\b",r"Larecaja\b"),(r"Larecaxá\b",r"Larecaxa\b"),(r"león\b",r"León\b"),(r"ltata\b",r"Itata\b"),(r"Lücanas\b",r"Lucanas\b"),(r"Lusya\b",r"Luya\b"),(r"maiz\b",r"Maíz\b"),(r"Manían d\b",r"Mariland\b"),(r"Mannalco\b",r"Marinalco\b"),(r"Maracaíbo\b",r"Maracaibo\b"),(r"Marañon\b",r"Marañón\b"),(r"Marávatio\b",r"Maravatio\b"),(r"Marinaico\b",r"Marinalco\b"),(r"Marinalcó\b",r"Marinalco\b"),(r"Marínaleo\b",r"Marinalco\b"),(r"Marjland\b",r"Mariland\b"),(r"Massachuséts\b",r"Massachussets\b"),(r"Matyland\b",r"Maryland\b"),(r"Merida\b",r"Mérida\b"),(r"Metida\b",r"Mérida\b"),(r"Mexilcaltzinge\b",r"Mexilcaltzingo\b"),(r"Mextirlan\b",r"Mextitlan\b"),(r"Moguehua\b",r"Moquehua\b"),(r"Molos\b",r"Moxos\b"),(r"Metepee\b",r"Metepec\b"),(r"Nátá\b",r"Nata\b"),(r"Neíba\b",r"Neiba\b"),(r"Nueva Yerck\b",r"Nueva Yorck\b"),(r"Nueva Yorek\b",r"Nueva Yorck\b"),(r"Nueva Yorok\b",r"Nueva Yorck\b"),(r"Parícacochas\b",r"Parinacochas\b"),(r"Quitó\b",r"Quito\b"),(r"Nutva\b",r"Nueva\b",r"\b"),(r"Odupán\b",r"Octupan\b"),(r"Octupán\b",r"Octupan\b"),(r"Octuán\b",r"Octupan\b"),(r"Omasúyos\b",r"Omasuyos\b"),(r"Onzava\b",r"Orizava\b"),(r"Orinaba\b",r"Orizaba\b"),(r"Ostimurí\b",r"Ostimuri\b"),(r"Ostirnuri\b",r"Ostimuri\b"),(r"Otávalo\b",r"Otavalo\b"),(r"Para\b",r"Pará\b"),(r"Paría\b",r"Paria\b"),(r"Parien\b",r"Darién\b"),(r"Patáz\b",r"Pataz\b"),(r"Patiz\b",r"Pataz\b"),(r"Paucárcolla\b",r"Paucarcolla\b"),(r"Paucareolla\b",r"Paucarcolla\b"),(r"Pensiivania\b",r"Pensilvania\b"),(r"Pénsilvania\b",r"Pensilvania\b"),(r"Pensilyania\b",r"Pensilvania\b"),(r"Píuarochiri\b",r"Huarochiri\b"),(r"Popayan\b",r"Popayán\b"),(r"Quiliota\b",r"Quillota\b"),(r"Quillpa\b",r"Quillota\b"),(r"Quispicánchi\b",r"Quispicanchi\b"),(r"Quiüota\b",r"Quillota\b"),(r"Quülóta\b",r"Quillota\b"),(r"Rancagtia\b",r"Rancagua\b"),(r"Raneagua\b",r"Rancagua\b"),(r"Jenelro\b",r"Jeneiro\b"),(r"Riobasnba\b",r"Riobamba\b"),(r"Sagadahoak\b",r"Sagadahock\b"),(r"Sicasicá\b",r"Sicasica\b"),(r"Sicaska\b",r"Sicasica\b"),(r"Sieasica\b",r"Sicasica\b"),(r"Sinalóa\b",r"Sinaloa\b"),(r"Smtiago\b",r"Santiago\b"),(r"Soñora\b",r"Sonora\b"),(r"Sucumbius\b",r"Sucumbios\b"),(r"Surinám\b",r"Surinam\b"),(r"Taranmará\b",r"Taraumara\b"),(r"Taraumará\b",r"Taraumara\b"),(r"Taríuimara\b",r"Taraumara\b"),(r"Tecpatitlari\b",r"Tecpatitlán\b"),(r"Teotihuacan\b",r"Teotihuacán\b"),(r"Tepequana\b",r"Tepeguana\b"),(r"Tépeguana\b",r"Tepeguana\b"),(r"Tepozcoíula\b",r"Tepozcolula\b"),(r"Tepozcoltila\b",r"Tepozcolula\b"),(r"Tequepesra\b",r"Tequepexpa\b"),(r"Teroantepec\b",r"Tecoantepec\b"),(r"Thehuacán\b",r"Thehuacan\b"),(r"Thenuacan\b",r"Thehuacan\b"),(r"Tixtlán\b",r"Tixtlan\b"),(r"Tolúca\b",r"Toluca\b"),(r"Tiapa\b",r"Tlapa\b"),(r"Tiüpa\b",r"Tlapa\b"),(r"Traxillo\b",r"Truxillo\b"),(r"Truxulo\b",r"Truxillo\b"),(r"Ttuzitan\b",r"Teuzitan\b"),(r"Tunia\b",r"Tunja\b"),(r"Ubate\b",r"Ubaté\b"),(r"Vailadolid\b",r"Valladolid\b"),(r"Valiadolid\b",r"Valladolid\b"),(r"Valparaiso\b",r"Valparaíso\b"),(r"Veiez\b",r"Velez\b"),(r"Vilialta\b",r"Villalta\b"),(r"Vilcas-huaman\b",r"Vilcas-huamán\b"),(r"Vilcashuaman\b",r"Vilcashuamán\b"),(r"Vucas\b",r"Vilcas\b"),(r"Vücas\b",r"Vilcas\b"),(r"Xacamarquiíía\b",r"Xacamarquilla\b"),(r"Xaiapa\b",r"Xalapa\b"),(r"Xicayan\b",r"Xicayán\b"),(r"Xkayan\b",r"Xicayán\b"),(r"Yámpares\b",r"Yamparaes\b"),(r"Yanquitlán\b",r"Yanguitlán\b"),(r"Yapizbga\b",r"Yapizlaga\b"),(r"Yzucár\b",r"Yzucar\b"),(r"Zacapúla\b",r"Zacapula\b"),(r"Zapópan\b",r"Zapopan\b"),(r"Zapatlán\b",r"Zapotlan\b"),(r"Zayuia\b",r"Zayula\b"),(r"Zayúla\b",r"Zayula\b"),(r"Zipaquira\b",r"Zipaquirá\b"),(r"Zuliepéc\b",r"Zultepec\b"),(r"Aracames\b",r"Atacames\b"),(r"Zacatepegues\b",r"Zacatepeques\b"),(r"Zacatían\b",r"Zacatlan\b"),(r"Topiá\b",r"Topia\b"),(r"Topía\b",r"Topia\b"),(r"Topja\b",r"Topia\b"),(r"Tabanco\b",r"Tabasco\b"),(r"Tepéaca\b",r"Tepeaca\b"),(r"Tierrarirme\b",r"Tierrafirme\b"),(r"Tierrafírme\b",r"Tierrafirme\b"),(r"Darlen\b",r"Darién\b")]
def replace_pattern(text):
    for pattern in pattern_list:
        text=re.sub(pattern[0],pattern[1], text)
    return(text)


    #Dummy list. Fill with tuples of replace patterns
pattern_list =[(r'<TEI.+?<div n="title"><p>',
                r''),
                (r'\r\n',
                r''),
                (r'<entry xml:id="(.+?)".+?>',
                r'€€€§§§\1§§§€€€'),
               (r'<pb n="(.+?)-(.+?)"/>',
                r'€€€@@@\1-\2@@@€€€'),
               (r'<xr>',
                r'###'),
               (r'</xr>',
                r'###'),
               (r'<sense>',
                r' '),
               (r'<.+?>',
                r''),
               (r'€€€(§§§.+?§§§€€€)(€€€@@@.+?@@@€€€)',
                   r'\2\1'),
               (r'\r\n',
                r''),
               (r'\n',
                r''),
               (r'€€€@@@',
                r'\r\n€€€@@@'),
               (r'.+?€€€\r\n@@@Alcedo_vol_([0-9])-titular@@@',
                r'€€€@@@Alcedo_vol_\1-titular@@@'),
               (r'  ',
                r' '),
               ]

##for vol in range(1,6):
##    with open(Master_path+"alcedo-"+str(vol)+"-utf8.xml", 'r', encoding="utf-8") as myinput:
##        text= myinput.read()
##        text = replace_pattern(text)
##        with open(Output_path+"alcedo-"+str(vol)+"textonly.txt", 'w+', encoding="utf-8") as myoutput:
##            myoutput.write(text)
##            myoutput.close()

for vol in range(1,6):
    with open(Output_path+"alcedo-"+str(vol)+"textonly.txt", 'r', encoding="utf-8") as myinput:
        for line in myinput:
            pagenumber = re.search(r'€€€@@@(.+?)@@@€€€', line)
            title = pagenumber.group(1)
            #print(title)
            with open(Output_path+'text_pages\\vol'+str(vol)+'\\'+title+".txt", 'w+', encoding="utf-8") as myoutput:
                contents= re.sub(r'€€€',r'\n', line)
                myoutput.write(contents)
                myoutput.close()
