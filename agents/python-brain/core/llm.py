import requests
import json
import time
from config.settings import config

class LLMAdapter:
    """Universal Adapter for LLM backends (Ollama, OpenAI, Mock)."""
    
    def __init__(self):
        self.provider = config.LLM_PROVIDER
        self.model = config.LLM_MODEL
        self.base_url = "http://localhost:11434"

    def query(self, prompt, system_prompt="You are STINGBOT v2 [GENERALIST NEURAL ENGINE]. You handle cybersecurity tasks and daily productivity with lethal efficiency. Be precise, fast, and helpful.", max_retries=3):
        """Query the configured LLM provider with automatic retry and fallback."""
        for attempt in range(max_retries):
            try:
                if self.provider == "ollama": 
                    return self._query_ollama(prompt, system_prompt)
                elif self.provider == "openai": 
                    return self._query_openai(prompt, system_prompt)
                elif self.provider == "gemini": 
                    return self._query_gemini(prompt, system_prompt)
                elif self.provider == "anthropic": 
                    return self._query_anthropic(prompt, system_prompt)
                else: 
                    return self._query_mock(prompt)
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    # Final fallback: return a safe error message
                    return f"[NEURAL ENGINE ERROR] Unable to process request after {max_retries} attempts. Error: {str(e)[:100]}"

    def _query_mock(self, prompt):
        """Offline mock responses for testing."""
        prompt = prompt.lower()
        if "scan" in prompt: return "scan localhost"
        if "hello" in prompt: return "talk Hello Operator."
        return "I am in Mock Mode. No LLM connected."

    def _query_ollama(self, prompt, system_prompt):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        try:
            res = requests.post(url, json=payload, timeout=180)
            if res.status_code == 200:
                return res.json().get("response", "Error: Empty response.")
            return f"Ollama Error: {res.text}"
        except Exception as e:
            return f"Connection Failed: {str(e)}"

    def _query_gemini(self, prompt, system_prompt):
        """Query Google Gemini API with exponential backoff for 429s."""
        if not config.GEMINI_KEY:
            return "Error: Gemini API Key missing in config (~/.stingbot2.json)."
            
        model = self.model if "gemini" in self.model else "gemini-flash-latest"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={config.GEMINI_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"System: {system_prompt}\nUser: {prompt}"}]
            }]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                res = requests.post(url, json=payload, headers=headers, timeout=30)
                if res.status_code == 200:
                    data = res.json()
                    return data['candidates'][0]['content']['parts'][0]['text']
                if res.status_code == 429:
                    # Exponential backoff: 5s, 10s, 20s
                    wait = (attempt + 1) * 5
                    time.sleep(wait)
                    continue
                return f"Gemini API Error: {res.text}"
            except Exception as e:
                # On connection error, try again once
                if attempt < 1: 
                    time.sleep(2)
                    continue
                return f"Gemini Connection Failed: {str(e)}"
        
        return "Gemini Error: Max retries exceeded (Quota/Rate Limit)."
