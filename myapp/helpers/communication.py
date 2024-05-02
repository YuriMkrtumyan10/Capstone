from .gpt import chatgpt_query
import re
from .conversation import agent_with_message
from .pdf import load_pdf

def handle_communication(file_messages, messages):
    response = chatgpt_query(messages)
    found_tags = checkBotTags(response)
    tags = []
    print(response)
    for tag, message, file_required in found_tags:
        tags.append(tag)
        res_m = agent_with_message(modifyTag(tag), message)
        if file_required:
            res_m = res_m + file_messages
        
        print('___________________________-')
        print(res_m)

        res = chatgpt_query(res_m)

        response = replaceBotTags(response, tag, res, file_required)
    return response, tags

def checkBotTags(message):
    pattern = r'\[([^\[\]]+)_START(?:\s([^\[\]]+))?\](.*?)\[\1_END\]'
    matches = re.findall(pattern, message, re.DOTALL)
    results = []
    for match in matches:
        tag, file_required, content = match
        if 'FROM' not in tag:
            file_required = file_required.strip() if file_required else None
            results.append((tag, content.strip(), bool(file_required)))
    return results
 
def replaceBotTags(message, tag, res, file_required=False):
    if file_required:
        pattern = r'\[({}_START IMAGE_REQUIRED)\](.*?)\[{}_END\]'.format(tag, tag)
    else:
        pattern = r'\[({}_START)\](.*?)\[{}_END\]'.format(tag, tag)
    replaced_message = re.sub(pattern, res, message, flags=re.DOTALL)
    return replaced_message

def modifyTag(i):
    return i.lower().replace('_', '-')
