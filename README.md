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

**Stingbot** is a *generalist neural engine* for offensive security and autonomous workflow automation.
It leverages advanced LLM reasoning to perform complex security audits, reconnaissance, and exploitation tasks autonomously. Designed for Kali Linux but optimized for any Unix environment, Stingbot transforms raw security tools into a coordinated, intelligent offensive platform.

If you want a personal, autonomous security analyst that feels fast, lethal, and always-on, this is it.

[Website](https://stingbot.ai) · [Docs](https://docs.stingbot.ai) · [Getting Started](https://docs.stingbot.ai/start) · [Wizard](https://docs.stingbot.ai/start/wizard)

Preferred setup: run the onboarding wizard (`npx stingbot-ai onboard`). It walks through the neural brain setup, security tool parity, and pairing. The CLI wizard is the recommended path and works on **Kali Linux, macOS, and WSL2**.

## 🧠 Models (Neural Brain)

Stingbot is designed for high-performance local inference. 
- **Ollama (Recommended)**: Run `llama3.2` or `mistral` locally for maximum privacy.
- **Failover**: Supports fallback to cloud models if local resources are constrained.

## � Install (recommended)

Runtime: **Python 3.10+** & **Node ≥20**.

```bash
# Launch the interactive onboarding wizard
npx stingbot-ai onboard
```

The wizard ensures your environment is hardened, security tools are bridged, and the neural brain is synchronized.

## ⚡ Quick start

```bash
# Establish the neural link
stingbot onboard

# Execute an autonomous mission
stingbot "perform a scan on testphp.vulnweb.com and look for SQLi"

# Run the health doctor
stingbot doctor
```

## 🦂 Highlights

- **[Autonomous Offensive Engine](https://docs.stingbot.ai/core)** — Real-time reasoning loop for complex exploitation chains.
- **[Neural Security Gateway](https://docs.stingbot.ai/gateway)** — Centralized control plane for sessions, tools, and events.
- **[Multi-Tool Parity](https://docs.stingbot.ai/tools)** — Native integration with `nmap`, `sqlmap`, `nikto`, `scapy`, and more.
- **[Interactive CLI/TUI](https://docs.stingbot.ai/interfaces)** — Premium terminal experience with real-time log streaming.

## 🛠️ Everything we built so far

### Core platform
- [Neural Orchestrator](https://docs.stingbot.ai/core) with autonomous feedback loops and error correction.
- [CLI/TUI surface](https://docs.stingbot.ai/interfaces) with rich logging and interactive pairing.
- [Tool Integration Layer](https://docs.stingbot.ai/tools) for sub-process execution and result synthesis.

### Security Modules
- [Reconnaissance](https://docs.stingbot.ai/modules/recon): Port scanning, service discovery, and banner grabbing.
- [Exploitation](https://docs.stingbot.ai/modules/exploit): SQL injection, XSS discovery, and CVE research.
- [Reporting](https://docs.stingbot.ai/modules/reporting): Automated generation of technical audit summaries.

---

## 🏗️ How it works

```
Operator Commands (Terminal)
               │
               ▼
┌───────────────────────────────┐
│       Neural Orchestrator     │
│       (The Brain & Logic)     │
└──────────────┬────────────────┘
               │
               ├─ Security Tool Layer (sqlmap, nmap, etc.)
               ├─ LLM Reasoning Logic (Local Ollama / Cloud)
               ├─ Interface Layer (CLI, TUI, Dashboard)
               └─ Observation Engine (Error Correction)
```

## 🔒 Security Model

- **Local-First**: Reasoning happens on your machine.
- **Consent-Based**: All neural links require explicit pairing codes.
- **Sandboxing**: Security tools run in restricted sub-processes.

---

## � Credits
Stingbot is inspired by the **OpenClaw** philosophy of personal AI assistants.
Built for the community. **Stay Lethal.**
