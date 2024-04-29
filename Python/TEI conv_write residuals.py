import csv
import re

# Function to extract content from input and write to CSV
def extract_content(input_file, tag_list, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        input_content = f.read()

    data = []

    # Regex pattern to match entries
    entry_pattern = r'<entry(?:\s+xml:id="(.*?)")?(.*?)</entry>'
    
    # Find entries
    entries = re.finditer(entry_pattern, input_content, re.DOTALL)

    for entry_match in entries:
        entry_id = entry_match.group(1) if entry_match.group(1) else ''
        entry_content = entry_match.group(2)

        # Strip tags, line breaks, and incomplete tags from entry content
        entry_content_stripped = re.sub(r'<[^>]+>', '', entry_content)
        entry_content_stripped = entry_content_stripped.replace('\n', ' ').strip()
        entry_content_stripped = re.sub(r'\s*<[^>]+>\s*', '', entry_content_stripped)  # Remove incomplete tags
        
        # Remove initial '>' if present
        if entry_content_stripped.startswith('>'):
            entry_content_stripped = entry_content_stripped[1:].strip()

        for tag in tag_list:
            tag_pattern = fr'<{tag}>(.*?)</{tag}>'
            matches = re.finditer(tag_pattern, entry_content, re.DOTALL)
            for match in matches:
                value = match.group(1)
                value_with_tag = match.group(0)
                
                # Find the position of the match in the original entry content
                match_start = entry_content.find(value_with_tag)
                match_end = match_start + len(value_with_tag)
                
                # Extract context from the original entry content
                context_left_end = max(0, match_start - 300)
                context_right_start = min(len(entry_content), match_end + 300)
                
                context_left = entry_content[context_left_end:match_start]
                context_right = entry_content[match_end:context_right_start]
                
                # Strip tags, line breaks, and incomplete tags from context
                context_left_stripped = re.sub(r'<[^>]+>', '', context_left)
                context_left_stripped = context_left_stripped.replace('\n', ' ').strip()
                context_left_stripped = re.sub(r'\s*<[^>]+>\s*', '', context_left_stripped)  # Remove incomplete tags
                context_left_stripped = re.sub(r'<[^>]*$', '', context_left_stripped)  # Remove trailing incomplete tags
                context_left_stripped = re.sub(r'^[^<]*>', '', context_left_stripped)  # Remove incomplete tags at start
                
                context_right_stripped = re.sub(r'<[^>]+>', '', context_right)
                context_right_stripped = context_right_stripped.replace('\n', ' ').strip()
                context_right_stripped = re.sub(r'\s*<[^>]+>\s*', '', context_right_stripped)  # Remove incomplete tags
                context_right_stripped = re.sub(r'<[^>]*$', '', context_right_stripped)  # Remove trailing incomplete tags
                context_right_stripped = re.sub(r'^[^<]*>', '', context_right_stripped)  # Remove incomplete tags at start
                
                data.append((entry_id, tag, value))  

    # Write to CSV
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='§')
        csv_writer.writerow(['xml:id', 'Tag', 'Match Value'])
        csv_writer.writerows(data)

# Example usage
rootpath = "F:/EHESS/TopUrbiGit/Alcedo/Annotated/"
filename_list = ['vol_1_annotated_TEId','vol_2_annotated_TEId','vol_3_annotated_TEId','vol_4_annotated_TEId','vol_5_annotated_TEId']

for filename in filename_list:
    if __name__ == "__main__":
        input_file = rootpath+filename+'.xml'  # Replace with your file path
        tag_list = ['Settlement','Structure','Territory','Landmark']
        output_file = rootpath+'residuals.csv'
        
        extract_content(input_file, tag_list, output_file)
