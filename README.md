# HaackLang

A polyrhythmic, polylogical programming language.

## Overview

HaackLang is a groundbreaking programming language based on Susan Haack's philosophy of logical pluralism. It implements a computational model where:

- **Multiple logics coexist** - Classical, fuzzy, and paraconsistent logic operate in parallel
- **Truth evolves rhythmically** - Different logical tracks update at different tempos
- **Contradiction is not an error** - Paraconsistent tracks safely handle contradictory beliefs
- **Contexts define cognitive domains** - Different reasoning modes for different tasks

This is a reference implementation of the HaackLang compiler, providing:
- Lexer/tokenizer
- Parser with AST generation
- Interpreter for executing HaackLang programs
- Support for core language features

## Installation

```bash
# Clone the repository
git clone https://github.com/zoadrazorro/HackLaang.git
cd HackLaang

# The compiler is pure Python with no external dependencies
# You can run the compiler directly using python3 src/haackc/main.py <file>.
# Alternatively, you can add the src directory to your PATH:
export PATH="$PATH:$(pwd)/src"

# Optional: Install ClaudeHackLang Agent (AI coding assistant)
pip install -r requirements.txt
```

## Getting Started

This section provides a brief introduction to writing and running HaackLang programs.

### Your First HaackLang Program

Create a file named `hello.haack` and add the following code:

```haack
# Define a track that fires on every beat using classical logic.
track main period 1 using classical

# Define a slower track that fires every 4 beats using fuzzy logic.
track slow period 4 using fuzzy

# Declare a TruthValue (a multi-track variable) and initialize it.
# This sets the value of 'greeting' to 0.8 on all tracks.
tv greeting = 0.8

# On the 'main' track, the value will be treated as 1.0 (true)
# because classical logic rounds to the nearest integer.
# On the 'slow' track, the value remains 0.8 due to fuzzy logic.

# Print the TruthValue to the console.
# This will display the values of 'greeting' on all tracks.
print(greeting)
```

### Running the Program

You can run the program using the HaackLang compiler:

```bash
python3 src/haackc/main.py hello.haack
```

### Expected Output

The output will show the state of the `greeting` TruthValue across all defined tracks:

```
TruthValue({main: 1.00, slow: 0.80, syncop: 0.80})
```

## Language Features

### 1. Tracks - Temporal Logical Timelines

Tracks are independent logical timelines that update at different rates:

```haack
track main period 1 using classical      # Fires every beat
track slow period 4 using fuzzy          # Fires every 4 beats
track syncop period 7 using paraconsistent  # Fires every 7 beats
```

Each track has:
- A **period** - how often it updates
- A **logic type** - classical, fuzzy, or paraconsistent
- Independent state evolution

### 2. TruthValues (BoolRhythm) - Multi-Track Truth

TruthValues are variables that have different values across tracks:

```haack
tv fear = 0.5

# Set track-specific values
fear.main = 0.9      # Crisp perception
fear.slow = 0.6      # Gradual belief
fear.syncop = 0.3    # Intuitive feeling
```

### 3. Polylogical Operators

Logical operators work differently on each track:

```haack
tv danger = 0.7
tv threat = 0.8

# This AND uses:
# - Classical logic on main track (true/false)
# - Fuzzy logic on slow track (min operator)
# - Paraconsistent logic on syncop track
tv assessment = danger and threat
```

### 4. Contexts - Cognitive Domains

Contexts define different reasoning modes:

```haack
context perception using logic classical {
    tv threat = 0.8
}

context deliberation using logic fuzzy {
    tv confidence = 0.6
}
```

### 5. Guards - Rhythmic Conditionals

Guards execute only when specific tracks fire:

```haack
guard main fear > 0.5 {
    # Only runs when main track is active
    print(fear)
}

guard slow trust < 0.3 {
    # Only runs every 4 beats (slow track period)
    print(trust)
}
```

### 6. Functions

Define reusable logic:

```haack
fn blend(a, b) {
    let result = a and b
    return result
}

tv outcome = blend(0.7, 0.8)
```

## Examples

See the `examples/` directory for complete programs:

- `simple.haack` - Basic tracks and truth values
- `polylogical.haack` - Operators working across multiple logics
- `contexts.haack` - Cognitive contexts in action
- `guards.haack` - Rhythmic conditional execution
- `functions.haack` - Function definitions and calls

## CLI Usage

```bash
# Run a program
python3 src/haackc/main.py program.haack

# Verbose output (shows tokens, AST, execution trace)
python3 src/haackc/main.py -v program.haack

# Lex only (output tokens)
python3 src/haackc/main.py --lex-only program.haack

# Parse only (output AST)
python3 src/haackc/main.py --parse-only program.haack
```

## AI Coding Assistant

