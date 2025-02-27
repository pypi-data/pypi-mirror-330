#!/usr/bin/env python3
import argparse
import os
import re
import ast
from typing import Dict, List

def extract_docstrings(filename: str) -> Dict:
    """Extract docstrings from Python file."""
    with open(filename, 'r') as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return {'module': None, 'functions': {}}

    docs = {'module': ast.get_docstring(tree), 'functions': {}}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docs['functions'][node.name] = {
                'docstring': ast.get_docstring(node),
                'args': [arg.arg for arg in node.args.args]
            }

    return docs

def generate_markdown(filename: str, docs: Dict) -> str:
    """Generate markdown documentation from docstrings."""
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

def update_readme(content: str, source_file: str) -> None:
    """Update README.md in the same directory as the source file."""
    marker_begin = "<!-- BEGIN_PY_DOCS -->"
    marker_end = "<!-- END_PY_DOCS -->"
    
    # Get directory of source file and create README.md path
    source_dir = os.path.dirname(source_file)
    readme_path = os.path.join(source_dir, 'README.md')
    
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        
        if marker_begin not in readme_content:
            new_content = f"{readme_content}\n\n{marker_begin}\n{content}\n{marker_end}"
        else:
            pattern = f"{marker_begin}.*?{marker_end}"
            new_content = re.sub(pattern, f"{marker_begin}\n{content}\n{marker_end}", 
                               readme_content, flags=re.DOTALL)
    else:
        # Create directory if it doesn't exist
        os.makedirs(source_dir, exist_ok=True)
        new_content = f"# {os.path.basename(source_dir)} Documentation\n\n{marker_begin}\n{content}\n{marker_end}"
    
    with open(readme_path, 'w') as f:
        f.write(new_content)

def main() -> int:
    """Main function to process Python files and generate documentation."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Python files to process')
    args = parser.parse_args()

    for filename in args.filenames:
        if filename.endswith('.py'):
            docs = extract_docstrings(filename)
            content = generate_markdown(filename, docs)
            update_readme(content, filename)
    
    return 0

if __name__ == '__main__':
    exit(main())
