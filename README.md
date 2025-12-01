# DoForMe

A CLI tool that converts natural language into CLI commands using AI. No more remembering complex command syntax!

## Features

- 🤖 Supports multiple LLM providers (OpenAI, Anthropic/Claude, Groq, OpenRouter)
- 🔍 Automatically checks if required tools are installed
- ⚡ Fast and easy to use
- 🔐 Secure API key management
- ✅ Confirmation before executing commands
- 🎯 Dry-run mode to preview commands

## Installation

### From PyPI

Install with your preferred LLM provider:

```bash
# For OpenAI support
pip install "doforme[openai]"

# For Anthropic/Claude support
pip install "doforme[anthropic]"

# For Groq support
pip install "doforme[groq]"

# For OpenRouter support
pip install "doforme[openrouter]"

# For all providers
pip install "doforme[all]"
```

### From source

```bash
git clone https://github.com/yourusername/doforme.git
cd doforme

# Install with your preferred provider
pip install -e ".[openai]"     # For OpenAI
pip install -e ".[anthropic]"  # For Anthropic/Claude
pip install -e ".[groq]"       # For Groq
pip install -e ".[openrouter]" # For OpenRouter
pip install -e ".[all]"        # For all providers
```

## Setup

### 1. Get an API Key

Choose your preferred LLM provider and get an API key:

- **OpenAI**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic (Claude)**: [Anthropic Console](https://console.anthropic.com/settings/keys)
- **Groq**: [Groq Console](https://console.groq.com/keys)
- **OpenRouter**: [OpenRouter](https://openrouter.ai/keys)

### 2. Configure the API Key

You have three options:

**Option A: Environment Variable (Recommended)**

```bash
# For OpenAI
export OPENAI_API_KEY=your_key_here

# For Anthropic/Claude
export ANTHROPIC_API_KEY=your_key_here

# For Groq
export GROQ_API_KEY=your_key_here

# For OpenRouter
export OPENROUTER_API_KEY=your_key_here
```

Add this to your `~/.bashrc` or `~/.zshrc` to make it permanent.

**Option B: Interactive Setup**

Just run `doforme` without an API key and it will prompt you to:
1. Select your LLM provider
2. Enter your API key

```bash
doforme "list files"
```

**Option C: Using DoForMe itself**

```bash
doforme "set the api key to sk-..."
# This will prompt you to select a provider
```

## Usage

### Basic Usage

Simply describe what you want to do in natural language:

```bash
doforme "downsize with ffmpeg to max 1024 on each side"
```

This will:
1. Query the AI to generate the appropriate command
2. Show you the command
3. Ask for confirmation
4. Execute it (if you confirm)

### More Examples

```bash
# File operations
doforme "find all python files in this directory"
doforme "compress this folder into a zip file"
doforme "count lines of code in all js files"

# Media processing
doforme "convert all png images to jpg"
doforme "extract audio from video.mp4"
doforme "create a gif from images"

# System operations
doforme "show disk usage"
doforme "find the largest files in current directory"
doforme "check my internet speed"

# Git operations
doforme "show git log for the last 5 commits"
doforme "undo last commit but keep changes"
```

### Options

#### Dry Run Mode

Preview the command without executing:

```bash
doforme --dry-run "delete all log files"
```

#### Auto-Execute Mode

Skip confirmation (use with caution!):

```bash
doforme --yes "show current date"
doforme -y "list files"
```

## How It Works

1. **Input**: You provide a natural language description
2. **AI Processing**: DoForMe sends your request to your chosen LLM provider's API
3. **Command Generation**: The AI generates the appropriate CLI command
4. **Validation**: Checks if required tools are installed
5. **Confirmation**: Shows you the command and asks for confirmation
6. **Execution**: Runs the command in your shell

## Safety Features

- ✅ Shows you the command before execution
- ✅ Checks if required tools exist on your system
- ✅ Secure API key storage (600 permissions)
- ✅ Confirmation prompts (can be disabled with `-y`)
- ✅ Dry-run mode for testing

## Error Handling

If a required tool is not installed, DoForMe will tell you:

```bash
$ doforme "convert video with ffmpeg"
🤔 Thinking about: convert video with ffmpeg

📋 Command: ffmpeg -i input.mp4 output.avi

❌ Error: Required tool 'ffmpeg' is not installed on your system.
   Please install it and try again.
```

## Configuration

API key and provider selection are stored in `~/.config/doforme/config.json` with secure permissions (600).

To change your API key:

```bash
doforme "set the api key to sk-new-key-here"
# This will prompt you to select a provider
```

Or manually edit `~/.config/doforme/config.json`:

```json
{
  "api_key": "your-api-key-here",
  "provider": "openai"
}
```

Valid provider values: `openai`, `anthropic`, `groq`, `openrouter`

## Requirements

- Python 3.8 or higher
- API key from one of the supported providers (OpenAI, Anthropic, Groq, or OpenRouter)
- Internet connection (for API calls)
- Provider-specific Python package (installed automatically with extras)

## Privacy & Security

- Your prompts are sent to your chosen LLM provider's API
- API keys are stored locally with restricted permissions (600)
- Commands are shown before execution
- No telemetry or tracking by DoForMe

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Troubleshooting

### "No API key found"

Make sure you've either:
- Set the appropriate environment variable for your provider (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY`, or `OPENROUTER_API_KEY`)
- Run the interactive setup when prompted

### "Required tool not installed"

Install the missing tool using your package manager:

```bash
# Ubuntu/Debian
sudo apt install <tool-name>

# macOS
brew install <tool-name>

# Fedora
sudo dnf install <tool-name>
```

### Command doesn't work as expected

Use `--dry-run` to see the generated command and adjust your prompt for better results.

## Acknowledgments

- Supports multiple LLM providers: [OpenAI](https://openai.com/), [Anthropic](https://anthropic.com/), [Groq](https://groq.com/), and [OpenRouter](https://openrouter.ai/)
- Inspired by the need to simplify CLI usage

## Support

For issues and questions, please [open an issue](https://github.com/yourusername/doforme/issues) on GitHub.
