#!/bin/bash
# 🦂 Stingbot Autonomous Installer 
# "Pairing codes exist because even bots believe in consent—and good security hygiene."

echo ""
echo "  🦂 Stingbot Neural Installer"
echo "  Pairing codes exist because even bots believe in consent—and good security hygiene."
echo ""

# 1. Environment Check
OS_TYPE=$(uname -s | tr '[:upper:]' '[:lower:]')
echo "✓ Detected: $OS_TYPE"

if [ -d ".git" ]; then
    echo "✓ Git repository detected"
else
    echo "→ Initializing environment..."
fi

# 2. Dependency Check (Mock/Simplified)
if command -v python3 &> /dev/null; then
    PY_VER=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python $PY_VER found"
else
    echo "✘ Python 3 not found. Please install python3."
    exit 1
fi

# 3. Installation
echo "→ Installing Stingbot Core 2.0.4..."
chmod +x setup.sh main.py
./setup.sh > /dev/null 2>&1

# 4. Global Link
AL_LINE="alias stingbot=\"python3 $(pwd)/main.py\""
if ! grep -q "$AL_LINE" ~/.zshrc; then
    echo "$AL_LINE" >> ~/.zshrc
    echo "✓ Global alias established in ~/.zshrc"
fi

echo ""
echo "✓ Installation Complete."
echo "→ Run 'source ~/.zshrc' then 'stingbot' to establish a neural link."
echo ""
