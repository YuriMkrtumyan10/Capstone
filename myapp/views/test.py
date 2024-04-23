from django.shortcuts import render
from ..helpers.gpt import chatgpt_query

def test(request):
    message = [
        {"role": "user", "content": 'Who is the first president of US? tell me about him in maximum of 20 tokens'},
        {"role": "assistant", "content": 'George Washington, a Revolutionary War hero, served as the first president of the United States with honor and distinction.'}
    ]

    response = chatgpt_query(message)
    response_tokens = len(response.split())

    return render(request, 'test.html', {
        "text": response,
        "text2": response_tokens
    })
    