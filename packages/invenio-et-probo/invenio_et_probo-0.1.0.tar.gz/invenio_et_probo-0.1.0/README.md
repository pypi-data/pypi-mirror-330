# Invenio Et Probo Test Runner

A modern, GUI-based test runner for Python unit tests and integration tests. Built with tkinter and ttkbootstrap, it provides an intuitive interface for discovering and running tests with real-time feedback and detailed logging.

## Features

- Modern, bootstrap-themed GUI interface
- Automatic test discovery
- Real-time test execution feedback
- Detailed test and method logging
- Test filtering and exclusion patterns
- Separate process test execution to avoid GUI freezing
- Support for both unit tests and integration tests

## Installation

```bash
pip install invenio-et-probo
```

## Usage

### As a Command Line Tool

```bash
# Start the GUI test runner
invenio-test-runner

# Start with a specific test directory
invenio-test-runner --test-dir /path/to/tests

# Start with specific exclude patterns
invenio-test-runner --exclude "test_skip_*" "test_integration_*"
```

### As a Python Module

```python
from invenio_et_probo.gui import TestRunnerGUI

# Create and start the test runner
runner = TestRunnerGUI(
    theme="darkly",  # Optional: ttkbootstrap theme
    test_dir="path/to/tests",  # Optional: initial test directory
    exclude_patterns=["test_skip_*"]  # Optional: patterns to exclude
)
runner.run()
```

## Configuration

- **Theme**: Uses ttkbootstrap themes. Available themes include: "darkly", "flatly", "litera", etc.
- **Test Directory**: Any directory containing Python test files
- **Exclude Patterns**: List of patterns to exclude from test discovery

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   python -m pytest tests/
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
