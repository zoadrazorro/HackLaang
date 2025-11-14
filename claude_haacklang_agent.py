#!/usr/bin/env python3
"""
ClaudeHackLang Agent - AI Coding Assistant for HaackLang
A intelligent assistant powered by Claude that helps with HaackLang programming.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed.")
    print("Install it with: pip install anthropic")
    sys.exit(1)


class HaackLangKnowledgeBase:
    """Loads and manages HaackLang documentation and examples."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.docs = {}
        self.examples = {}
        self._load_knowledge()

    def _load_knowledge(self):
        """Load documentation and examples from the repository."""
        # Load documentation files
        doc_files = {
            'quickref': self.repo_path / 'docs' / 'QUICKREF.md',
            'readme': self.repo_path / 'README.md',
            'tutorial': self.repo_path / 'docs' / 'TUTORIAL.md',
            'comparison': self.repo_path / 'docs' / 'COMPARISON.md',
        }

        for key, path in doc_files.items():
            if path.exists():
                self.docs[key] = path.read_text()

        # Load example files
        examples_dir = self.repo_path / 'examples'
        if examples_dir.exists():
            for example_file in examples_dir.glob('*.haack'):
                self.examples[example_file.stem] = example_file.read_text()

    def get_context_summary(self) -> str:
        """Get a summary of HaackLang for the AI agent."""
        return f"""# HaackLang Knowledge Base

## Quick Reference
{self.docs.get('quickref', 'Not available')}

## Examples Available
{', '.join(self.examples.keys())}

Use this knowledge to help users write, debug, and understand HaackLang code.
"""

    def get_example(self, name: str) -> Optional[str]:
        """Get a specific example by name."""
        return self.examples.get(name)

    def list_examples(self) -> List[str]:
        """List all available examples."""
        return list(self.examples.keys())


class ClaudeHaackLangAgent:
    """AI coding assistant for HaackLang powered by Claude."""

    def __init__(self, api_key: str, repo_path: str = "."):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.knowledge = HaackLangKnowledgeBase(repo_path)
        self.conversation_history = []

        # System prompt with HaackLang knowledge
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt with HaackLang knowledge."""
        return f"""You are an expert AI coding assistant for HaackLang, a polyrhythmic, polylogical programming language based on Susan Haack's philosophy of logical pluralism.

{self.knowledge.get_context_summary()}

Your role is to help users:
1. **Write HaackLang code** - Generate correct, idiomatic HaackLang programs
2. **Debug code** - Identify and fix errors in HaackLang programs
3. **Explain concepts** - Clarify HaackLang syntax, semantics, and philosophy
4. **Optimize code** - Suggest improvements for clarity and effectiveness
5. **Answer questions** - Provide detailed explanations about the language

Key HaackLang Concepts to Remember:
- **Tracks**: Independent logical timelines with different periods and logic types (classical, fuzzy, paraconsistent)
- **Truth Values (tv)**: Variables that have different values across different tracks
- **Polylogical Operations**: Operators that work differently on each track (e.g., 'and' uses classical logic on one track, fuzzy on another)
- **Guards**: Conditional execution that only fires when specific tracks are active
- **Contexts**: Cognitive domains with specific logic types
- **Rhythmic Computation**: Different tracks update at different temporal rates

Always provide:
- Clear, executable HaackLang code
- Explanations of how polylogical operations work
- Context about which track(s) your code affects
- Comments explaining the reasoning

