# STINGBOT Testing Guide

## Overview

This document provides comprehensive information about testing STINGBOT, including how to run tests, add new tests, and understand test coverage.

## Running Tests

### Run All Tests

```bash
cd /home/kali/Desktop/STINGBOT
python3 -m pytest tests/ -v
```

### Run Specific Test Files

```bash
# Installation tests
python3 -m pytest tests/test_installation.py -v

# CLI interface tests
python3 -m pytest tests/test_cli_interface.py -v

# Agent integration tests
python3 -m pytest tests/test_agents_integration.py -v

# LLM integration tests
python3 -m pytest tests/test_llm_integration.py -v

# End-to-end tests
python3 -m pytest tests/test_end_to_end.py -v

# Demo missions
python3 -m pytest tests/test_demo_missions.py -v
```

### Run Specific Test Categories

```bash
# Unit tests only
python3 -m pytest tests/ -v -m unit

# Integration tests only
python3 -m pytest tests/ -v -m integration

# End-to-end tests only
python3 -m pytest tests/ -v -m e2e
```

### Run Tests with Coverage

```bash
# Generate coverage report
python3 -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# View HTML coverage report
xdg-open htmlcov/index.html
```

## Test Structure

### Test Categories

1. **Installation Tests** (`test_installation.py`)
   - Python/Node.js version validation
   - Configuration file creation
   - Directory structure verification
   - Dependency checks

2. **CLI Interface Tests** (`test_cli_interface.py`)
   - CLI module imports
   - MAS Terminal initialization
   - Agent registration
   - Command parsing

3. **Agent Integration Tests** (`test_agents_integration.py`)
   - All agent imports and initialization
   - Supervisor agent registration
   - Fuzzy agent name matching
   - Mission decomposition and execution

4. **LLM Integration Tests** (`test_llm_integration.py`)
   - LLM adapter initialization
   - Configuration loading
   - Provider support
   - Error handling

5. **End-to-End Tests** (`test_end_to_end.py`)
   - Complete mission workflows
   - Multi-agent coordination
   - Error recovery
   - State persistence

6. **Demo Missions** (`test_demo_missions.py`)
   - Web application audit
   - Network reconnaissance
   - Binary analysis
   - Multi-stage attacks
   - Report generation

### Existing Tests

- `test_supervisor.py` - Supervisor orchestration
- `test_guardrails.py` - Safety and security controls
- `test_state_manager.py` - State graph management

## Adding New Tests

### Creating a New Test File

```python
import unittest
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_my_feature(self):
        """Test description."""
        # Your test code here
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
```

### Best Practices

1. **Use Mocks**: Mock external dependencies (LLM, network calls, file I/O)
2. **Isolate Tests**: Each test should be independent
3. **Clean Up**: Always clean up test artifacts in `tearDown()`
4. **Descriptive Names**: Use clear, descriptive test names
5. **Document**: Add docstrings explaining what each test validates

## Manual Testing

### Interactive Mode

```bash
python3 stingbot.py
```

Test commands:
- `help` - Show available commands
- `mission "test objective"` - Start a mission
- `graph` - View attack graph
- `memory` - View session memory
- `exit` - Exit the terminal

### Direct Mission Mode

```bash
python3 stingbot.py "Perform reconnaissance on test-target.local"
```

### Demo Script

```bash
python3 demo_mission.py
```

## Continuous Integration

### GitHub Actions (if configured)

Tests run automatically on:
- Push to main branch
- Pull requests
- Manual workflow dispatch

### Local CI Simulation

```bash
# Run full test suite with coverage
python3 -m pytest tests/ -v --cov=. --cov-report=term

# Check code style
black --check .
flake8 .
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure paths are correct
export PYTHONPATH="${PYTHONPATH}:/home/kali/Desktop/STINGBOT"
export PYTHONPATH="${PYTHONPATH}:/home/kali/Desktop/STINGBOT/agents/python-brain"
```

**Missing Dependencies**
```bash
# Install test dependencies
pip3 install pytest pytest-cov pytest-mock

# Install development dependencies
pip3 install -r requirements-dev.txt
```

**Mock LLM Issues**
- Tests use mocked LLM responses
- No actual API calls are made during testing
- Configure mock responses in test setup

## Test Coverage Goals

- **Unit Tests**: > 80% coverage
- **Integration Tests**: All major workflows
- **End-to-End Tests**: Complete user journeys
- **Overall**: > 70% code coverage

## Contributing Tests

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Add integration tests for new workflows
4. Update this documentation

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [STINGBOT README](README.md)
- [Contributing Guide](CONTRIBUTING.md)
