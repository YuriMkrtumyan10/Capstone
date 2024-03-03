import requests
from django.http import JsonResponse

class OpenAIChatGPT:
    def __init__(self, api_key):
        self.api_key = "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"
        self.endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"

    def query(self, prompt, max_tokens=150):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        response = requests.post(self.endpoint, headers=headers, json=data)
        return response.json()
    
    def get_available_models(self):
        # The URL for the OpenAI API models endpoint
        url = "https://api.openai.com/v1/models"

        # The headers for the API request, including your API key for authorization
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        # Sending a GET request to the API
        response = requests.get(url, headers=headers)

        # Checking if the request was successful
        if response.status_code == 200:
            # If successful, return the JSON response containing available models
            return JsonResponse(response.json())
        else:
            # If unsuccessful, return an error message
            return JsonResponse({"error": "Failed to get response from the API"}, status=response.status_code)    
