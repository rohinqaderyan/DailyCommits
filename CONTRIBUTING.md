# Contributing to Daily Python Report

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- Clear description of the enhancement
- Use cases and benefits
- Possible implementation approach
- Examples or mockups if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`

2. **Make your changes**:
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check coverage
   pytest tests/ --cov=scripts
   
   # Test the script
   python scripts/generate_report.py
   ```

4. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Follow conventional commits format:
     - `feat:` for new features
     - `fix:` for bug fixes
     - `docs:` for documentation
     - `test:` for tests
     - `chore:` for maintenance

5. **Push to your fork** and create a pull request

6. **Wait for review** - maintainers will review and provide feedback

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/daily-python-report.git
cd daily-python-report

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Testing Guidelines

- Write tests for all new functionality
- Maintain or improve code coverage
- Tests should be fast and deterministic
- Use descriptive test names
- Include edge cases and error conditions

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Include examples in documentation
- Update troubleshooting section if needed

## Style Guide

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Keep functions focused and small
- Add comments for complex logic
- Use descriptive variable names

## Questions?

If you have questions:
- Check existing issues and documentation
- Create a new issue with the "question" label
- Be specific about what you're trying to accomplish

Thank you for contributing! 🎉