HaackLang includes an intelligent AI coding assistant powered by Claude (Anthropic). The ClaudeHackLang Agent can help you:
- Write HaackLang code from natural language descriptions
- Debug and fix errors in your programs
- Explain complex polylogical concepts
- Analyze existing code
- Learn from interactive examples

**Quick Start:**
```bash
# Set up your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Launch interactive mode
python claude_haacklang_agent.py

# Or ask a quick question
python claude_haacklang_agent.py -q "How do I use fuzzy logic in HaackLang?"

# Generate code
python claude_haacklang_agent.py -g "Create a program that models threat assessment"

# Analyze a file
python claude_haacklang_agent.py -a examples/simple.haack
```

**See [docs/AGENT.md](docs/AGENT.md) for complete documentation.**

## Architecture

The compiler consists of several modules:

- **Lexer** (`src/haackc/lexer/`) - Tokenizes source code
- **Parser** (`src/haackc/parser/`) - Builds abstract syntax tree
- **Runtime** (`src/haackc/runtime/`) - Core data structures (Tracks, TruthValues, Contexts)
- **Interpreter** (`src/haackc/interpreter/`) - Executes the AST

## Language Specification

For the complete language specification, see `haack_lang_specification.md`. This comprehensive document covers:

- Philosophical foundations (Susan Haack's logical pluralism)
- Formal semantics
- Complete grammar (EBNF)
- HLVM bytecode specification
- Standard library
- Advanced features (meta-logic, rhythmic operators, etc.)

## Current Status

This reference implementation supports:

✅ Track declarations with periods and logic types  
✅ TruthValue (BoolRhythm) variables  
✅ Track-qualified variable access (e.g., `fear.main`)  
✅ Polylogical operators (and, or, not)  
✅ Arithmetic and comparison operators  
✅ Context declarations  
✅ Guard statements  
✅ Functions with parameters and return values  
✅ If/else statements  
✅ Basic expression evaluation  

## Future Enhancements

The specification defines many advanced features not yet implemented:

- Meta-logic operators (`@meta`, `@coh`, `@conflict`)
- Rhythmic operators (`hold`, `pulse`, `sync`, `echo`, `interfere`)
- Paraconsistent branching (`if!!`)
- Rules and rule-based execution
- Module system
- HLVM bytecode compilation
- Full standard library
- Beat-gated execution loops

## Contributing to Language Development

Contributions are welcome! HaackLang provides an **AI-powered coding assistant** (ClaudeHaackLang Agent) to help you contribute effectively to language development.

### Using the AI Agent for Development

The ClaudeHaackLang Agent can help you:

- Understand the compiler architecture and codebase
- Implement new language features from the specification
- Write comprehensive tests for your contributions
- Debug complex issues in the compiler
- Generate documentation and examples

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up your API key (get one at https://console.anthropic.com/)
export ANTHROPIC_API_KEY='your-api-key-here'

# Get help implementing a feature
python claude_haacklang_agent.py -q "How do I implement rhythmic operators in the interpreter?"

# Generate code for a feature
python claude_haacklang_agent.py -g "Implement the @meta coherence operator"

# Interactive development mode
python claude_haacklang_agent.py
```

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidance on using the AI agent for language development, and **[docs/AGENT.md](docs/AGENT.md)** for complete agent documentation.

### Contribution Areas

- Implementing additional language features from the specification
- Writing more example programs
- Improving error messages
- Adding unit tests
- Optimizing the interpreter
- Documentation improvements

### Language Specification

The complete HaackLang specification is available in **[readme/specifications.md](readme/specifications.md)**, covering:

- Philosophical foundations (Susan Haack's logical pluralism)
- Formal semantics and grammar (EBNF)
- Core language features (Tracks, BoolRhythm, Contexts)
- HLVM bytecode specification
- Standard library definitions
- Advanced features and future enhancements

## License

See LICENSE file for details.

## Philosophy

HaackLang embodies Susan Haack's insight that "logic is a toolbox, not a religion." Different kinds of reasoning require different logical tools. This language makes that philosophy executable, allowing:

- Classical logic for crisp decisions
- Fuzzy logic for gradations and uncertainty  
- Paraconsistent logic for contradictions without collapse
- Temporal pluralism for multi-speed reasoning
- Meta-logic for reasoning about reasoning

It's a language built for **minds**, not machines.

## References

- Susan Haack, *Philosophy of Logics* (1978)
- HaackLang language specification: [readme/specifications.md](readme/specifications.md)
- HaackLang whitepaper: [HaackLang - A Polyrhythmic Programming Language.pdf](HaackLang%20-%20A%20Polyrhythmic%20Programming%20Language.pdf)
- AI Coding Assistant documentation: [docs/AGENT.md](docs/AGENT.md)
