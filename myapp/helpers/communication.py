from .gpt import chatgpt_query
import re
from .conversation import agent_with_message

def handle_communication(messages):
    response = chatgpt_query(messages)
    found_tags = checkBotTags(response)
    tags = []

    for tag, message in found_tags:
        tags.append(tag)
        res_m = agent_with_message(modifyTag(tag), message)
        res = chatgpt_query(res_m)
        response = replaceBotTags(response, tag, 'MotherFucker ' + res + ' end of MotherFucker')
    return response, tags

def checkBotTags(message):
    pattern = r'\[([^\[\]]+)_START\](.*?)\[\1_END\]'
    matches = re.findall(pattern, message, re.DOTALL)
    return matches
 
def replaceBotTags(message, tag, res):
    pattern = r'\[({}_START)\](.*?)\[{}_END\]'.format(tag, tag)
    replaced_message = re.sub(pattern, res, message, flags=re.DOTALL)
    return replaced_message

def modifyTag(i):
    return i.lower().replace('_', '-')
