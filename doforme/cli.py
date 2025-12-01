"""Main CLI implementation for DoForMe."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

from openai import OpenAI

from .config import get_api_key, prompt_for_api_key, set_api_key


def check_tool_exists(command):
    """Check if the main tool/command exists on the system."""
    # Extract the first command (tool name)
    parts = command.strip().split()
    if not parts:
        return True

    tool = parts[0]

    # Handle shell built-ins and common commands
    if tool in ["cd", "echo", "export", "set", "source", "alias"]:
        return True

    # Check if tool exists in PATH
    return shutil.which(tool) is not None


def get_command_from_llm(prompt, api_key):
    """Query OpenAI to convert natural language to CLI command."""
    client = OpenAI(api_key=api_key)

    system_prompt = """You are a helpful assistant that converts natural language instructions into CLI commands.

Rules:
1. Return ONLY the command, nothing else
2. Do not include explanations or markdown formatting
3. Do not include backticks or code blocks
4. Return the exact command that can be executed in a bash shell
5. If multiple commands are needed, join them with && or ; as appropriate
6. Use common Unix/Linux tools when possible
7. Make sure the command is safe and doesn't require sudo unless absolutely necessary

Examples:
User: "downsize with ffmpeg to max 1024 on each side"
Assistant: ffmpeg -i input.mp4 -vf "scale='min(1024,iw)':'min(1024,ih)':force_original_aspect_ratio=decrease" output.mp4

User: "find all python files"
Assistant: find . -name "*.py"

User: "show disk usage"
Assistant: df -h"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        command = response.choices[0].message.content.strip()
        # Remove any markdown code blocks if present
        command = re.sub(r'^```(?:bash|sh)?\n?', '', command)
        command = re.sub(r'\n?```$', '', command)
        return command.strip()

    except Exception as e:
        print(f"❌ Error querying OpenAI API: {e}", file=sys.stderr)
        return None


def handle_set_api_key(prompt):
    """Check if the prompt is asking to set the API key."""
    # Pattern to match variations of setting API key
    patterns = [
        r"set (?:the )?api[ _]?key to (.+)",
        r"save (?:the )?api[ _]?key as (.+)",
        r"update (?:the )?api[ _]?key to (.+)",
        r"change (?:the )?api[ _]?key to (.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, prompt.lower())
        if match:
            api_key = match.group(1).strip()
            set_api_key(api_key)
            print(f"✓ API key updated successfully")
            return True

    return False


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="DoForMe - Execute CLI commands using natural language",
        usage="doforme \"<your natural language command>\""
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Natural language description of what you want to do"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the command without executing it"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip confirmation and execute immediately"
    )

    args = parser.parse_args()

    if not args.prompt:
        parser.print_help()
        return 1

    prompt = " ".join(args.prompt)

    # Special case: setting API key
    if handle_set_api_key(prompt):
        return 0

    # Get API key
    api_key = get_api_key()
    if not api_key:
        api_key = prompt_for_api_key()
        if not api_key:
            return 1

    print(f"🤔 Thinking about: {prompt}")

    # Get command from LLM
    command = get_command_from_llm(prompt, api_key)
    if not command:
        return 1

    print(f"\n📋 Command: {command}")

    # Check if required tool exists
    if not check_tool_exists(command):
        tool = command.strip().split()[0]
        print(f"\n❌ Error: Required tool '{tool}' is not installed on your system.")
        print(f"   Please install it and try again.")
        return 1

    # Ask for confirmation unless --yes or --dry-run
    if args.dry_run:
        print("\n🏃 Dry run mode - not executing")
        return 0

    if not args.yes:
        response = input("\n▶️  Execute this command? [Y/n]: ").strip().lower()
        if response and response not in ["y", "yes"]:
            print("❌ Cancelled")
            return 0

    # Execute the command
    print()
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=False,
            text=True
        )
        return result.returncode
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error executing command: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
