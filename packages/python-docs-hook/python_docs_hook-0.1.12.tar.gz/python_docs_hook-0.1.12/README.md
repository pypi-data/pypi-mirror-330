# Python Documentation Hook

A pre-commit hook that automatically generates documentation for Python files by extracting docstrings and function definitions.

## Features

- Automatically extracts Python docstrings
- Generates markdown documentation
- Updates README.md automatically in the same directory as Python files
- Handles nested function documentation
- Supports multiple Python files
- Preserves existing README content

## Installation

```bash
# Using pip
pip install python_docs_hook

# From source
git clone https://github.com/geek-kb/python_docs_hook.git
cd python_docs_hook
pip install -e .
```

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/geek-kb/python_docs_hook
    rev: v0.1.1
    hooks:
    -   id: python-docs
```

Install the pre-commit hook:

```bash
pre-commit install
```

## Configuration

The hook will:

- Look for Python files in your commits
- Generate documentation from docstrings
- Create/update README.md in the same directory as the Python files
- Use markers to update documentation sections:

  ```markdown
  <!-- BEGIN_PY_DOCS -->
## setup.py

<!-- END_PY_DOCS -->
  ```

## Example Output

<!-- BEGIN_PY_DOCS -->
## setup.py

<!-- END_PY_DOCS -->

## Development

Clone the repository and install in development mode:

```bash
git clone https://github.com/geek-kb/python_docs_hook.git
cd python_docs_hook
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some
