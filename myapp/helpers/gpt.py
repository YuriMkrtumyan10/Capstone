from openai import OpenAI

def chatgpt_query(messages):
  
    client = OpenAI(
        api_key='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',
    )
    completion = client.chat.completions.create(
        # model="gpt-4-turbo-preview",
        # model="gpt-4-1106-vision-preview",
        # messages=messages
        
        model="gpt-4-vision-preview",
        messages=messages
    )
    return completion.choices[0].message.content.strip()

