from ..constants import agents
from myapp.models import Conversation, Message
from django.shortcuts import redirect
import os
from django.conf import settings
from ..helpers.pdf import load_pdf

def bringAgentsConversations():
    for i, agent_data in enumerate(agents):
        agents[i]['conversations'] = Conversation.objects.filter(type=agent_data['type']).order_by('-created_at')

def find_conversation(guid):
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

def load_conversation(guid, default_title, type):
    if not(guid):
        conversation = Conversation(
            title=default_title,
            type=type
        )
        conversation.save()
    else:
        conversation = Conversation.objects.filter(guid=guid).first()
        if not conversation:
            conversation = Conversation(title=default_title, type=type)
            conversation.save()
    return conversation

def load_messages(conversation, user_input, type):
    messages_in_conversation = Message.objects.filter(conversation__guid=conversation.guid)

    messages = []
    for msg in messages_in_conversation:
        messages.append({"role": "user", "content": msg.question})
        messages.append({"role": "assistant", "content": msg.answer})
        messages = load_pdf(messages, msg.file_id)

    messages.append({"role": "user", "content": user_input})
    
    if type and type != 'main':
        file_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'source', type, 'system.md')

        with open(file_path, 'r') as file:
            pattern = file.read()
        messages.insert(
            0,
            {"role": "system", "content": pattern}
        )
    return messages_in_conversation, messages

def update_conversation(conversation, messages_in_conversation, messages, user_input, bot_response, file_id):

    messages.append({"role": "bot", "content": bot_response})

    last_message = Message.objects.create(
        conversation=conversation,
        question=user_input,
        answer=bot_response,
        file_id=file_id
    )
    messages_in_conversation = messages_in_conversation | Message.objects.filter(pk=last_message.pk)

    return messages_in_conversation