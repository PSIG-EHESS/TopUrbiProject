import csv, re, mmap
for n in range(1,6):
    with open("F:/EHESS/Workbench/processing/Input/alcedo-"+str(n)+"-utf8.xml", 'r', encoding="utf-8") as f:
        for line in f:
            passtext=line
            searchedstring = re.search(r'xml:id="(.+?)"',line)
            if searchedstring:
            #print(searchedstring.group(1))
                with open("F:/EHESS/Workbench/processing/Input/tipos.csv", 'r', encoding="utf-8") as fo:
                    reader = csv.reader(fo, delimiter=";")
                    for row in reader:
                        rowid = (row[0])
                        fvalue = (row[1])
                        if rowid==searchedstring.group(1):
                            passtext = re.sub ('<fs></fs>', '<fs><f type="featuretype"><symbol value="'+fvalue+'"/></f></fs>',passtext)
            with  open("F:/EHESS/Workbench/processing/Output/alcedo-"+str(n)+"-utf8.xml", 'a+', encoding="utf-8") as fop:
                fop.write(passtext)
                
                
