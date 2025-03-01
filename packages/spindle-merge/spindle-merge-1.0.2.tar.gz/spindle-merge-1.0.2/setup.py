# setup.py

from setuptools import setup, find_packages

setup(
    name="spindle-merge",
    version="1.0.2",
    description="A command-line tool for merging files with wildcard support.",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="ll3Ynxnj",
    author_email="ll3ynxnj@claywork.co.jp",
    url="https://github.com/ll3ynxnj/spindle",  # GitHubリポジトリURL
    packages=find_packages(),
    install_requires=[],  # 必要な依存関係があれば記載
    entry_points={
        'console_scripts': [
            'spindle=spindle.main:main',  # コマンドラインエントリポイント
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
