from setuptools import setup, find_packages

setup(
    name='python_docs_hook',  # Changed from hyphen to underscore
    version='0.1.9',
    description='A pre-commit hook to generate Python documentation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Itai Ganot',
    author_email='lel@lel.bz',
    url='https://github.com/geek-kb/python_docs_hook',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'python-docs-hook=python_docs_hook.main:main',  # This creates the executable
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
