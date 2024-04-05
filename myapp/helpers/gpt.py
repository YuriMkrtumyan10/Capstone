from openai import OpenAI

def chatgpt_query(messages):
  
    client = OpenAI(
        api_key='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',
    )
    print(messages)
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages
    )
    return completion.choices[0].message.content.strip()

