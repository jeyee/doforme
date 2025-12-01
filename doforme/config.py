"""Configuration management for DoForMe."""

import json
import os
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "doforme"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Provider configuration
PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "env_var": "OPENAI_API_KEY",
        "url": "https://platform.openai.com/api-keys"
    },
    "anthropic": {
        "name": "Anthropic (Claude)",
        "env_var": "ANTHROPIC_API_KEY",
        "url": "https://console.anthropic.com/settings/keys"
    },
    "groq": {
        "name": "Groq",
        "env_var": "GROQ_API_KEY",
        "url": "https://console.groq.com/keys"
    },
    "openrouter": {
        "name": "OpenRouter",
        "env_var": "OPENROUTER_API_KEY",
        "url": "https://openrouter.ai/keys"
    }
}


def load_config():
    """Load configuration from file."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            # If config is corrupted or old format, return empty dict
            return {}
    return {}


def save_config(config):
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)  # Secure the file


def get_api_key():
    """Get API key and provider from environment or config file.

    Returns:
        tuple: (api_key, provider) or (None, None) if not found
    """
    config = load_config()
    provider = config.get("provider")

    # First check environment variables for each provider
    for prov_id, prov_info in PROVIDERS.items():
        api_key = os.environ.get(prov_info["env_var"])
        if api_key:
            return api_key, prov_id

    # Then check config file
    if provider and "api_key" in config:
        return config["api_key"], provider

    return None, None


def set_api_key(api_key, provider=None):
    """Save API key and provider to config file."""
    config = load_config()
    config["api_key"] = api_key
    if provider:
        config["provider"] = provider
    save_config(config)
    return True


def prompt_for_provider():
    """Prompt user to select an LLM provider."""
    print("\n🤖 Select your LLM provider:")
    providers_list = list(PROVIDERS.items())

    for idx, (prov_id, prov_info) in enumerate(providers_list, 1):
        print(f"{idx}. {prov_info['name']}")

    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(providers_list):
                return providers_list[choice_idx][0]
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 4.")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input.")
            return None


def prompt_for_api_key():
    """Prompt user to select provider and enter their API key."""
    print("\n⚠️  No API key found!")

    # Select provider
    provider = prompt_for_provider()
    if not provider:
        print("No provider selected. Exiting.")
        return None, None

    provider_info = PROVIDERS[provider]
    print(f"\n📝 Setting up {provider_info['name']}")
    print("\nYou can set it in one of two ways:")
    print(f"1. Set environment variable: export {provider_info['env_var']}=your_key_here")
    print(f"2. Enter it now to save to {CONFIG_FILE}")
    print(f"\nGet your API key from: {provider_info['url']}\n")

    api_key = input(f"Enter your {provider_info['name']} API key (or press Enter to exit): ").strip()
    if not api_key:
        print("No API key provided. Exiting.")
        return None, None

    set_api_key(api_key, provider)
    print(f"\n✓ API key saved to {CONFIG_FILE}")
    return api_key, provider
