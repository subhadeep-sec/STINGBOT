#!/usr/bin/env python3
import json
import os
import sys

CONFIG_PATH = os.path.expanduser("~/.stingbot2.json")

def setup_model():
    print("\n╭──────────────────────────────────────────────────────────────╮")
    print("│             STINGBOT MULTI-MODEL CONFIGURATION               │")
    print("╰──────────────────────────────────────────────────────────────╯")
    print("Select your preferred Neural Engine Provider:")
    print("1. Google Gemini  (Fast, Efficient, 1M context) [Rec: gemini-1.5-flash]")
    print("2. OpenAI         (GPT-4o, GPT-3.5-Turbo)       [Rec: gpt-4o-mini]")
    print("3. Anthropic      (Claude 3.5 Sonnet, Haiku)    [Rec: claude-3-5-sonnet]")
    print("4. Ollama         (Local Llama 3, Phi-3, Mistral) [Rec: llama3.2]")
    print("5. Puter.com      (Free Access to all models)   [Rec: gpt-4o-mini]")
    
    choice = input("\nEnter choice [1-5]: ").strip()
    
    provider = "ollama" # Default
    model = "llama3.2"
    api_key_name = ""
    api_key_val = ""

    if choice == "1":
        provider = "gemini"
        model = input("Enter Model Name [default: gemini-1.5-flash]: ").strip() or "gemini-1.5-flash"
        api_key_name = "GEMINI_KEY"
        api_key_val = input("Enter Google Gemini API Key: ").strip()
    elif choice == "2":
        provider = "openai"
        model = input("Enter Model Name [default: gpt-4o-mini]: ").strip() or "gpt-4o-mini"
        api_key_name = "OPENAI_KEY"
        api_key_val = input("Enter OpenAI API Key: ").strip()
    elif choice == "3":
        provider = "anthropic"
        model = input("Enter Model Name [default: claude-3-5-sonnet-20241022]: ").strip() or "claude-3-5-sonnet-20241022"
        api_key_name = "ANTHROPIC_KEY"
        api_key_val = input("Enter Anthropic API Key: ").strip()
    elif choice == "4":
        provider = "ollama"
        model = input("Enter Model Name [default: llama3.2]: ").strip() or "llama3.2"
        print("Note: Ensure Ollama is running (systemctl start ollama)")
    elif choice == "5":
        provider = "puter"
        model = input("Enter Model to use via Puter [default: gpt-4o-mini]: ").strip() or "gpt-4o-mini"
        api_key_name = "PUTER_API_KEY"
        api_key_val = input("Enter Puter.com API Key: ").strip()
    else:
        print("Invalid choice. Exiting.")
        return

    # Load existing config
    config = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        except:
            pass
            
    # Update config
    config["LLM_PROVIDER"] = provider
    config["LLM_MODEL"] = model
    
    if api_key_name and api_key_val:
        config[api_key_name] = api_key_val
    elif api_key_name and not api_key_val:
        # Check env var as fallback, otherwise warn
        env_key = os.getenv(f"{api_key_name}_API_KEY") or os.getenv(api_key_name)
        if env_key:
            print(f"Using API Key from environment variable: {api_key_name}")
        else:
            print(f"Warning: No API Key provided for {provider}. Ensure it is set in environment.")

    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        print(f"\n[+] Configuration updated successfully at {CONFIG_PATH}")
        print(f"[+] Active Provider: {provider.upper()}")
        print(f"[+] Active Model:    {model}")
        print("\nRestart STINGBOT to apply changes.")
    except Exception as e:
        print(f"[-] Error saving config: {e}")

if __name__ == "__main__":
    setup_model()
