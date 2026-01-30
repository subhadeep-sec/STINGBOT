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

**Stingbot** is an *autonomous AI security platform* you run on your own devices.
It leverages advanced LLM reasoning to perform complex security audits, reconnaissance, and exploitation tasks autonomously. It follows a decoupled architecture, separating the **Neural Gateway** (Control Plane) from the **Python Security Brain** (Execution Engine). This allows for a premium Web UI experience combined with the raw power of Python-based offensive tools.

If you want a personal, autonomous security analyst that feels local, fast, and always-on, this is it.

[Website](https://stingbot.ai) · [Docs](https://docs.stingbot.ai) · [Project Wiki](https://github.com/subhadeep-sec/STINGBOT/wiki) · [Getting Started](https://docs.stingbot.ai/start) · [Wizard](https://docs.stingbot.ai/start/wizard)

Preferred setup: run the onboarding wizard (`npx stingbot-ai onboard`). It walks through the neural brain setup, security tool parity, and pairing. The CLI wizard is the recommended path and works on **Kali Linux, macOS, and Windows (via WSL2; strongly recommended)**.

### 🧠 Models (Neural Brain)

Stingbot is designed for high-performance local inference. 
- **Ollama (Recommended)**: Run `llama3.2` or `mistral` locally for maximum privacy.
- **Failover**: Supports fallback to cloud models if local resources are constrained.

## 📦 Install (recommended)

Runtime: **Node ≥20** & **Python 3.10+**.

```bash
# Deploy the platform instantly
curl -fsSL https://raw.githubusercontent.com/subhadeep-sec/STINGBOT/main/install.sh | bash
```

The installer synchronizes the neural assets and launches the **Stingbot Doctor** to migrate settings and verify system parity.

## ⚡ Quick start (TL;DR)

```bash
# Launch the interactive onboarding wizard
npx stingbot-ai onboard

# Run the health doctor anytime
stingbot doctor

# Start the Neural Gateway
stingbot gateway --port 18789
```

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
- **`client/`**: The React/Vite premium web interface.
- **`agents/python-brain/`**: The core offensive security engine (Python).

## 🔒 Security defaults

Stingbot interacts with live targets. Treat all generated payloads and results with care.
Run `stingbot doctor` to surface risky/misconfigured environment variables.

---
Built with intensity. **Stay Lethal.** 🦂
