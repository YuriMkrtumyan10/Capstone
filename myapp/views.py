from django.shortcuts import render
from openai import OpenAI
from django.conf import settings
import os
from .helpers import format_as_gpt_print
from myapp.models import Conversation, Message

# , parameter = ''
def soc(request, guid = None):

    if guid is None:
        conversation = None
        messages = []
    else:
        conversation = Conversation.objects.filter(guid=guid)[0]
         # load data
        messages = Message.objects.filter(conversation__guid=conversation.guid)
    print(messages)
    print('------------')
   
    return render(request, 'soc.html', {'chat_history': messages, 'guid': guid, 'type': ''})



def send_message(request):
    user_input = request.POST['user_input']
    type = request.POST['type']
    # session_index = 'chat_history'
    guid = request.POST['guid']

    if not(guid):
        conversation = Conversation(
            title='New Chat'
        )
        conversation.save()
    else:
        conversation = Conversation.objects.filter(guid=guid)[0]

    # load data
    messages_in_conversation = Message.objects.filter(conversation__guid=conversation.guid)


    # Call ChatGPT to get bot response
    client = OpenAI(
        api_key='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',
    )

    messages = []
    for msg in messages_in_conversation:
        messages.append({"role": "user", "content": msg['question']})
        messages.append({"role": "bot", "content": msg['answer']})

    messages.append({"role": "user", "content": user_input})
    
    if type:
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

    messages.append({"role": "user", "content": bot_response})
    
    last_message = Message()
    last_message.conversation = conversation.guid
    last_message.question = user_input
    last_message.answer = bot_response
    last_message.save()
    messages_in_conversation.append(last_message)
    
    return render(request, 'layouts/chatbox.html', {
        'chat_history': messages_in_conversation,
        'guid': conversation.guid
    })
