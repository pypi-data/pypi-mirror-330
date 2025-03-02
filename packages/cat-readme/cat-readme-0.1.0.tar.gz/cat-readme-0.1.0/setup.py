from setuptools import setup, find_packages

setup(
    name='cat-readme',
    version='0.1.0',
    author='DOSSEH Shalom',
    author_email='dossehdosseh14@gmail.com',
    description='A command-line tool to display markdown files with rich formatting.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AnalyticAce/cat-readme',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'rich',
        'typer',
        'pathlib',
    ],
    entry_points={
        'console_scripts': [
            'cat-readme=cat_readme.cli:app',
        ],
    }
)
