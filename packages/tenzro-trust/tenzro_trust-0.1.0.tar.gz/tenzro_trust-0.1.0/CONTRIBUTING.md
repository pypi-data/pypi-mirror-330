# Contributing to Tenzro Trust

Thank you for your interest in contributing to Tenzro Trust! This document outlines the process for contributing to the project and provides guidelines for creating pull requests, reporting issues, and more.

## Table of Contents

- [Contributing to Tenzro Trust](#contributing-to-tenzro-trust)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [Development Environment](#development-environment)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Running Tests](#running-tests)
  - [Contribution Workflow](#contribution-workflow)
  - [Pull Request Guidelines](#pull-request-guidelines)
  - [Coding Standards](#coding-standards)
  - [Testing Guidelines](#testing-guidelines)
  - [Documentation](#documentation)
  - [Adding New Providers](#adding-new-providers)
  - [Issue Reporting](#issue-reporting)
  - [Security Vulnerabilities](#security-vulnerabilities)
  - [License](#license)

## Code of Conduct

Our project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to understand the expectations and maintain a welcoming and inclusive environment.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork to your local machine
3. Set up the development environment
4. Create a feature branch for your changes
5. Make your changes and test them thoroughly
6. Push your changes to your fork
7. Submit a pull request

## Development Environment

### Prerequisites

- Python 3.9 or later
- pip (for installing dependencies)
- git (for version control)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/tenzro-trust.git
cd tenzro-trust

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest -v tests/

# Run with coverage
pytest -v --cov=tenzro_trust --cov-report=term tests/

# Run a specific test
pytest -v tests/test_tenzro_trust.py::test_hsm_provider
```

## Contribution Workflow

1. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes, following the coding standards and guidelines

3. Add tests for your changes, ensuring they pass

4. Update documentation as needed

5. Commit your changes with descriptive commit messages:
```bash
git commit -m "Add support for new HSM type"
```

6. Push your branch to your fork:
```bash
git push origin feature/your-feature-name
```

7. Submit a pull request to the main repository

## Pull Request Guidelines

- Each pull request should address a single concern
- Include a clear description of the changes and the problem they solve
- Reference any related issues using GitHub's issue linking syntax
- Ensure all tests pass before submitting
- Update documentation for any user-facing changes
- Follow the coding standards
- Be responsive to feedback and be willing to make changes as needed

## Coding Standards

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable, function, and class names
- Include docstrings for all public functions, methods, and classes
- Keep functions and methods focused and small
- Use type hints where appropriate
- Add appropriate error handling
- Write clean, readable code over clever solutions

Example docstring format:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of function purpose.
    
    Args:
        param1 (type): Description of parameter 1
        param2 (type): Description of parameter 2
        
    Returns:
        return_type: Description of return value
        
    Raises:
        ExceptionType: Description of when this exception is raised
    """
```

## Testing Guidelines

- Write tests for all new functionality
- Ensure existing tests continue to pass
- Use pytest for writing and running tests
- Include both unit tests and integration tests when appropriate
- Use mocking when testing code that interacts with external systems
- Aim for high test coverage, especially for critical components

## Documentation

- Update documentation for any user-facing changes
- Document all new configuration options and features
- Provide examples for new functionality
- Keep README.md up to date with the latest features and usage
- Update USAGE.md with detailed usage instructions
- Include docstrings for all public APIs

## Adding New Providers

To add a new provider to Tenzro Trust:

1. Create a new file named `tenzro_trust_<provider>.py`
2. Implement a class that inherits from `TenzroTrustProvider`
3. Name the class `<Provider>Provider` (e.g., `CustomProvider`)
4. Implement the required methods: `initialize()`, `sign()`, and `verify()`
5. Add support for `get_attestation()` if appropriate
6. Add appropriate error handling
7. Write comprehensive tests for the new provider
8. Update documentation to include the new provider

Example skeleton for a new provider:

```python
# tenzro_trust_newprovider.py
from tenzro_trust import TenzroTrustProvider, InitializationError, SigningError, VerificationError, ConfigurationError

class NewproviderProvider(TenzroTrustProvider):
    """
    Implementation of Tenzro Trust provider for New Provider technology.
    """
    
    def __init__(self):
        """Initialize a new provider instance."""
        self.initialized = False
        # Add provider-specific attributes
    
    def initialize(self, config):
        """Initialize the provider with configuration settings."""
        try:
            # Implement initialization logic
            self.initialized = True
        except Exception as e:
            raise InitializationError(f"Failed to initialize: {e}")
    
    def sign(self, data):
        """Sign data using the provider."""
        if not self.initialized:
            raise SigningError("Provider not initialized")
        
        # Implement signing logic
        return signature
    
    def verify(self, data, signature):
        """Verify signature using the provider."""
        if not self.initialized:
            raise VerificationError("Provider not initialized")
        
        # Implement verification logic
        return is_valid
    
    def get_attestation(self):
        """Get attestation information about the provider."""
        if not self.initialized:
            return None
        
        # Implement attestation logic
        return attestation_data
```

## Issue Reporting

When reporting issues, please include:

- A clear description of the issue
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Environment information (OS, Python version, package versions)
- Any relevant logs or error messages
- Potential solutions if you have ideas

Use the issue templates provided in the repository when available.

## Security Vulnerabilities

If you discover a security vulnerability, please do NOT open an issue. Instead, email [security@tenzro.com](mailto:security@tenzro.com) with details about the vulnerability.

## License

By contributing to Tenzro Trust, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

Thank you for contributing to Tenzro Trust!