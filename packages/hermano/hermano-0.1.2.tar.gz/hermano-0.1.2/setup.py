from setuptools import setup, find_packages

setup(
    name="hermano",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "ebooklib>=0.17.1",
        "beautifulsoup4>=4.10.0",
        "openai>=1.0.0",
        "tiktoken>=0.5.0",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "hermano=hermano.cli:cli",
        ],
    },
    python_requires=">=3.8",
    author="Manohar",
    author_email="example@example.com",
    description="LLM-powered CLI tool for daily tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hermano-tools/hermano-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
