from django.shortcuts import render
from openai import OpenAI
from ..helpers.conversation import load_conversation, load_messages, update_conversation
from ..helpers.gpt import chatgpt_query
from ..helpers.pdf import handlePDF, load_pdf

def send_message(request):
    pdf_name = None
    user_input = request.POST['user_input']
    type = request.POST['type']
    guid = request.POST.get('guid', None)
    default_title = user_input
    conversation = load_conversation(guid, default_title, type)
    messages_in_conversation, messages = load_messages(conversation, user_input, type)

    if 'file_upload' in request.FILES:
        file = request.FILES['file_upload']
        images_count, pdf_name = handlePDF(file)
        messages = load_pdf(messages, pdf_name)

    response = chatgpt_query(messages)
    messages_in_conversation = update_conversation(conversation, messages_in_conversation, messages, user_input, response, pdf_name)
    
    return render(request, 'layouts/chatbox.html', {
        'chat_history': messages_in_conversation,
        'guid': conversation.guid
    })
    