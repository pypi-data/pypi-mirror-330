from setuptools import setup

setup(
    name='python-docs-hook',
    version='0.1.0',
    description='A pre-commit hook to generate Python documentation',
    author='Itai Ganot',
    author_email='lel@lel.bz',
    url='https://github.com/geek-kb/python-docs-hook',
    packages=['python_docs_hook'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'python-docs-hook=python_docs_hook.main:main',
        ],
    },
)
