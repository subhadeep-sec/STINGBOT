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
                elif self.provider == "puter": 
                    return self._query_puter(prompt, system_prompt)
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
        api_key = config.GEMINI_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Error: Gemini API Key missing. Set GEMINI_KEY in ~/.stingbot2.json or GEMINI_API_KEY env var."
            
        model = self.model if "gemini" in self.model else "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
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

    def _query_openai(self, prompt, system_prompt):
        """Query OpenAI API (GPT-4, GPT-3.5-turbo, etc.)."""
        if not config.OPENAI_KEY:
            return "Error: OpenAI API Key missing in config (~/.stingbot2.json)."
        
        url = "https://api.openai.com/v1/chat/completions"
        model = self.model if "gpt" in self.model else "gpt-4o-mini"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.OPENAI_KEY}'
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2048,
            "temperature": 0.7
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                res = requests.post(url, json=payload, headers=headers, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    return data['choices'][0]['message']['content']
                if res.status_code == 429:
                    wait = (attempt + 1) * 5
                    time.sleep(wait)
                    continue
                return f"OpenAI API Error ({res.status_code}): {res.text[:200]}"
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return f"OpenAI Connection Failed: {str(e)}"
        
        return "OpenAI Error: Max retries exceeded (Rate Limit)."

    def _query_anthropic(self, prompt, system_prompt):
        """Query Anthropic Claude API."""
        if not config.ANTHROPIC_KEY:
            return "Error: Anthropic API Key missing in config (~/.stingbot2.json)."
        
        url = "https://api.anthropic.com/v1/messages"
        model = self.model if "claude" in self.model else "claude-3-5-sonnet-20241022"
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': config.ANTHROPIC_KEY,
            'anthropic-version': '2023-06-01'
        }
        payload = {
            "model": model,
            "max_tokens": 2048,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                res = requests.post(url, json=payload, headers=headers, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    return data['content'][0]['text']
                if res.status_code == 429:
                    wait = (attempt + 1) * 5
                    time.sleep(wait)
                    continue
                return f"Anthropic API Error ({res.status_code}): {res.text[:200]}"
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return f"Anthropic Connection Failed: {str(e)}"
        
        return "Anthropic Error: Max retries exceeded (Rate Limit)."

    def _query_puter(self, prompt, system_prompt):
        """Query Puter.com AI API - Free access to GPT, Claude, Gemini and 500+ models."""
        if not config.PUTER_API_KEY:
            return "Error: Puter API Key missing in config (~/.stingbot2.json). Get one at https://puter.com"
        
        url = "https://api.puter.com/drivers/call"
        
        # Model mapping for Puter - supports gpt-5-nano, claude-sonnet-4, gemini-2.5-flash-lite, etc.
        model = self.model
        if not any(x in model.lower() for x in ["gpt", "claude", "gemini", "mistral", "llama"]):
            model = "gpt-4o-mini"  # Default to a fast, capable model
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.PUTER_API_KEY}'
        }
        
        payload = {
            "interface": "puter-chat-completion",
            "driver": "ai-chat",
            "method": "complete",
            "args": {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "model": model
            }
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                res = requests.post(url, json=payload, headers=headers, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    # Handle different response formats from Puter API
                    if isinstance(data, dict):
                        if 'message' in data and 'content' in data['message']:
                            return data['message']['content']
                        elif 'result' in data:
                            result = data['result']
                            if isinstance(result, dict) and 'message' in result:
                                return result['message'].get('content', str(result))
                            return str(result)
                        elif 'text' in data:
                            return data['text']
                        elif 'content' in data:
                            return data['content']
                    return str(data)
                if res.status_code == 429:
                    wait = (attempt + 1) * 5
                    time.sleep(wait)
                    continue
                if res.status_code == 401:
                    return "Puter Auth Error: Invalid API key. Get one at https://puter.com"
                return f"Puter API Error ({res.status_code}): {res.text[:200]}"
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return f"Puter Connection Failed: {str(e)}"
        
        return "Puter Error: Max retries exceeded (Rate Limit)."
