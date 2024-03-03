from django.shortcuts import render
from openai import OpenAI
from django.conf import settings
import os


def soc(request, parameter = None):
    if parameter is None:
        chat_history = request.session.get('chat_history', [])
    else:
        chat_history = request.session.get('chat_history_' + parameter, [])

    return render(request, 'soc.html', {'chat_history': chat_history, 'type': parameter})

def send_message(request):
    user_input = request.POST['user_input']
    type = request.POST['type']
    chat_history = request.session.get('chat_history', [])
    chat_history.append({'user': user_input, 'bot': ''})  # Add user input to chat history
    request.session['chat_history'] = chat_history

    # Call ChatGPT to get bot response
    client = OpenAI(
        api_key='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',
    )
    messages = [{"role": "user", "content": msg['user']} for msg in chat_history]

    if (type):
        file_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'source', 'analyze_threat_report', 'system.md')
        with open(file_path, 'r') as file:
            pattern = file.read()
        print(pattern)
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

    chat_history[-1]['bot'] = bot_response  # Update last entry in chat history with bot response
    request.session['chat_history'] = chat_history
    return render(request, 'layouts/chatbox.html', {'chat_history': chat_history})
