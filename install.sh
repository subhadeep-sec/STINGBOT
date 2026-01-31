#!/bin/bash

# ============================================
# STINGBOT v2.0 Installation Script
# Neural Security Engine Deployment
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art Banner
print_banner() {
    echo -e "${RED}"
    cat << 'EOF'
              ___
           .-'     '-.
          /  _     _  \
         |  / \   / \  |
         | |   \ /   | |
          \ \_  V  _/ /
           '-._   _.-'
              /  |  \
             /   |   \
            |   |   |
            |  / \  |
             \_/   \_/
              |  .  |
               \ . /
                \_/
                 o

    ╔═══════════════════════════════════════╗
    ║     STINGBOT v2.0 INSTALLER           ║
    ║     Neural Security Engine            ║
    ╚═══════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✘]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. Some features may behave differently."
    fi
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if grep -qi "kali" /etc/os-release 2>/dev/null; then
            OS="kali"
        elif grep -qi "ubuntu\|debian" /etc/os-release 2>/dev/null; then
            OS="debian"
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    log_info "Detected OS: $OS"
}

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        if [[ $(echo "$PYTHON_VERSION >= 3.10" | bc -l) -eq 1 ]]; then
            log_success "Python $PYTHON_VERSION found"
            return 0
        fi
    fi
    log_error "Python 3.10+ required but not found"
    return 1
}

# Check Node.js version
check_node() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
        if [[ $NODE_VERSION -ge 18 ]]; then
            log_success "Node.js v$(node -v | cut -d'v' -f2) found"
            return 0
        fi
    fi
    log_warning "Node.js 18+ recommended for web dashboard"
    return 1
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    # Create virtual environment (optional but recommended)
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv 2>/dev/null || true
    fi
    
    # Fix for low /tmp space (common in cloud/VMs)
    mkdir -p tmp_install
    export TMPDIR=$(pwd)/tmp_install
    
    # Install main requirements
    pip3 install --quiet rich textual requests psutil colorama 2>/dev/null || pip install rich textual requests psutil colorama
    
    # Install python-brain requirements (Heavy ML libs)
    if [[ -f "agents/python-brain/requirements.txt" ]]; then
        log_info "Installing Neural Engine dependencies (This may take a while)..."
        if pip3 install -r agents/python-brain/requirements.txt 2>/dev/null; then
             log_success "Neural Engine dependencies installed"
        else
             log_warning "Could not install full Neural Engine dependencies (likely disk space/network)."
             log_warning "STINGBOT will run in 'Lite Mode' (Basic Autonomy)."
        fi
    fi
    
    # Cleanup
    rm -rf tmp_install
    
    log_success "Python dependencies setup complete"
}

# Install Node.js dependencies
install_node_deps() {
    log_info "Installing Node.js dependencies..."
    
    # Gateway dependencies
    if [[ -f "gateway/package.json" ]]; then
        cd gateway
        npm install --silent 2>/dev/null || npm install
        cd ..
    fi
    
    # Client dependencies (if exists)
    if [[ -f "client/package.json" ]]; then
        cd client
        npm install --silent 2>/dev/null || npm install
        cd ..
    fi
    
    log_success "Node.js dependencies installed"
}

# Setup configuration
setup_config() {
    CONFIG_FILE="$HOME/.stingbot2.json"
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log_info "Creating default configuration..."
        cat > "$CONFIG_FILE" << 'EOF'
{
    "PROJECT_NAME": "Stingbot",
    "VERSION": "2.0",
    "SAFETY_MODE": true,
    "USER_ALIAS": "Operator",
    "BOT_NAME": "Sting",
    "LLM_PROVIDER": "ollama",
    "LLM_MODEL": "qwen2.5:1.5b",
    "PUTER_API_KEY": "",
    "OPENAI_KEY": "",
    "ANTHROPIC_KEY": "",
    "GEMINI_KEY": "",
    "VOICE_ENABLED": false
}
EOF
        log_success "Configuration created at $CONFIG_FILE"
        log_info "Fast local LLM configured. Install model with: ollama pull qwen2.5:1.5b"
    else
        log_info "Configuration already exists at $CONFIG_FILE"
    fi
}

