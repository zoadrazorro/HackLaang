# HaackLang Quick Reference

## Basic Syntax

### Comments
```haack
# This is a single-line comment
```

### Track Declarations
```haack
track <name> period <N> [phase <M>] [using <logic>]

# Examples:
track main period 1 using classical
track slow period 4 using fuzzy
track syncop period 7 using paraconsistent
```

**Logic Types:**
- `classical` - Boolean logic (true/false)
- `fuzzy` - Continuous logic [0, 1]
- `paraconsistent` - Contradiction-tolerant logic

### Truth Value Declarations
```haack
tv <name> [= <value>]

# Examples:
tv fear
tv courage = 0.7
tv threat = 0.5
```

### Track-Qualified Access
```haack
# Read from specific track
let x = fear.main

# Write to specific track
fear.slow = 0.6
```

## Operators

### Logical Operators
```haack
and    # Conjunction (track-specific logic)
or     # Disjunction (track-specific logic)
not    # Negation (track-specific logic)
```

### Arithmetic Operators
```haack
+      # Addition
-      # Subtraction
*      # Multiplication
/      # Division
```

### Comparison Operators
```haack
==     # Equal
!=     # Not equal
<      # Less than
<=     # Less than or equal
>      # Greater than
>=     # Greater than or equal
```

## Control Flow

### If Statements
```haack
if <condition> {
    # then body
}

if <condition> {
    # then body
} else {
    # else body
}
```

### Guard Statements
```haack
guard <track> <condition> {
    # Only executes when track fires AND condition is true
}

# Example:
guard main fear > 0.7 {
    print(fear)
}
```

## Contexts

```haack
context <name> [using logic <logic>] [using track <track>] {
    # Context body
}

# Examples:
context perception using logic classical {
    tv threat = 0.8
}

context deliberation using logic fuzzy {
    tv confidence = 0.6
}
```

## Functions

```haack
fn <name>(<params>) {
    # Function body
    [return <value>]
}

# Example:
fn blend(a, b) {
    let result = a and b
    return result
}

# Call:
tv outcome = blend(0.7, 0.8)
```

## Built-in Functions

```haack
print(value)    # Print value to stdout
```

## Data Types

### Numbers
```haack
42        # Integer
3.14      # Float
0.5       # Common for truth values
```

### Truth Values
```haack
tv fear = 0.7

# Truth values have components for each track:
# fear.main   - main track value
# fear.slow   - slow track value  
# fear.syncop - syncop track value
```

## Examples

### Simple Truth Value
```haack
track main period 1 using classical

tv danger = 0.8
print(danger)
```

### Polylogical Operation
```haack
track main period 1 using classical
track slow period 4 using fuzzy

tv a = 0.7
tv b = 0.6

# Uses classical AND on main, fuzzy AND on slow
tv result = a and b
print(result)
```

### Context-Based Reasoning
```haack
track main period 1 using classical

context planning using logic fuzzy {
    tv confidence = 0.6
    tv doubt = 0.3
    tv decision = confidence and not doubt
    print(decision)
}
```

### Rhythmic Guards
```haack
track main period 1 using classical
track slow period 4 using fuzzy

tv fast_state = 0.8
tv slow_state = 0.6

# Executes every beat (main period = 1)
guard main fast_state > 0.5 {
    print(fast_state)
}

# Executes every 4 beats (slow period = 4)
guard slow slow_state > 0.5 {
    print(slow_state)
}
```

## How Polylogical Operations Work

When you write:
```haack
tv result = a and b
```

The `and` operator applies **different logic on each track**:

**Main track (classical):**
- `result.main = (a.main >= 0.5) AND (b.main >= 0.5)`
- Returns 1.0 or 0.0

**Slow track (fuzzy):**
- `result.slow = min(a.slow, b.slow)`
- Returns continuous value [0, 1]

**Syncop track (paraconsistent):**
- `result.syncop = min(a.syncop, b.syncop)`
- Can represent contradictions

This is the core innovation: **one expression, multiple logics**.

## Common Patterns

### State Initialization
```haack
tv state = 0.0
state.main = 0.8
state.slow = 0.6
state.syncop = 0.4
```

### Conditional Logic
```haack
tv action = 0.0

if threat > 0.7 {
    action = 1.0
} else {
    action = 0.3
}
```

### Function-Based Logic
```haack
fn assess_danger(threat, resources) {
    let danger = threat and not resources
    return danger
}

tv danger_level = assess_danger(0.8, 0.3)
```

## Tips

1. **Use meaningful names** - `fear`, `courage`, `threat` are clearer than `x`, `y`, `z`
2. **Track periods matter** - Different periods create temporal interference patterns
3. **Logic types matter** - Choose classical for crisp decisions, fuzzy for gradations
4. **Guards are powerful** - Use them to create rhythmic patterns
5. **Contexts organize code** - Group related logic in contexts

## Further Reading

- Full specification: `haack_lang_specification.md`
- Examples: `examples/` directory
- Philosophy: Susan Haack's *Philosophy of Logics*
