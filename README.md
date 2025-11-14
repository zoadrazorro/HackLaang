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
# Add to your PATH or run directly
export PATH="$PATH:$(pwd)/src"
```

## Quick Start

Create a simple HaackLang program (`hello.haack`):

```haack
# Define tracks with different periods and logics
track main period 1 using classical
track slow period 4 using fuzzy

# Declare a truth value
tv greeting = 0.8

# Print it
print(greeting)
```

Run it:

```bash
python3 src/haackc/main.py hello.haack
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

## Contributing

Contributions are welcome! Areas for contribution:

- Implementing additional language features from the specification
- Writing more example programs
- Improving error messages
- Adding unit tests
- Optimizing the interpreter
- Documentation improvements

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
- HaackLang specification document (`haack_lang_specification.md`)
- HaackLang whitepaper (`HaackLang - A Polyrhythmic Programming Language.pdf`)
