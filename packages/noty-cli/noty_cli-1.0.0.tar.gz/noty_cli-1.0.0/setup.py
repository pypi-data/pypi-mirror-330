from setuptools import setup, find_packages

setup(
    name="noty-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "windows-curses;platform_system=='Windows'",  # For Windows support
    ],
    entry_points={
        'console_scripts': [
            'noty=noty.cli:main',
        ],
    },
    author="Replit User",
    author_email="user@replit.com",
    description="A terminal-based note-taking application with vim-like navigation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/replit/noty",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console :: Curses",
        "Topic :: Text Editors :: Text Processing",
    ],
    python_requires='>=3.6',
)