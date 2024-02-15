#Written assisted by Bing CoPilot.
import os
import re

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('<?xml-stylesheet type="text/css" href="../test.css"?>\n<xml>')
        file.write(content)
        file.write('</xml>')
def segment_text_files(input_directory, output_directory):
    # Process each input file
    for i in range(1, 6):
        input_filename = f"txt_vol{i}_annotated.xml"
        input_path = os.path.join(input_directory, input_filename)
        input_content = read_text_file(input_path)

        # Split the content based on <BATCHn/> markers
        batches = re.split(r'<BATCH/>', input_content)
        output_directory = 'F:/EHESS/TopUrbiGit/Alcedo/Annotated/vol_'+str(i)
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Write each batch to a new file
        for j, batch_content in enumerate(batches[1:], start=1):
            output_filename = f"vol{i}_BATCH{j}.xml"
            output_path = os.path.join(output_directory, output_filename)
            write_text_file(output_path, batch_content.strip())

if __name__ == '__main__':
    input_directory = 'F:/EHESS/TopUrbiGit/Alcedo/Annotated'  # Replace with your actual input directory
    output_directory = 'F:/EHESS/TopUrbiGit/Alcedo/Annotated/vol_'  # Replace with your desired output directory

    segment_text_files(input_directory, output_directory)
