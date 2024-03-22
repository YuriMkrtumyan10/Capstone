from django.http import JsonResponse
from django.shortcuts import render, redirect
from openai import OpenAI
from django.conf import settings
import os
from django.views.decorators.http import require_POST
from myapp.models import Conversation, Message

agents = [
    {'name': 'bot', 'type': 'main', 'image': None},
    {'name': 'incident-responder', 'type': 'incident-responder', 'image': 'agent1'},
    {'name': 'network-engineer', 'type': 'network-engineer', 'image': 'agent2'},
    {'name': 'soc-analyst', 'type': 'soc-analyst', 'image': 'agent3'},
]

# , parameter = ''
def main(request, guid = None):
    conversation, messages = _find_conversation(guid)
    bringAgentsConversations()
    return render(request, 'soc.html', {
        'chat_history': messages,
        'guid': guid,
        'type': 'main', 
        'agents': agents
    })

def agent(request, type, guid = None):
    conversation, messages = _find_conversation(guid)

    bringAgentsConversations()
    return render(request, 'soc.html', {
        'chat_history': messages,
        'guid': guid,
        'type': type, 
        'agents': agents
    })
    

def bringAgentsConversations():
    for i, agent_data in enumerate(agents):
        agents[i]['conversations'] = Conversation.objects.filter(type=agent_data['type']).order_by('-created_at')

@require_POST
def delete_conversation(request, guid):
    if request.method == 'POST':
        response_data = {'status': 'failed', 'message': 'Invalid request'}
        try:
            conversation = Conversation.objects.get(guid=guid)
            conversation.delete()
            response_data = {'status': 'success', 'message': 'Conversation deleted successfully'}
        except Conversation.DoesNotExist:
            response_data = {'status': 'failed', 'message': 'Conversation not found'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})
    
    
def _find_conversation(guid):
    if guid is None:
        conversation = None
        messages = []
    else:
        conversation = Conversation.objects.filter(guid=guid)[0]
        if not(conversation):
            return redirect('main')
         # load data
        messages = Message.objects.filter(conversation=conversation)

    return conversation, messages

def send_message(request):
    user_input = request.POST['user_input']
    type = request.POST['type']
    # session_index = 'chat_history'
    guid = request.POST.get('guid', None)
    default_title = user_input[:15] + '...'
    if not(guid):
        conversation = Conversation(
            title=default_title,
            type=type
        )
        conversation.save()
    else:
        conversation = Conversation.objects.filter(guid=guid).first()
        if not conversation:
            # Handle the case where guid is provided but not found in database
            # For example, return an error or create a new conversation
            # This example creates a new conversation
            conversation = Conversation(title=default_title, type=type)
            conversation.save()

    # load data
    messages_in_conversation = Message.objects.filter(conversation__guid=conversation.guid)


    # Call ChatGPT to get bot response
    client = OpenAI(
        api_key='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',
    )

    messages = []
    for msg in messages_in_conversation:
        messages.append({"role": "user", "content": msg.question})
        messages.append({"role": "assistant", "content": msg.answer})

    messages.append({"role": "user", "content": user_input})
    
    if type and type != 'main':
        file_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'source', type, 'system.md')

        with open(file_path, 'r') as file:
            pattern = file.read()
        messages.insert(
            0,
            {"role": "system", "content": pattern}
        )
    

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
        # messages=[
        #     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        # ]
    )

    bot_response = completion.choices[0].message.content.strip()

    messages.append({"role": "bot", "content": bot_response})

    last_message = Message.objects.create(
        conversation=conversation,
        question=user_input,
        answer=bot_response
    )
    messages_in_conversation = messages_in_conversation | Message.objects.filter(pk=last_message.pk)

    return render(request, 'layouts/chatbox.html', {
        'chat_history': messages_in_conversation,
        'guid': conversation.guid
    })
    