# DeepSeek severity placeholder
import os
import requests

DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY")

def classify_severity(incident):
    prompt = f"""
Classify severity as one of: CRITICAL, HIGH, MEDIUM, LOW.
Only return the word.

Level: {incident.level}
Message: {incident.message}
"""

    res = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {DEESEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 5
        }
    )
    return res.json()["choices"][0]["message"]["content"].strip()
