#!/bin/bash
# 🦂 Stingbot Autonomous Platform Installer
# "Speed is the only currency in the neural age."

STINGBOT_DIR="$HOME/stingbot"
REPO_URL="https://github.com/subhadeep-sec/STINGBOT.git"

echo -e "\033[1;36m"
echo "  🦂 Stingbot Installer"
echo "  \"It's not 'failing,' it's 'discovering new ways to configure the same thing wrong.'\""
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
if [ -d "$STINGBOT_DIR" ]; then
    echo "→ Existing Stingbot installation detected. Synchronizing..."
    cd "$STINGBOT_DIR" && git pull --quiet
else
    echo "→ Provisioning Neural Assets (Installing Stingbot)..."
    git clone --quiet "$REPO_URL" "$STINGBOT_DIR"
fi

cd "$STINGBOT_DIR"
echo "✓ Stingbot platform assets synchronized."

# 3. Provisioning
echo "→ Building Neural Brain & Gateway..."
npm install --quiet > /dev/null 2>&1
python3 -m pip install -r agents/python-brain/requirements.txt --quiet > /dev/null 2>&1

# 4. Launching the Onboarding Doctor
echo "→ Running doctor to migrate settings..."
node gateway/bin/onboard.js --doctor
