import requests
import json

path = "/home/kali/.stingbot2.json"
with open(path, "r") as f:
    config = json.load(f)

api_key = config["GEMINI_KEY"]
model = config["LLM_MODEL"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

headers = {'Content-Type': 'application/json'}
payload = {
    "contents": [{
        "parts": [{"text": "Hello, who are you?"}]
    }]
}

try:
    res = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")
except Exception as e:
    print(f"Error: {e}")
