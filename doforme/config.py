"""Configuration management for DoForMe."""

import os
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "doforme"
CONFIG_FILE = CONFIG_DIR / "config"


def get_api_key():
    """Get OpenAI API key from environment or config file."""
    # First check environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    # Then check config file
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()

    return None


def set_api_key(api_key):
    """Save API key to config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        f.write(api_key)
    os.chmod(CONFIG_FILE, 0o600)  # Secure the file
    return True


def prompt_for_api_key():
    """Prompt user to enter their OpenAI API key."""
    print("\n⚠️  No OpenAI API key found!")
    print("\nYou can set it in one of two ways:")
    print("1. Set environment variable: export OPENAI_API_KEY=your_key_here")
    print("2. Enter it now to save to ~/.config/doforme/config")
    print("\nGet your API key from: https://platform.openai.com/api-keys\n")

    api_key = input("Enter your OpenAI API key (or press Enter to exit): ").strip()
    if not api_key:
        print("No API key provided. Exiting.")
        return None

    set_api_key(api_key)
    print(f"\n✓ API key saved to {CONFIG_FILE}")
    return api_key
