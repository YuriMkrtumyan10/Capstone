from django.shortcuts import render
from openai import OpenAI
from ..helpers.conversation import load_conversation, load_messages, update_conversation
from ..helpers.gpt import chatgpt_query
from ..helpers.pdf import handlePDF, load_pdf
from ..helpers.communication import handle_communication

def send_message(request):
    pdf_name = None
    user_input = request.POST['user_input']
    type = request.POST['type']
    guid = request.POST.get('guid', None)
    default_title = user_input
    conversation = load_conversation(guid, default_title, type)
    messages_in_conversation, messages = load_messages(conversation, user_input, type)
    file_messages = []
    
    if 'file_upload' in request.FILES:
        file = request.FILES['file_upload']
        pdf_name = handlePDF(file)
        file_messages = load_pdf(pdf_name)
        messages = messages + file_messages

    response, agents = handle_communication(file_messages, messages)
    agents.insert(0, type)
    messages_in_conversation = update_conversation(conversation, messages_in_conversation, messages, user_input, response, pdf_name, agents)
    
    return render(request, 'layouts/chatbox.html', {
        'chat_history': messages_in_conversation,
        'guid': conversation.guid
    })
    