import os
import requests

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def generate_response(prompt: str):
    if not OPENAI_KEY:
        return "OpenAI API key not set."

    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)

    try:
        return res.json()["choices"][0]["message"]["content"]
    except:
        return "Error generating text."
