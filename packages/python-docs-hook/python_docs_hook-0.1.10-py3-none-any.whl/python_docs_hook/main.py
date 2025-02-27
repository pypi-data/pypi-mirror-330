#!/usr/bin/env python3
import logging
import os
import argparse
import re
import ast
from typing import Dict, List, Optional

# Set up logging with detailed formatting
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('python_docs_hook')

# Define documentation markers
marker_begin = "<!-- BEGIN_PY_DOCS -->"
marker_end = "<!-- END_PY_DOCS -->"

def extract_docstrings(filename: str) -> Dict:
    """Extract docstrings from Python file.

    Args:
        filename: Path to the Python file to process

    Returns:
        Dictionary containing module and function documentation
    """
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            logger.error(f"Syntax error in file: {filename}")
            return {'module': None, 'functions': {}}

    docs = {'module': ast.get_docstring(tree), 'functions': {}}
    logger.debug(f"Extracted module docstring from {filename}")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docs['functions'][node.name] = {
                'docstring': ast.get_docstring(node),
                'args': [arg.arg for arg in node.args.args]
            }
            logger.debug(f"Extracted docstring for function: {node.name}")

    return docs

def generate_markdown(filename: str, docs: Dict) -> str:
    """Generate markdown documentation from docstrings.

    Args:
        filename: Name of the source file
        docs: Dictionary containing extracted documentation

    Returns:
        Formatted markdown string
    """
    content = []
    base_filename = os.path.basename(filename)
    content.append(f"## {base_filename}\n")
    logger.debug(f"Generating markdown for {base_filename}")

    if docs['module']:
        content.append(f"{docs['module']}\n")
        logger.debug("Added module documentation")

    if docs['functions']:
        content.append("### Functions\n")
        for func_name, func_info in docs['functions'].items():
            args = ', '.join(func_info['args'])
            content.append(f"#### `{func_name}({args})`\n")
            if func_info['docstring']:
                content.append(f"{func_info['docstring']}\n")
            logger.debug(f"Added documentation for function: {func_name}")

    return '\n'.join(content)

def is_path_allowed(source_dir: str, allowed_paths: Optional[List[str]]) -> bool:
    """Check if the source directory is in allowed paths.
    
    Args:
        source_dir: Directory to check
        allowed_paths: List of allowed paths
        
    Returns:
        True if directory is allowed, False otherwise
    """
    # Get absolute paths
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abs_source_dir = os.path.abspath(source_dir)
    
    logger.debug(f"Checking path: {abs_source_dir}")
    logger.debug(f"Package directory: {package_dir}")
    logger.debug(f"Allowed paths: {allowed_paths}")
    
    # Skip package directory
    if abs_source_dir.startswith(package_dir):
        logger.debug(f"Skipping package directory: {package_dir}")
        return False
    
    # If no paths specified, allow all
    if not allowed_paths:
        logger.debug("No path restrictions, allowing all")
        return True
    
    # Check if path is in allowed paths
    for path in allowed_paths:
        abs_path = os.path.abspath(path)
        logger.debug(f"Checking against allowed path: {abs_path}")
        if abs_source_dir.startswith(abs_path):
            logger.debug(f"Path {abs_source_dir} is allowed")
            return True
    
    logger.debug(f"Path {abs_source_dir} is not allowed")
    return False

def update_readme(content: str, source_file: str, allowed_paths: Optional[List[str]] = None) -> None:
    """Update README.md in the same directory as the source file.
    
    Args:
        content: Generated markdown content
        source_file: Path to the source Python file
        allowed_paths: List of paths where README.md files should be generated
    """
    source_dir = os.path.dirname(source_file) or '.'
    logger.debug(f"Processing file: {source_file}")
    logger.debug(f"Source directory: {source_dir}")
    
    if not is_path_allowed(source_dir, allowed_paths):
        logger.debug(f"Skipping {source_dir} - not in allowed paths")
        return

    readme_path = os.path.join(source_dir, 'README.md')
    logger.debug(f"README path: {readme_path}")

    try:
        if os.path.exists(readme_path):
            logger.debug(f"Updating existing README at {readme_path}")
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()

            if marker_begin not in readme_content:
                new_content = f"{readme_content}\n\n{marker_begin}\n{content}\n{marker_end}"
            else:
                pattern = re.escape(marker_begin) + r".*?" + re.escape(marker_end)
                new_content = re.sub(pattern, f"{marker_begin}\n{content}\n{marker_end}",
                                   readme_content, flags=re.DOTALL)
        else:
            logger.debug(f"Creating new README at {readme_path}")
            os.makedirs(source_dir, exist_ok=True)
            new_content = f"# {os.path.basename(source_dir)} Documentation\n\n{marker_begin}\n{content}\n{marker_end}"

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            logger.debug(f"Successfully wrote README at {readme_path}")

    except Exception as e:
        logger.error(f"Error updating README: {e}")
        raise

def main() -> int:
    """Main function to process Python files and generate documentation.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(description='Generate Python documentation')
    parser.add_argument('filenames', nargs='*', help='Python files to process')
    parser.add_argument(
        '--doc-paths',
        nargs='+',
        help='Paths where README.md files should be generated (space-separated)',
        default=None
    )
    args = parser.parse_args()

    try:
        logger.debug(f"Processing files: {args.filenames}")
        logger.debug(f"Documentation paths: {args.doc_paths}")

        for filename in args.filenames:
            if filename.endswith('.py'):
                logger.info(f"Processing Python file: {filename}")
                docs = extract_docstrings(filename)
                content = generate_markdown(filename, docs)
                update_readme(content, filename, args.doc_paths)

        return 0
    except Exception as e:
        logger.error(f"Error processing files: {e}")
        return 1

if __name__ == '__main__':
    exit(main())