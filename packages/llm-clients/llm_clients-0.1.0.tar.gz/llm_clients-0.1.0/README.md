# LLM Clients

A command-line interface for working with Large Language Models, providing utilities for prompts, tools, and LLM API calls.

## Features

- Command-line interface for interacting with various LLM providers (OpenAI, Anthropic, SambaNova, OpenRouter)
- Composable prompt management
- Tool integration for enhanced LLM capabilities:
  - File operations (read/write with XML tags)
  - Search and replace (with regex and line range support)
  - Calculator (for arithmetic operations)
  - History management (for conversation context)
  - Instruction templates
- Configuration management for API keys and settings
- Rich terminal output formatting

## Installation

1. Clone the repository:
```bash
pipx install llm-clients

llm config init
# Manually edit ~/.config/llm-clients/config.yaml
# Or, 
llm config set openai.api_key YOUR_API_KEY
llm config set siliconflow.api_key YOUR_API_KEY
```

```bash
# Use the default model
git diff | llm run "Write a commit message" | xargs -I{} git commit -m {}

# Programming
llm run -t file "Establish a python chat box using OpenAI API, saving to chat.py."
llm run -f chat.py "Add comments for the code."

# Chat box
while true; do
  read -p "Enter your message (type '/exit' to quit): " user_input
  if [ "$user_input" = "/exit" ]; then
    break
  fi
  llm run -H chat.log "$user_input"
done
```


## License

MIT License 