import requests
import json

path = "/home/kali/.stingbot2.json"
with open(path, "r") as f:
    config = json.load(f)

api_key = config["GEMINI_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    res = requests.get(url, timeout=30)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        models = res.json()
        print("Available models:")
        for m in models.get('models', []):
            if 'gemini' in m['name'].lower():
                print(f"- {m['name']}")
    else:
        print(f"Response: {res.text}")
except Exception as e:
    print(f"Error: {e}")
