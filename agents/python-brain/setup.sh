#!/bin/bash
# Stingbot Component Provisioner
echo "→ Provisioning system dependencies..."
pip3 install -r requirements.txt --quiet
echo "✓ Python dependencies verified."
echo "→ Linkage: stingbot -> $(pwd)/main.py"

