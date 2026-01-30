#!/bin/bash
# 🦂 Stingbot Autonomous One-Line Installer
# "Speed is the only currency in the neural age."

REPO_URL="https://github.com/subhadeep-sec/STINGBOT.git"
INSTALL_DIR="$HOME/STINGBOT"

echo ""
echo "  🦂 STINGBOT GLOBAL DEPLOYMENT"
echo "  --------------------------------"

# 1. Verification
for cmd in git python3; do
    if ! command -v $cmd &> /dev/null; then
        echo "✘ Error: $cmd is required but not installed."
        exit 1
    fi
done

# 2. Cloning/Syncing
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
