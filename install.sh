#!/bin/bash
# 🦂 Stingbot Autonomous Platform Installer
# "Speed is the only currency in the neural age."

STINGBOT_DIR="$HOME/stingbot"
REPO_URL="https://github.com/subhadeep-sec/STINGBOT.git"

echo -e "\033[1;36m"
echo "              ___"
echo "             /  _\\"
echo "            |  /"
echo "  __________|  |__________"
echo " /                        \\"
echo "|   STINGBOT NEURAL LINK   |"
echo " \\________________________/"
echo "         |  |   |  |"
echo "         |  |   |  |"
echo "         \\  \\___/  /"
echo "          \\_______/"
echo ""
echo "          🦂 STINGBOT 🦂"
echo -e "\033[0m"

# 1. Environment Check
OS_TYPE=$(uname -s | tr '[:upper:]' '[:lower:]')
echo "✓ Detected: $OS_TYPE"

# Check for Node.js (v20+)
NODE_VERSION=$(node -v 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1)
if [ -z "$NODE_VERSION" ] || [ "$NODE_VERSION" -lt 20 ]; then
    echo "✘ Error: Node.js v20+ is required. Found: $NODE_VERSION"
    exit 1
fi
echo "✓ Node.js $(node -v) found"

# 2. Deployment
STING_ROOT="$HOME/sting"

if [ -d "$STING_ROOT" ]; then
    echo "→ STING installation detected. Synchronizing Neural Assets..."
    cd "$STING_ROOT" && git pull --quiet
else
    echo "→ Provisioning STING Neural Assets..."
    git clone --quiet "$REPO_URL" "$STING_ROOT"
fi

cd "$STING_ROOT" || exit 1
echo "✓ STING platform assets synchronized."

# 3. Provisioning
echo "→ Building STING Neural Brain & MAS..."
npm install --quiet > /dev/null 2>&1
python3 -m pip install -r agents/python-brain/requirements.txt --quiet > /dev/null 2>&1

# 4. Premium Setup
python3 scripts/setup_premium.py

# 5. Global Link (Optional/Local)
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$(pwd)/stingbot" "$HOME/.local/bin/stingbot"
    echo "✓ Global command 'stingbot' linked to \$HOME/.local/bin"
    
    # Ensure ~/.local/bin is in PATH
    for rc_file in "$HOME/.zshrc" "$HOME/.bashrc"; do
        if [ -f "$rc_file" ]; then
            grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$rc_file" || \
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc_file"
        fi
    done
fi

echo -e "\n\033[1;32m✓ STINGBOT INSTALLATION SUCCESSFUL\033[0m"
echo "Launch with: stingbot (restart terminal or run: source ~/.zshrc)"
