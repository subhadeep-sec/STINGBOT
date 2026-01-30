# Contributing to STING

Thank you for your interest in contributing to STING! 🦂

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/STINGBOT.git
   cd STINGBOT
   ```

2. **Install Dependencies**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

- **Agents**: Add new specialized agents in `agents/`
- **Tools**: Extend tool wrappers in `tools_mcp/`
- **UI**: Improve terminal interface in `interfaces/`
- **Safety**: Enhance guardrails in `orchestrator/guardrails.py`

## Testing

```bash
# Run unit tests
python3 -m pytest tests/

# Test your changes
python3 stingbot.py "test mission objective"
```

## Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub

## Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings to functions
- Keep commits atomic and well-described

## Questions?

Open an issue on GitHub or reach out to the maintainers!
