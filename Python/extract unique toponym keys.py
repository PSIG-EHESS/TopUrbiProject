import re
import csv

pattern= r'<PLACE[^>]+?key="([^"]+)"[^>]*?>(?!</PLACE>).*?<placeName[^>]+?type="([^"]+)"[^>]*?>([^<]+?)</placeName>'

rootpath="F:/EHESS/TopUrbiGit/Alcedo/Annotated/"
filename_list = ['vol_1_annotated','vol_2_annotated','vol_3_annotated','vol_4_annotated','vol_5_annotated']

# Open a CSV file to write the results
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header
    writer.writerow(['Tag', 'Text'])
    for filename in filename_list:
        with open(rootpath+filename+'_TEId.xml', 'r', encoding="utf-8") as file:
            input_string = file.read()
            # Find all matches
            matches = re.findall(pattern, input_string)
            # Write matches to CSV
            for match in matches:
                writer.writerow([match])
