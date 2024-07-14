from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def chatgpt_query(messages):
    api_key = os.getenv('OPENAI_API_KEY')

    client = OpenAI(
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        # model="gpt-4-turbo-preview",
        # model="gpt-4-1106-vision-preview",
        # model="gpt-4-vision-preview",
        model="gpt-3.5-turbo",
        messages=messages,
        
    )

    
    return completion.choices[0].message.content.strip()