Be concise but thorough. Focus on practical, working code.
"""

    def chat(self, user_message: str, mode: str = "assist") -> str:
        """
        Send a message to Claude and get a response.

        Args:
            user_message: The user's question or request
            mode: The assistant mode (assist, explain, generate, debug, analyze)

        Returns:
            Claude's response
        """
        # Add mode-specific context
        mode_prompts = {
            "explain": "Please explain the following HaackLang concept or code:\n\n",
            "generate": "Please generate HaackLang code for the following requirement:\n\n",
            "debug": "Please debug the following HaackLang code and identify any issues:\n\n",
            "analyze": "Please analyze the following HaackLang code and explain how it works:\n\n",
            "assist": ""  # General assistance
        }

        prefixed_message = mode_prompts.get(mode, "") + user_message

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": prefixed_message
        })

        try:
            # Call Claude API
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=self.system_prompt,
                messages=self.conversation_history
            )

            # Extract response text
            assistant_message = response.content[0].text

            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except anthropic.APIError as e:
            return f"API Error: {e}"

    def analyze_file(self, file_path: str) -> str:
        """Analyze a HaackLang file and provide insights."""
        try:
            code = Path(file_path).read_text()
            return self.chat(f"Analyze this HaackLang program:\n\n```haack\n{code}\n```", mode="analyze")
        except FileNotFoundError:
            return f"Error: File '{file_path}' not found."
        except Exception as e:
            return f"Error reading file: {e}"

    def debug_file(self, file_path: str) -> str:
        """Debug a HaackLang file."""
        try:
            code = Path(file_path).read_text()
            return self.chat(f"Debug this HaackLang program:\n\n```haack\n{code}\n```", mode="debug")
        except FileNotFoundError:
            return f"Error: File '{file_path}' not found."
        except Exception as e:
            return f"Error reading file: {e}"

    def get_example_explanation(self, example_name: str) -> str:
        """Get an explanation of a specific example."""
        example_code = self.knowledge.get_example(example_name)
        if not example_code:
            return f"Example '{example_name}' not found. Available: {', '.join(self.knowledge.list_examples())}"

        return self.chat(f"Explain this HaackLang example:\n\n```haack\n{example_code}\n```", mode="explain")

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []


def load_api_key() -> Optional[str]:
    """Load API key from environment or .env file."""
    # Try environment variable first
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        return api_key

    # Try .env file
    env_file = Path('.env')
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith('ANTHROPIC_API_KEY='):
                return line.split('=', 1)[1].strip().strip('"').strip("'")

    return None


def interactive_mode(agent: ClaudeHaackLangAgent):
    """Run the agent in interactive REPL mode."""
    print("ClaudeHackLang Agent - Interactive Mode")
    print("=" * 50)
    print("Commands:")
    print("  /help          - Show this help")
    print("  /examples      - List available examples")
    print("  /example <name> - Explain an example")
    print("  /analyze <file> - Analyze a HaackLang file")
    print("  /debug <file>   - Debug a HaackLang file")
    print("  /reset         - Reset conversation")
    print("  /quit          - Exit")
    print("=" * 50)
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith('/'):
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else None

                if command == '/quit':
                    print("Goodbye!")
                    break
                elif command == '/help':
                    print("\nCommands:")
                    print("  /help          - Show this help")
                    print("  /examples      - List available examples")
                    print("  /example <name> - Explain an example")
                    print("  /analyze <file> - Analyze a HaackLang file")
                    print("  /debug <file>   - Debug a HaackLang file")
                    print("  /reset         - Reset conversation")
                    print("  /quit          - Exit\n")
                elif command == '/examples':
                    examples = agent.knowledge.list_examples()
                    print(f"\nAvailable examples: {', '.join(examples)}\n")
                elif command == '/example':
                    if arg:
                        print("\nClaude:", agent.get_example_explanation(arg), "\n")
                    else:
                        print("Usage: /example <name>\n")
                elif command == '/analyze':
                    if arg:
                        print("\nClaude:", agent.analyze_file(arg), "\n")
                    else:
                        print("Usage: /analyze <file>\n")
                elif command == '/debug':
                    if arg:
                        print("\nClaude:", agent.debug_file(arg), "\n")
                    else:
                        print("Usage: /debug <file>\n")
                elif command == '/reset':
                    agent.reset_conversation()
                    print("Conversation reset.\n")
                else:
                    print(f"Unknown command: {command}\n")
                continue

            # Regular chat
            response = agent.chat(user_input)
            print(f"\nClaude: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="ClaudeHackLang Agent - AI Coding Assistant for HaackLang",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python claude_haacklang_agent.py

  # Ask a question
  python claude_haacklang_agent.py -q "How do I create a track with fuzzy logic?"

  # Generate code
  python claude_haacklang_agent.py -g "Create a program that models decision-making under uncertainty"

  # Analyze a file
  python claude_haacklang_agent.py -a examples/simple.haack

  # Debug a file
  python claude_haacklang_agent.py -d myprogram.haack

  # Explain an example
  python claude_haacklang_agent.py -e polylogical

API Key Configuration:
  Set ANTHROPIC_API_KEY environment variable or create a .env file:
    export ANTHROPIC_API_KEY='your-key-here'
  or
    echo 'ANTHROPIC_API_KEY=your-key-here' > .env
        """
    )

    parser.add_argument('--api-key', '-k', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
    parser.add_argument('--repo-path', '-r', default='.', help='Path to HaackLang repository (default: current directory)')

    # Operating modes (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--interactive', '-i', action='store_true', help='Interactive REPL mode (default)')
    mode_group.add_argument('--question', '-q', metavar='TEXT', help='Ask a question')
    mode_group.add_argument('--generate', '-g', metavar='SPEC', help='Generate code from specification')
    mode_group.add_argument('--analyze', '-a', metavar='FILE', help='Analyze a HaackLang file')
    mode_group.add_argument('--debug', '-d', metavar='FILE', help='Debug a HaackLang file')
    mode_group.add_argument('--explain', '-e', metavar='EXAMPLE', help='Explain an example program')

    args = parser.parse_args()

    # Load API key
    api_key = args.api_key or load_api_key()
    if not api_key:
        print("Error: No API key provided.")
        print("\nOptions:")
        print("  1. Set ANTHROPIC_API_KEY environment variable:")
        print("     export ANTHROPIC_API_KEY='your-key-here'")
        print("  2. Create a .env file:")
        print("     echo 'ANTHROPIC_API_KEY=your-key-here' > .env")
        print("  3. Use --api-key argument:")
        print("     python claude_haacklang_agent.py --api-key 'your-key-here'")
        sys.exit(1)

    # Initialize agent
    try:
        agent = ClaudeHaackLangAgent(api_key, args.repo_path)
    except Exception as e:
        print(f"Error initializing agent: {e}")
        sys.exit(1)

    # Execute based on mode
    if args.question:
        response = agent.chat(args.question, mode="assist")
        print(response)
    elif args.generate:
        response = agent.chat(args.generate, mode="generate")
        print(response)
    elif args.analyze:
        response = agent.analyze_file(args.analyze)
        print(response)
    elif args.debug:
        response = agent.debug_file(args.debug)
        print(response)
    elif args.explain:
        response = agent.get_example_explanation(args.explain)
        print(response)
    else:
        # Default to interactive mode
        interactive_mode(agent)


if __name__ == '__main__':
    main()
