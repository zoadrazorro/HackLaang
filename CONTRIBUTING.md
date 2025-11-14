# Contributing to HaackLang

Thank you for your interest in contributing to HaackLang! This document provides guidelines for contributing to the reference compiler implementation.

## Using ClaudeHaackLang Agent for Language Development

**NEW**: HaackLang now includes an AI-powered coding assistant that can help you contribute to language development!

The **ClaudeHaackLang Agent** is specifically trained on HaackLang's unique polyrhythmic, polylogical architecture and can assist with:

- **Understanding the codebase**: Get explanations of how the compiler works
- **Implementing new features**: Generate code for features from the specification
- **Writing tests**: Create test cases for new or existing functionality
- **Debugging issues**: Identify and fix bugs in the compiler
- **Code review**: Get suggestions for improving your contributions
- **Documentation**: Help write clear documentation and examples

### Quick Start with the AI Agent

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Start the interactive agent
python claude_haacklang_agent.py
```

### Using the Agent for Development

**Example 1: Understanding a Component**
```bash
python claude_haacklang_agent.py -q "Explain how the Track system is implemented in the runtime module"
```

**Example 2: Implementing a New Feature**
```bash
python claude_haacklang_agent.py -g "Implement the 'hold' rhythmic operator that freezes a value for N beats"
```

**Example 3: Writing Tests**
```bash
python claude_haacklang_agent.py -q "Generate unit tests for the fuzzy logic operators in the interpreter"
```

**Example 4: Debugging**
```bash
python claude_haacklang_agent.py -d src/haackc/parser/parser.py
```

### Interactive Development Workflow

The agent excels at iterative development:

```bash
python claude_haacklang_agent.py

You: I want to implement meta-logic operators. Where should I start?
[Agent explains the architecture and suggests starting points]

You: Show me how to add @meta operator support to the lexer
[Agent generates lexer changes]

You: Now show me the parser changes needed
[Agent generates parser modifications]

You: Generate test cases for these changes
[Agent creates comprehensive tests]
```

### Best Practices with the AI Agent

1. **Start with questions**: Ask the agent to explain before implementing
2. **Iterative refinement**: Build features step by step with agent guidance
3. **Verify suggestions**: Always test agent-generated code
4. **Reference the spec**: Ask the agent to cite the language specification
5. **Code review**: Use the agent to review your changes before submitting PRs

See [docs/AGENT.md](docs/AGENT.md) for complete documentation on using the ClaudeHaackLang Agent.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/HackLaang.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

```bash
# No dependencies needed - pure Python
cd HackLaang

# Run tests
python3 tests/test_compiler.py

# Run examples
./haackc examples/simple.haack
```

## Project Structure

```
HackLaang/
├── src/haackc/           # Compiler source code
│   ├── lexer/            # Lexical analysis
│   ├── parser/           # Syntax analysis & AST
│   ├── runtime/          # Runtime structures (Tracks, TruthValues, Contexts)
│   ├── interpreter/      # AST interpreter
│   └── main.py           # CLI entry point
├── tests/                # Unit tests
├── examples/             # Example programs
└── docs/                 # Additional documentation
```

## How to Contribute

### 1. Bug Reports

If you find a bug:
- Check if it's already reported in Issues
- If not, create a new issue with:
  - Clear description of the bug
  - Steps to reproduce
  - Expected vs actual behavior
  - HaackLang code that triggers the bug
  - Your Python version

### 2. Feature Requests

For new features:
- Check the specification (`haack_lang_specification.md`) to see if it's already defined
- Create an issue describing:
  - The feature you'd like
  - Why it's useful
  - How it relates to the specification

### 3. Code Contributions

#### Adding New Language Features

Many features from the specification are not yet implemented. Priority areas:

**High Priority:**
- Meta-logic operators (`@meta`, `@coh`, `@conflict`)
- Rhythmic operators (`hold`, `pulse`, `sync`, `echo`)
- Enhanced contexts (inheritance, priority)
- Module system
- Better error messages with source location

**Medium Priority:**
- Paraconsistent branching (`if!!`)
- While loops
- For loops
- List/array support
- String manipulation

**Advanced:**
- HLVM bytecode compilation
- Standard library modules
- Debugger integration
- IDE support (LSP)

#### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for classes and functions
- Keep functions focused and modular

#### Testing

- Add tests for new features
- Ensure all existing tests pass
- Test with the example programs

```bash
# Run all tests
python3 tests/test_compiler.py

# Test all examples
for f in examples/*.haack; do
    echo "Testing $f"
    ./haackc "$f"
done
```

### 4. Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify confusing sections
- Add more examples
- Create tutorials
- Improve API documentation

### 5. Examples

Adding example programs helps users understand the language:
- Create `.haack` files in `examples/`
- Include comments explaining the concepts
- Demonstrate specific features
- Show practical use cases

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation for any changes
3. Add tests for new features
4. Create a pull request with:
   - Clear title and description
   - Link to related issues
   - Summary of changes

## Design Principles

When contributing, keep these principles in mind:

1. **Minimal Changes**: Make the smallest changes necessary to achieve the goal
2. **Specification Compliance**: Follow the language specification
3. **Clarity Over Cleverness**: Readable code is better than clever code
4. **Philosophy Matters**: Remember HaackLang is about logical pluralism and polyrhythmic reasoning

## Language Design Decisions

Some areas require careful consideration:

### Track Semantics
- How should tracks interact?
- What happens when tracks disagree?
- How should Beat scheduling work?

### Logic Systems
- Classical logic: strict true/false
- Fuzzy logic: continuous [0,1]
- Paraconsistent logic: allows contradictions

### Error Handling
- When should the compiler error vs. warning?
- How to handle undefined behavior?
- What errors are recoverable?

## Questions?

- Open an issue for discussion
- Check existing issues and PRs
- Read the specification document

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Assume good intentions
- Help others learn

Thank you for contributing to HaackLang!
