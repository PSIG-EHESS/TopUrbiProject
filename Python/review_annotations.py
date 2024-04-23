rootpath="F:/EHESS/TopUrbiGit/Alcedo/Annotated/"

import re

def get_context_and_entry(content, tag_type, same_value):
    modified_content = content
    # Find all matches for the given tag
    matches = re.finditer(fr"<{tag_type}>(.*?)</{tag_type}>", content)

    for match in matches:
        # Extract the matched string
        matched_string = match.group(1)

        # Find the position of the matched string in the content
        start_index = match.start(0)
        end_index = match.end(0)

        # Get the context (10 characters before and after the matched tag)
        context = content[max(0, start_index - 10): min(len(content), end_index + 10)]
        context = re.sub(fr"<{tag_type}>(.*?)</{tag_type}>", r"\1", context)

        # Highlight matched string and context
        context = context.replace(matched_string, f"<b>{matched_string}</b>")
        matched_string = f"<b>{matched_string}</b>"

        # Get the entire content of the wrapping entry tag
        entry_match = re.search(r"<entry.*?>(.*?)</entry>", content, re.DOTALL)
        entry_content = entry_match.group(1) if entry_match else ""
        stripped_entry_content = re.sub(r'<.*?>', '', entry_content) # Strip tags

        # Get suggested keys
        first_term_key = re.search(fr'<term type="{tag_type}" key="(.*?)"', entry_content)
        last_term_key = re.findall(fr'<term type="{tag_type}" key="(.*?)"', entry_content)[-1] if re.findall(fr'<term type="{tag_type}" key="(.*?)"', entry_content) else ""

        # Display context and entry content
        print(f"Context: {context}")
        print(f"Matched String: {matched_string}")
        print(suggested_types(first_term_key, last_term_key))

        if same_value:
            user_input = input(f"Indicate type for {matched_string}: ")
            updated_tag = f'<{tag_type} type="{user_input}">{matched_string}</{tag_type}>'
        else:
            user_input = input("Indicate type (or 'skip' to skip this instance): ")
            if user_input.lower() == 'skip':
                continue
            updated_tag = f'<{tag_type} type="{user_input}">{matched_string}</{tag_type}>'

        # Replace the original tag with the updated one
        modified_content = modified_content[:start_index] + updated_tag + modified_content[end_index:]

    return modified_content

def suggested_types(first_term_key, last_term_key):
    suggestions = f"Suggested types. 1: {first_term_key} 2: {last_term_key}"
    return suggestions

def main():
    with open(rootpath+"TEST_REPLACE-output.xml", "r", encoding="utf-8") as file:
        content = file.read()

    tag_type = input("Enter tag type (Territory, Settlement, or Landmark): ").strip()
    same_value = input("Should all instances of the same term receive the same attribute value? (yes/no): ").strip().lower()
    same_value = same_value == 'yes'

    modified_content = get_context_and_entry(content, tag_type, same_value)

    with open(rootpath+"TEST_REPLACE-output.xml", "w", encoding="utf-8") as file:
        file.write(modified_content)

if __name__ == "__main__":
    main()


#    with open(rootpath+"TEST_REPLACE-output.xml", "w", encoding="utf-8") as file:

