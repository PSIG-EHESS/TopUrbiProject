import codecs

def remove_line_breaks(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    content_without_breaks = "".join(content.splitlines())

    with codecs.open(filename, 'w', encoding='utf-8') as file:
        file.write(content_without_breaks)

def add_line_breaks_after_zbr(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    modified_content = content.replace("<zbr/>", "<zbr/>\r\n")

    with codecs.open(filename, 'w', encoding='utf-8') as file:
        file.write(modified_content)
        # Example usage for four files: 1.txt, 2.txt, 3.txt, and 4.txt
file_list = ['vol_1_annotated.xml', 'vol_2_annotated.xml', 'vol_3_annotated.xml', 'vol_4_annotated.xml']
for filename in file_list:
    path="F:/EHESS/TopUrbiGit/Alcedo/Annotated/"
    remove_line_breaks(path+filename)
    add_line_breaks_after_zbr(path+filename)
