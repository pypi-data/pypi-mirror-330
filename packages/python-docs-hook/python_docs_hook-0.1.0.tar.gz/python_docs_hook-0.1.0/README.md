# Python Documentation Hook

A pre-commit hook that automatically generates documentation for Python files.

## Installation

```bash
pip install python-docs-hook
```

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/geek-kb/python-docs-hook
    rev: v0.1.0
    hooks:
    -   id: python-docs
```

## Configuration

The hook supports the following options:

- `--path-to-file`: Specify the output file (default: README.md)

## Example Output

<!-- BEGIN_PY_DOCS -->
## example.py

Example module documentation

### Functions

#### `fetch_astronauts(astros_api_url)`

Fetches and displays current astronauts in space

#### `get_iss_location(iss_api_url)`

Gets and displays current ISS location coordinates
<!-- END_PY_DOCS -->
