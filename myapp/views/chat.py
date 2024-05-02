from django.shortcuts import render
from ..helpers.conversation import find_conversation, bringAgentsConversations
from ..constants import agents

def orchestrator(request, guid = None):
    conversation, messages = find_conversation(guid)
    bringAgentsConversations()
    return render(request, 'soc.html', {
        'chat_history': messages,
        'guid': guid,
        'type': 'orchestrator', 
        'agents': agents
    })

def agent(request, type, guid = None):
    conversation, messages = find_conversation(guid)
    bringAgentsConversations()
    return render(request, 'soc.html', {
        'chat_history': messages,
        'guid': guid,
        'type': type, 
        'agents': agents
    })
    
