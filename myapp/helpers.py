def format_as_gpt_print(text):
    formatted_text = "<div>\n"
    in_list = False
    in_code_block = False
    lines = text.splitlines()

    for line in lines:
        # Handle headings
        if line.startswith("# "):
            if in_list:  # Close the list before starting a new section
                formatted_text += "</ul>\n"
                in_list = False
            formatted_text += f"<h2>{line[2:]}</h2>\n"
        # Handle bullet points
        elif line.startswith("- "):
            if not in_list:
                formatted_text += "<ul>\n"
                in_list = True
            formatted_text += f"<li>{line[2:]}</li>\n"
        # Handle code blocks start
        elif line.startswith("```"):
            if in_code_block:
                formatted_text += "</code></pre>\n"
                in_code_block = False
            else:
                formatted_text += "<div class=\"code-container\"><button class=\"copy-btn\">Copy Code</button><pre class=\"code-block\"><code>\n"
                in_code_block = True
        # Handle code blocks end
        elif in_code_block:
            formatted_text += f"{line}\n"
        # Handle paragraphs/statistics
        elif line.strip() != "":
            if in_list:  # Close the list before adding a paragraph
                formatted_text += "</ul>\n"
                in_list = False
            formatted_text += f"<p>{line}</p>\n"
        else:
            if in_list:
                formatted_text += "</ul>\n"
                in_list = False
            # formatted_text += "<p>&nbsp;</p>\n"

    if in_list:  # Ensure the list is closed if the text ends with bullet points
        formatted_text += "</ul>\n"
    if in_code_block:  # Ensure the code block is closed if the text ends with a code block
        formatted_text += "</code></pre>\n"

    formatted_text += "</div>"
    return formatted_text
