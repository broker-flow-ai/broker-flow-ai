# BrokerFlow AI - Contributing Guide

## 🎉 Welcome!

We're thrilled you're interested in contributing to BrokerFlow AI! This document will guide you through the contribution process.

## 📋 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/broker-flow-ai.git`
3. Create a branch for your feature: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to your branch: `git push origin feature/your-feature-name`
7. Create a Pull Request

## 📊 How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
1. Check existing issues to avoid duplicates
2. Try to reproduce the bug in the latest version

When submitting a bug report, please include:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable
- Your environment details (OS, Python version, etc.)

### Suggesting Enhancements

We welcome ideas for new features! Before submitting:
1. Check existing issues and feature requests
2. Clearly describe the proposed feature
3. Explain the problem it solves
4. Provide use cases

### Code Contributions

#### Development Setup
1. Follow the installation guide in [INSTALLAZIONE.md](INSTALLAZIONE.md)
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run tests: `python -m pytest`

#### Coding Standards
- Follow PEP 8 style guide
- Write docstrings for all functions and classes
- Use type hints where possible
- Keep functions small and focused
- Write unit tests for new functionality

#### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters or less
- Reference issues and pull requests liberally

### Documentation
- Improve existing documentation
- Add examples and use cases
- Translate documentation to other languages
- Fix typos and grammar errors

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_extract_data.py

# Run with coverage
python -m pytest --cov=modules
```

### Writing Tests
- Place test files in the `tests/` directory
- Follow the naming convention: `test_*.py`
- Use descriptive test function names
- Test both success and failure cases

## 📦 Pull Request Process

1. Ensure any install or build dependencies are removed
2. Update the README.md with details of changes to the interface
3. Increase the version numbers in any examples files and the README.md
4. Your PR must pass all CI checks
5. Your PR must be reviewed and approved by at least one maintainer

## 🌟 Recognition

Contributors will be recognized in:
- Our [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes for each version
- Social media shoutouts

## 🤝 Community

- Join our [Slack community](https://brokerflow-ai.slack.com)
- Follow us on [Twitter](https://twitter.com/BrokerFlowAI)
- Participate in monthly contributor meetings

## 📞 Support

If you need help with your contribution:
1. Check our [documentation](DOCUMENTAZIONE.md)
2. Open an issue with the "question" label
3. Contact our core team at contribute@brokerflow.ai

Thank you for making BrokerFlow AI better! 🚀