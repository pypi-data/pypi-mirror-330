# AI GCM

A command-line tool that uses AI to generate meaningful git commit messages.

## Features

- Analyzes git diff to understand code changes
- Generates human-readable summaries of changes
- Creates conventional commit messages
- Supports custom AI models
- Interactive prompts for staging changes

## Prerequisites

1. Install [Ollama](https://ollama.ai):
   ```bash
   brew install ollama
   ```

2. Pull required models:
   ```bash
   ollama pull qwen2.5-coder  # for code analysis
   ollama pull llama3.2       # for commit message generation
   ```

## Installation

```bash
pip install ai-gcm
```

## Usage

### Generate Commit Message

```bash
# Stage your changes first
git add .

# Generate commit message with default models
ai-gcm commit

# Show detailed output including code changes summary
ai-gcm commit --verbose

# Use custom models
ai-gcm commit --summary-model qwen2.5-coder --commit-model llama3.2
```

### Options

- `--summary-model, -s`: Model to use for code summary generation (default: qwen2.5-coder)
- `--commit-model, -c`: Model to use for commit message generation (default: llama3.2)
- `--verbose, -v`: Show detailed output including summary

### Check Version

```bash
ai-gcm version
```

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## License

MIT
