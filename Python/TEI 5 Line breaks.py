import os

rootpath = "F:/EHESS/TopUrbiGit/"
input_dir = rootpath + "TEI/"
output_dir = rootpath + "TEI/"

def replace_newlines(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    
    # Replace consecutive newline characters with just one
    content = content.replace('\r\n\r\n', '\r\n')
    content = content.replace('\n\n', '\n')
    content = content.replace('\r\r', '\r')

    with open(file_path, 'w', encoding='utf-8', newline='\r\n') as outfile:
        outfile.write(content)

if __name__ == "__main__":
    for i in range(1, 6):
        file_path = input_dir + "Alcedo_vol_" + str(i) + ".xml"
        if os.path.exists(file_path):
            replace_newlines(file_path)
            print(f"Newline replacement done for Alcedo_vol_{i}.xml")
        else:
            print(f"File not found: Alcedo_vol_{i}.xml")


### Replace patterns to correct artifacts and structural changes introduced after reflection
##
##
##(<term type="[^"]+?" key=")([^"]+?)(">)\1\2\3(.+?</term>)([^<]+?)(<term[^>]+?key=")([^"]+)
##\1\2\5\7\3\1\2\3\4\5\6\7
##
##
##(<settlement)( subtype="inferred_term" key="[^"]+?)">
##\1><term type="Settlement"\2"/>
##
##(<settlement)( subtype="supplied_term" key="[^"]+?)">
##\1><term type="Settlement"\2"/>
##
##
##(<district)( subtype="inferred_term" key="[^"]+?)">
##\1><term type="Territory"\2"/>
##
##(<district)( subtype="supplied_term" key="[^"]+?)">
##\1><term type="Territory"\2"/>
##
##(<geogName type="Landmark")( subtype="inferred_term" key="[^"]+?)">
##\1><term type="Landmark"\2"/>
##
##(<geogName type="Landmark")( subtype="supplied_term" key="[^"]+?)">
##\1><term type="Landmark"\2"/>
##
##(<geogName type="Structure")( subtype="inferred_term" key="[^"]+?)">
##\1><term type="Structure"\2"/>
##
##(<geogName type="Structure")( subtype="supplied_term" key="[^"]+?)">
##\1><term type="Structure"\2"/>
##
## subtype="explicit_term"
            ##
##
##subtype="unresolved_term">
##><term  subtype="unresolved_term"/>
##            
##placeName type="[^"]+?"
##placeName
##
##Compound" type="[^"]+?"
##Compound"
##            
##(term type="[^"]+?" )key="
##\1ref="TopUrbiIndex.xml#

