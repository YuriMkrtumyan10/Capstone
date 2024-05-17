import html

def format_as_gpt_print(text):
    formatted_text = "<div>\n"
    in_list = False
    in_code_block = False
    code_language = "plaintext"  

    lines = text.splitlines()

    for line in lines:
        if line.startswith("# "):
            if in_list:  
                formatted_text += "</ul>\n"
                in_list = False
            formatted_text += f"<h2>{line[2:]}</h2>\n"
        elif line.startswith("- ") and not line.startswith("- " * 4):  
            if not in_list:
                formatted_text += "<ul>\n"
                in_list = True
            formatted_text += f"<li>{line[2:]}</li>\n"
        elif line.startswith("```"):
            if in_code_block:
                formatted_text += "</code></pre><button class=\"copy-button\" onclick=\"copyCode(this)\">Copy</button></div>\n"
                in_code_block = False
            else:
                code_language = line[3:].strip() or "plaintext"
                formatted_text += f"<div class=\"code-container\"><pre><code class=\"language-{code_language}\">"
                in_code_block = True
        elif in_code_block:
            formatted_text += html.escape(line) + "\n"  
        elif line.strip() != "":
            if in_list:  
                formatted_text += "</ul>\n"
                in_list = False
            formatted_text += f"<p>{html.escape(line)}</p>\n"  
        else:
            if in_list:
                formatted_text += "</ul>\n"
                in_list = False

    if in_list:
        formatted_text += "</ul>\n"
    if in_code_block:  
        formatted_text += "</code></pre><button class=\"copy-button\" onclick=\"copyCode(this)\">Copy</button></div>\n"

    formatted_text += "</div>"
    return formatted_text
