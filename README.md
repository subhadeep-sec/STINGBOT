# 🦂 Stingbot — Neural Security Platform

<p align="center">
    <img src="docs/assets/logo.png" alt="Stingbot" width="500">
</p>

<p align="center">
  <strong>EXPLOIT! EXFILTRATE! EVOLVE!</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <a href="https://github.com/subhadeep-sec/STINGBOT/releases"><img src="https://img.shields.io/github/v/release/subhadeep-sec/STINGBOT?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
</p>

**Stingbot** is an *autonomous AI security platform* built for the neural age. 
It follows a decoupled architecture, separating the **Neural Gateway** (Control Plane) from the **Python Security Brain** (Execution Engine). This allows for a premium Web UI experience combined with the raw power of Python-based offensive tools.

[Official Docs](https://docs.stingbot.ai) · [Project Wiki](https://github.com/subhadeep-sec/STINGBOT/wiki) · [Onboarding Wizard](https://docs.stingbot.ai/start)

### 💎 The Platform Strategy
- **Frontend**: Premium React/Vite dashboard for mission monitoring.
- **Gateway**: Node.js/Express WebSocket server for real-time log streaming.
- **Brain**: Headless Python Engine for autonomous tool orchestration.

## 📦 Installation (The Platform Way)

Runtime: **Node ≥20** & **Python 3.10+**.

```bash
# Launch the interactive platform onboarding wizard
npx stingbot-ai onboard
```

The wizard installs the **Stingbot Daemon**, provisions the Python environment, and synchronizes with your local **Ollama** neural brain.

## ⚡ Quick Start

```bash
# Start the Neural Gateway
stingbot gateway --port 18789

# Connect your local brain
stingbot agent "audit http://testphp.vulnweb.com"

# Launch the Web Dashboard
npm run dev --workspace=client
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

## �️ Components
- **`gateway/`**: The Node.js WebSocket control plane.
- **`client/`**: The React/Vite premium web interface.
- **`agents/python-brain/`**: The core offensive security engine.

---
Built with intensity. **Stay Lethal.** 🦂
