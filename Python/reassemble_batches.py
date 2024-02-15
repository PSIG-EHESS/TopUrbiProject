##import os
##
##def read_text_file(file_path):
##    with open(file_path, 'r', encoding='utf-8') as file:
##        return file.read()
##
##def write_text_file(file_path, content):
##    with open(file_path, 'w', encoding='utf-8') as file:
##        file.write(content)
##
##def reassemble_files(input_directory):
##    # Process each subdirectory (vol_1 to vol_5)
##    for i in range(1, 6):
##        subdirectory = f"vol_{i}"
##        output_filename = f"vol_{i}_reassembled.xml"
##        output_path = os.path.join(input_directory, output_filename)
##
##        # Initialize the reassembled content
##        reassembled_content = ""
##
##        # Iterate through batch files in the subdirectory
##        for filename in os.listdir(os.path.join(input_directory, subdirectory)):
##            if filename.startswith("vol"):
##                batch_path = os.path.join(input_directory, subdirectory, filename)
##                batch_content = read_text_file(batch_path)
##                reassembled_content += "<BATCH/>"+batch_content
##
##        # Write the reassembled content to the output file
##        write_text_file(output_path, reassembled_content)
##
##if __name__ == '__main__':
##    input_directory = 'F:/EHESS/TopUrbiGit/Alcedo/Annotated'  # Replace with your actual input directory
##    reassemble_files(input_directory)
##


import os
import re
from pathlib import Path

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_batch_files(input_directory):
    # Get a list of batch files sorted by modification date
    batch_files = []
    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.startswith("vol") and filename.endswith(".xml"):
                file_path = os.path.join(root, filename)
                batch_files.append((file_path, os.path.getmtime(file_path)))

    # Sort batch files by modification date
    sorted_batch_files = sorted(batch_files, key=lambda x: x[1])
    return [file_path for file_path, _ in sorted_batch_files]

def reassemble_files(input_directory):
    # Process each subdirectory (vol_1 to vol_5)
    for i in range(1, 6):
        subdirectory = f"vol_{i}"
        output_filename = f"txt_vol{i}_annotated.xml"
        output_path = os.path.join(input_directory, output_filename)

        # Initialize the reassembled content
        reassembled_content = ""

        # Get sorted batch files
        batch_files = get_batch_files(os.path.join(input_directory, subdirectory))

        # Read and concatenate batch contents
        for batch_file in batch_files:
            batch_content = read_text_file(batch_file)
            reassembled_content += "<BATCH/>"+batch_content

        # Write the reassembled content to the output file
        write_text_file(output_path, reassembled_content)

if __name__ == '__main__':
    input_directory = 'F:/EHESS/TopUrbiGit/Alcedo/Annotated'  # Replace with your actual input directory
    reassemble_files(input_directory)
