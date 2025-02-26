#!/usr/bin/env python3
import argparse
import os
import re
import ast

def extract_docstrings(filename):
    """Extract docstrings from Python file."""
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())

    docs = {'module': ast.get_docstring(tree), 'functions': {}}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docs['functions'][node.name] = {
                'docstring': ast.get_docstring(node),
                'args': [arg.arg for arg in node.args.args]
            }

    return docs

def generate_markdown(filename, docs):
    """Generate markdown documentation."""
    content = []
    content.append(f"## {os.path.basename(filename)}\n")

    if docs['module']:
        content.append(f"{docs['module']}\n")

    if docs['functions']:
        content.append("### Functions\n")
        for func_name, func_info in docs['functions'].items():
            args = ', '.join(func_info['args'])
            content.append(f"#### `{func_name}({args})`\n")
            if func_info['docstring']:
                content.append(f"{func_info['docstring']}\n")

    return '\n'.join(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--path-to-file', default='README.md')
    args = parser.parse_args()

    marker_begin = "<!-- BEGIN_PY_DOCS -->"
    marker_end = "<!-- END_PY_DOCS -->"

    documentation = []
    for filename in args.filenames:
        if filename.endswith('.py'):
            docs = extract_docstrings(filename)
            documentation.append(generate_markdown(filename, docs))

    doc_content = '\n'.join(documentation)

    # Update or create README
    if os.path.exists(args.path_to_file):
        with open(args.path_to_file, 'r') as f:
            content = f.read()

        if marker_begin not in content:
            content = f"{content}\n\n{marker_begin}\n{doc_content}\n{marker_end}"
        else:
            pattern = f"{marker_begin}.*?{marker_end}"
            content = re.sub(pattern, f"{marker_begin}\n{doc_content}\n{marker_end}",
                           content, flags=re.DOTALL)
    else:
        content = f"# Python Documentation\n\n{marker_begin}\n{doc_content}\n{marker_end}"

    with open(args.path_to_file, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()
