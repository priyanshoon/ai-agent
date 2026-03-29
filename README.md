# AI Agent

**Note:** This project has a lot of security flaws, do not use it for general purpose use. Use it only for learning how AI Agent works.

This is tool is a simple AI Agent for learning purpose on how AI Agent actually
works in general. The goal of this project is to call AI Agent and make it do
coding for me.

## Installation

### Prerequisite
- Python (version > 3.11)
- uv (python package manager)

```zsh
git clone https://github.com/priyanshoon/ai-agent.git
cd ai-agent
uv sync

touch .env
```

Add your `GEMINI_API_KEY` in `.env` file.

## Usage

```zsh
uv run main.py "your prompt"
uv run main.py "your prompt" --verbose # to see every details (tokens consumed etc...)
```