# Create global command
create_global_command() {
    log_info "Setting up global 'stingbot' command..."
    
    INSTALL_DIR=$(pwd)
    STINGBOT_SCRIPT="$HOME/.local/bin/stingbot"
    
    mkdir -p "$HOME/.local/bin"
    
    cat > "$STINGBOT_SCRIPT" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 stingbot.py "\$@"
EOF
    
    chmod +x "$STINGBOT_SCRIPT"
    
    # Add to PATH if not already
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
        log_warning "Added ~/.local/bin to PATH. Restart your shell or run: source ~/.bashrc"
    fi
    
    log_success "Global command created. Use 'stingbot' from anywhere."
}

# Check for Ollama
check_ollama() {
    if command -v ollama &> /dev/null; then
        log_success "Ollama found"
        
        # Check if model is available
        if ollama list 2>/dev/null | grep -q "llama3"; then
            log_success "Ollama model available"
        else
            log_warning "No models found. Run: ollama pull llama3.2"
        fi
    else
        log_warning "Ollama not found. Install from: https://ollama.ai"
        log_info "Or configure a cloud LLM provider in ~/.stingbot2.json"
    fi
}

# Create necessary directories
create_directories() {
    mkdir -p logs
    mkdir -p agents/python-brain/data/logs
    log_success "Directories created"
}

# Run health check
run_health_check() {
    log_info "Running system health check..."
    
    echo ""
    echo -e "${PURPLE}┌─────────────────────────────────────────────┐${NC}"
    echo -e "${PURPLE}│           STINGBOT HEALTH CHECK             │${NC}"
    echo -e "${PURPLE}└─────────────────────────────────────────────┘${NC}"
    
    # Python
    if check_python; then
        echo -e "  Python:     ${GREEN}✓ OK${NC}"
    else
        echo -e "  Python:     ${RED}✘ MISSING${NC}"
    fi
    
    # Node.js
    if check_node; then
        echo -e "  Node.js:    ${GREEN}✓ OK${NC}"
    else
        echo -e "  Node.js:    ${YELLOW}! Optional${NC}"
    fi
    
    # Ollama
    if command -v ollama &> /dev/null; then
        echo -e "  Ollama:     ${GREEN}✓ OK${NC}"
    else
        echo -e "  Ollama:     ${YELLOW}! Not found${NC}"
    fi
    
    # Config
    if [[ -f "$HOME/.stingbot2.json" ]]; then
        echo -e "  Config:     ${GREEN}✓ OK${NC}"
    else
        echo -e "  Config:     ${RED}✘ MISSING${NC}"
    fi
    
    # Security tools
    for tool in nmap sqlmap nikto; do
        if command -v $tool &> /dev/null; then
            echo -e "  $tool:$(printf '%*s' $((10-${#tool})) '')${GREEN}✓ OK${NC}"
        else
            echo -e "  $tool:$(printf '%*s' $((10-${#tool})) '')${YELLOW}! Not found${NC}"
        fi
    done
    
    echo ""
}

# Main installation
main() {
    print_banner
    
    echo -e "${CYAN}Starting STINGBOT installation...${NC}\n"
    
    check_root
    detect_os
    
    echo ""
    log_info "Checking prerequisites..."
    check_python || exit 1
    check_node || true
    
    echo ""
    create_directories
    install_python_deps
    install_node_deps
    setup_config
    
    # Run interactive model setup
    log_info "Launching Neural Engine Configuration..."
    python3 scripts/setup_model.py || log_warning "Model setup skipped or failed."
    
    create_global_command
    
    echo ""
    check_ollama
    
    echo ""
    run_health_check
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║          STINGBOT INSTALLATION COMPLETE!              ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${CYAN}Quick Start:${NC}"
    echo -e "    ${YELLOW}stingbot${NC}                    - Interactive mode"
    echo -e "    ${YELLOW}stingbot \"your objective\"${NC}   - Direct mission"
    echo ""
    echo -e "  ${CYAN}Web Dashboard:${NC}"
    echo -e "    ${YELLOW}cd gateway && npm start${NC}     - Start gateway"
    echo -e "    ${YELLOW}cd client && npm run dev${NC}    - Start dashboard"
    echo ""
    echo -e "  ${CYAN}Configuration:${NC}"
    echo -e "    ${YELLOW}~/.stingbot2.json${NC}           - Edit settings"
    echo ""
    echo -e "${PURPLE}Stay Lethal. 🦂${NC}"
}

# Run main
main "$@"
