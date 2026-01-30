import os
import json

class Settings:
    def __init__(self):
        self.PROJECT_NAME = "Stingbot"
        self.VERSION = "1.0"
        self.SAFETY_MODE = True
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.LOG_DIR = os.path.join(self.BASE_DIR, "data", "logs")
        
        # User Config
        self.USER_ALIAS = "Operator"
        self.BOT_NAME = "Sting"
        
        # AI Config
        self.LLM_PROVIDER = "ollama" # ollama, openai, anthropic, gemini, mock
        self.LLM_MODEL = "llama3.2"
        self.OPENAI_KEY = ""
        self.ANTHROPIC_KEY = ""
        self.GEMINI_KEY = ""
        
        # Voice Config
        self.VOICE_ENABLED = False
        
        self.config_path = os.path.expanduser("~/.stingbot2.json")
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    self.__dict__.update(data)
            except Exception as e:
                print(f"[!] Error loading config: {e}")

    def save(self):
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and not callable(v)}
        try:
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[!] Error saving config: {e}")

config = Settings()
