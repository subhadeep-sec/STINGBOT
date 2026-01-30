#!/bin/bash
# 🦂 Stingbot Autonomous One-Line Installer
# "Speed is the only currency in the neural age."

REPO_URL="https://github.com/subhadeep-sec/STINGBOT.git"
INSTALL_DIR="$HOME/STINGBOT"

echo ""
echo "          .                                                      "
echo "         .NM.          🦂 STINGBOT NEURAL GATEWAY               "
echo "        .NMMM.         ---------------------------               "
echo "      .NMMMMMM.                                                  "
echo "    .NMMMMMMMMMM.      [ VERSION 1.0 // PRODUCTION ]             "
echo "  .NMMMMMMMMMMMMMM.    [ STATUS: INITIALIZING ]                  "
echo "   '''''''''''''''                                               "
echo ""

# 2. Dependency Check
for cmd in git python3 ollama; do
    if ! command -v $cmd &> /dev/null; then
        if [ "$cmd" == "ollama" ]; then
            echo "→ [WIZARD] Ollama not found. Required for local AI reasoning."
        else
            echo "✘ Error: $cmd is required but not installed."
            exit 1
        fi
    fi
done

# 3. Neural Brain Check
if command -v ollama &> /dev/null; then
    echo "→ Synchronizing Neural Brain (Llama 3.2)..."
    if ! ollama list | grep -q "llama3.2"; then
        echo "→ [WIZARD] Building local logic gates (Pulling Llama 3.2)..."
        ollama pull llama3.2 > /dev/null 2>&1
        echo "✓ Neural Brain synchronized."
    else
        echo "✓ Neural Brain active."
    fi
fi

# 4. Cloning/Syncing
if [ -d "$INSTALL_DIR" ]; then
    echo "✓ Global assets detected. Synchronizing..."
    cd "$INSTALL_DIR" && git pull --quiet
else
    echo "→ Provisioning Neural Assets..."
    git clone --quiet "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 5. Build & Environment
echo "→ Resolving neural dependencies..."
python3 -m pip install -r requirements.txt --quiet > /dev/null 2>&1
chmod +x setup.sh main.py

# 6. Global Link (npx/npm style fallback)
AL_LINE="alias stingbot=\"python3 $INSTALL_DIR/main.py\""
SHELL_CONFIG="$HOME/.zshrc"
if [ ! -f "$SHELL_CONFIG" ]; then SHELL_CONFIG="$HOME/.bashrc"; fi

if ! grep -q "alias stingbot=" "$SHELL_CONFIG"; then
    echo "" >> "$SHELL_CONFIG"
    echo "# Stingbot Neural Link" >> "$SHELL_CONFIG"
    echo "$AL_LINE" >> "$SHELL_CONFIG"
    echo "✓ Alias established in $SHELL_CONFIG"
fi

echo ""
echo "✓ ONBOARDING COMPLETE."
echo "→ Launch the engine: stingbot"
echo "→ Or use npx: npx stingbot-ai onboard"
echo ""
