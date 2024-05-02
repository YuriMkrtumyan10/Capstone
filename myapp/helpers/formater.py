import html

def format_as_gpt_print(text):
    formatted_text = "<div>\n"
    in_list = False
    in_code_block = False
    code_language = "plaintext"  # Default code language, can be adjusted as needed

    lines = text.splitlines()

    for line in lines:
        # Handle headings
        if line.startswith("# "):
            if in_list:  # Close the list before starting a new section
                formatted_text += "</ul>\n"
                in_list = False
            formatted_text += f"<h2>{line[2:]}</h2>\n"
        # Handle bullet points
        elif line.startswith("- ") and not line.startswith("- " * 4):  # Ensure it's not a nested list
            if not in_list:
                formatted_text += "<ul>\n"
                in_list = True
            formatted_text += f"<li>{line[2:]}</li>\n"
        # Handle code blocks start and specify language if provided
        elif line.startswith("```"):
            if in_code_block:
                formatted_text += "</code></pre><button class=\"copy-button\" onclick=\"copyCode(this)\">Copy</button></div>\n"
                in_code_block = False
            else:
                code_language = line[3:].strip() or "plaintext"
                formatted_text += f"<div class=\"code-container\"><pre><code class=\"language-{code_language}\">"
                in_code_block = True
        # Handle code block content
        elif in_code_block:
            formatted_text += html.escape(line) + "\n"  # Escape HTML special characters
        # Handle paragraphs/statistics
        elif line.strip() != "":
            if in_list:  # Close the list before adding a paragraph
                formatted_text += "</ul>\n"
                in_list = False
            formatted_text += f"<p>{html.escape(line)}</p>\n"  # Escape HTML special characters
        else:
            if in_list:
                formatted_text += "</ul>\n"
                in_list = False

    # Ensure all open HTML elements are properly closed
    if in_list:
        formatted_text += "</ul>\n"
    if in_code_block:  # Ensure the code block is closed if the text ends within a code block
        formatted_text += "</code></pre><button class=\"copy-button\" onclick=\"copyCode(this)\">Copy</button></div>\n"

    formatted_text += "</div>"
    return formatted_text
