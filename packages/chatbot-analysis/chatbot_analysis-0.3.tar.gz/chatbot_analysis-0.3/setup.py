#from setuptools import setup, find_packages

from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()
setup(
    name="chatbot_analysis",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.10.0",
        "pandas>=1.5.3",
        "tabulate>=0.9.0",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'chatbot-cli = chatbot_analysis.cli:main',  # Define your CLI command and the function to call
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
