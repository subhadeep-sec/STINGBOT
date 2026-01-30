# 🦂 Stingbot — Neural Security Engine

<p align="center">
    <img src="docs/assets/logo.png" alt="Stingbot" width="500">
</p>

<p align="center">
  <strong>NEURIZE! EXPLOIT! SECURE!</strong>
</p>

<p align="center">
  <a href="https://github.com/subhadeep-sec/STINGBOT/actions"><img src="https://img.shields.io/github/actions/workflow/status/subhadeep-sec/STINGBOT/ci.yml?branch=main&style=for-the-badge" alt="CI status"></a>
  <a href="https://github.com/subhadeep-sec/STINGBOT/releases"><img src="https://img.shields.io/github/v/release/subhadeep-sec/STINGBOT?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
</p>

# STING: Autonomous Multi-Agent Platform 🦂

**STING** (formerly Stingbot) is a premium, AI-powered Multi-Agent System (MAS) designed for autonomous offensive security missions. Built for zero-cost local execution, it leverages a Supervisor-Agent architecture to decompose complex goals into actionable intelligence.

## 🚀 One-Line Installation

Deploy **STING** to your system with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/subhadeep-sec/STINGBOT/main/install.sh | bash
```

> [!IMPORTANT]
> **Requirements**: Kali Linux, macOS, or WSL2 with Python 3.10+ and Node.js 20+

**What happens during installation:**
1. 🔐 Security clearance and neural operating agreement
2. 🧠 LLM provider selection (Ollama, OpenAI, Anthropic, or Gemini)
3. 🔧 Automatic dependency installation and environment setup
4. 🦂 Global `stingbot` command configuration
5. 📊 Diagnostic health check and verification

**Launch STING:**
```bash
stingbot                    # Interactive mission control
stingbot "your objective"   # Direct mission mode
```

---

### 🧠 Models (Neural Brain)

Stingbot is designed for high-performance local inference.
- **Ollama (Recommended)**: Run `llama3.2` or `mistral` locally for maximum privacy.
- **Failover**: Supports fallback to cloud models if local resources are constrained.



## 🎮 Usage

Once installed, Stingbot is ready for action. To start the platform:

```bash
stingbot
```

> **Note**: The installation script automatically runs the Neural Health Check and Interactive Onboarding. If you need to re-run them later:
> - `stingbot doctor` - Run system diagnostics
> - `stingbot onboard` - Re-configure the platform

## 🏗️ Architecture (Clawbot Fidelity)

```
Web Dashboard (React) <─── Socket.io ───> Neural Gateway (Node.js)
                                            │
                                            ▼
                                     Python Brain (RPC)
                                            │
                                  ┌─────────┴─────────┐
                                  ▼                   ▼
                           Security Tools       Local LLM (Ollama)
```

## 🛠️ Components
- **`gateway/`**: The Node.js WebSocket control plane.
- **`client/`**: The React/Vite premium web interface (Under development).
- **`agents/python-brain/`**: The core offensive security engine (Python).

## 🔒 Security defaults
Stingbot is a professional tool. Run `node gateway/bin/onboard.js doctor` to surface any insecure configurations.

---
Built with intensity. **Stay Lethal.** 🦂
