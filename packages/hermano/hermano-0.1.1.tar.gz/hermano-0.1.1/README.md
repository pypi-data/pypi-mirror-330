# Hermano (LLM-powered Assistant for Operations)

A powerful CLI tool that leverages large language models to automate daily tasks.

## Features

- EPUB token counter: Calculate how many tokens an EPUB file would use when sent to an LLM
- More features coming soon!

## Installation

### Using pip

```bash
pip install hermano
```

### Using Homebrew

```bash
brew tap manohar/hermano
brew install hermano
```

## Configuration

Hermano requires API keys for various LLM services. You can set these as environment variables:

```bash
export OPENAI_API_KEY="your-api-key"
export DEEPSEEK_API_KEY="your-api-key"
export GEMINI_API_KEY="your-api-key"
```

Alternatively, you can create a `.env` file in your home directory:

```
OPENAI_API_KEY=your-api-key
DEEPSEEK_API_KEY=your-api-key
GEMINI_API_KEY=your-api-key
```

## Usage

### EPUB Token Counter

```bash
hermano epub tokens path/to/your/book.epub
```

Options:
- `--model`: Specify the model to calculate tokens for (default: "gpt-4")
- `--format`: Output format (text, json) (default: "text")

## Development

### Setup with uv (recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver that we recommend for development:

```bash
# Install uv
pip install uv

# Clone the repository
git clone https://github.com/manohar/hermano.git
cd hermano

# Create and activate a virtual environment 
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode
uv pip install -e .

# Install development dependencies
uv pip install -r requirements-dev.txt
```

### Traditional Setup

```bash
git clone https://github.com/manohar/hermano.git
cd hermano
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

## License

MIT
