#!/usr/bin/env python3
import json
import os
import sys

CONFIG_PATH = os.path.expanduser("~/.stingbot2.json")

def setup_gemini():
    print("=== STINGBOT Gemini Setup ===")
    print("Switching to Google Gemini (Fast & Efficient)...")
    
    api_key = input("Enter your Gemini API Key (or press Enter if set in env vars): ").strip()
    
    config = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        except:
            print("Warning: Could not read existing config, starting fresh.")
            
    # Update settings
    config["LLM_PROVIDER"] = "gemini"
    config["LLM_MODEL"] = "gemini-1.5-flash"
    
    if api_key:
        config["GEMINI_KEY"] = api_key
        print("API Key saved.")
    else:
        print("No API Key entered. Ensure 'GEMINI_API_KEY' environment variable is set.")
        
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        print(f"\nSuccess! Configuration updated at {CONFIG_PATH}")
        print("STINGBOT will now use Gemini for high-speed autonomous reasoning.")
    except Exception as e:
        print(f"Error saving config: {e}")

if __name__ == "__main__":
    setup_gemini()
