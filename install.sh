#!/bin/bash
# 🦂 Stingbot Autonomous One-Line Installer
# "Speed is the only currency in the neural age."

REPO_URL="https://github.com/subhadeep-sec/STINGBOT.git"
INSTALL_DIR="$HOME/STINGBOT"

echo ""
echo "  🦂 STINGBOT GLOBAL DEPLOYMENT"
echo "  --------------------------------"

# 2. Dependency Check
for cmd in git python3 ollama; do
    if ! command -v $cmd &> /dev/null; then
        if [ "$cmd" == "ollama" ]; then
            echo "→ [WIZARD] Ollama not found. Please install it from https://ollama.ai/"
        else
            echo "✘ Error: $cmd is required but not installed."
            exit 1
        fi
    fi
done

# 3. Neural Brain Check
if command -v ollama &> /dev/null; then
    echo "→ Checking Neural Brain (Llama 3.2)..."
    if ! ollama list | grep -q "llama3.2"; then
        echo "→ [WIZARD] Pulling Llama 3.2 engine (this may take a moment)..."
        ollama pull llama3.2
        echo "✓ Neural Brain synchronized."
    else
        echo "✓ Neural Brain ready."
    fi
fi

# 4. Cloning/Syncing
if [ -d "$INSTALL_DIR" ]; then
    echo "✓ Existing assets detected. Synchronizing..."
    cd "$INSTALL_DIR" && git pull || { echo "✘ Update failed."; exit 1; }
else
    echo "→ Provisioning Neural Assets from GitHub..."
    git clone "$REPO_URL" "$INSTALL_DIR" || { echo "✘ Clone failed."; exit 1; }
fi

cd "$INSTALL_DIR"

# 3. Environment Preparation
echo "→ Hardening core binaries..."
chmod +x setup.sh main.py

echo "→ Resolving neural dependencies..."
python3 -m pip install -r requirements.txt --quiet > /dev/null 2>&1

# 4. Alias Establishment
echo "→ Establishing permanent Neural Link (Alias)..."
AL_LINE="alias stingbot=\"python3 $INSTALL_DIR/main.py\""
SHELL_CONFIG="$HOME/.zshrc"
if [ ! -f "$SHELL_CONFIG" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if ! grep -q "alias stingbot=" "$SHELL_CONFIG"; then
    echo "" >> "$SHELL_CONFIG"
    echo "# Stingbot Neural Link" >> "$SHELL_CONFIG"
    echo "$AL_LINE" >> "$SHELL_CONFIG"
    echo "✓ Stingbot added to $SHELL_CONFIG"
fi

echo ""
echo "✓ DEPLOYMENT SUCCESSFUL."
echo "→ Load your shell: source $SHELL_CONFIG"
echo "→ Launch the engine: stingbot"
echo ""
