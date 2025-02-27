from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="blindllm",
    version="0.1.0",
    description="A library for making anonymized calls to LLM APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="BlindLLM Team",
    author_email="contact@blindllm.com",  # Replace with actual email
    url="https://github.com/EthanPasquier/BlindLLM",  # Replace with actual repository URL
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",        # For OpenAI API
        "anthropic>=0.18.0",    # For Claude API
        "mistralai",            # For Mistral API
        "text_anonymizer",      # For anonymization functionality
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="llm, ai, anonymization, privacy, openai, mistral, claude",
)
