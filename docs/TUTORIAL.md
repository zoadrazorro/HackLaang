# HaackLang Tutorial

Welcome to HaackLang! This tutorial will guide you through the core concepts of polyrhythmic, polylogical programming.

## Table of Contents
1. [What Makes HaackLang Different](#what-makes-haacklang-different)
2. [Your First Program](#your-first-program)
3. [Understanding Tracks](#understanding-tracks)
4. [Truth Values (BoolRhythm)](#truth-values-boolrhythm)
5. [Polylogical Operations](#polylogical-operations)
6. [Contexts](#contexts)
7. [Guards and Rhythmic Execution](#guards-and-rhythmic-execution)
8. [Functions](#functions)
9. [A Complete Example](#a-complete-example)

## What Makes HaackLang Different

Most programming languages use a single logic system (usually Boolean logic) evaluated at a single moment in time. HaackLang breaks this mold:

- **Multiple logics coexist**: Classical, fuzzy, and paraconsistent logic all operate simultaneously
- **Truth evolves rhythmically**: Different logical "tracks" update at different tempos
- **Contradiction is not an error**: Paraconsistent tracks can safely handle contradictory beliefs
- **Cognitive modeling**: The language is designed to model how minds actually reason

## Your First Program

Let's start with a simple HaackLang program:

```haack
# hello.haack
track main period 1 using classical

tv greeting = 0.8
print(greeting)
```

Run it:
```bash
./haackc hello.haack
```

Output:
```
TruthValue({main: 0.80, slow: 0.80, syncop: 0.80})
```

What happened?
1. We defined a track called `main` that fires every beat (period 1) using classical logic
2. We created a truth value `greeting` with initial value 0.8
3. We printed it, showing its values across all tracks

## Understanding Tracks

Tracks are the heart of HaackLang. Think of them as independent timelines, each with:
- A **period**: how often they update
- A **logic type**: how they reason

```haack
track main period 1 using classical      # Every beat, crisp logic
track slow period 4 using fuzzy          # Every 4 beats, gradual logic
track syncop period 7 using paraconsistent  # Every 7 beats, contradiction-tolerant
```

### Why Different Periods?

In cognitive science, different mental processes operate at different speeds:
- **Perception** (fast, period 1): Immediate sensory processing
- **Deliberation** (slow, period 4): Careful reasoning
- **Intuition** (irregular, period 7): Subconscious processing

HaackLang models this with tracks.

### Why Different Logics?

Different types of reasoning need different logical systems:
- **Classical**: For crisp decisions (yes/no, true/false)
- **Fuzzy**: For uncertainty and gradations (somewhat true, very true)
- **Paraconsistent**: For handling contradictions without breaking

## Truth Values (BoolRhythm)

In HaackLang, variables aren't just numbers or booleans—they're **truth values** that have different values on each track:

```haack
track main period 1 using classical
track slow period 4 using fuzzy

tv fear = 0.5

# Set track-specific values
fear.main = 0.9      # Immediate perception: high fear
fear.slow = 0.6      # Deliberate assessment: moderate fear
```

This models how you might *feel* very afraid (immediate perception) while *knowing* rationally that the danger is moderate (deliberate assessment).

## Polylogical Operations

Here's where HaackLang gets powerful. When you write:

```haack
tv danger = 0.8
tv threat = 0.7
tv assessment = danger and threat
```

The `and` operator **applies different logic on each track**:

### On the main track (classical):
```
assessment.main = (danger.main >= 0.5) AND (threat.main >= 0.5)
                = (0.8 >= 0.5) AND (0.7 >= 0.5)  
                = true AND true
                = 1.0
```

### On the slow track (fuzzy):
```
assessment.slow = min(danger.slow, threat.slow)
                = min(0.8, 0.7)
                = 0.7
```

### On the syncop track (paraconsistent):
```
assessment.syncop = min(danger.syncop, threat.syncop)  # simplified
                  = min(0.8, 0.7)
                  = 0.7
```

**One expression, three different logics.**

Try it yourself:

```haack
track main period 1 using classical
track slow period 4 using fuzzy

tv a = 0.7
tv b = 0.6
tv result = a and b

print(result)
```

## Contexts

Contexts let you organize related reasoning into cognitive domains:

```haack
track main period 1 using classical

context perception using logic classical {
    tv threat = 0.8
    print(threat)
}

context deliberation using logic fuzzy {
    tv confidence = 0.6
    tv doubt = 0.3
    tv decision = confidence and not doubt
    print(decision)
}
```

This models how different mental contexts use different logic styles.

## Guards and Rhythmic Execution

Guards let you execute code only when specific tracks fire:

```haack
track main period 1 using classical
track slow period 4 using fuzzy

tv fast_state = 0.8
tv slow_state = 0.6

# This executes EVERY beat (main fires every beat)
guard main fast_state > 0.5 {
    print(fast_state)
}

# This executes EVERY 4 BEATS (slow fires every 4 beats)
guard slow slow_state > 0.5 {
    print(slow_state)
}
```

This creates **rhythmic patterns** in execution—different parts of your code fire at different tempos.

## Functions

Functions work as you'd expect, but remember: they operate on truth values!

```haack
track main period 1 using classical
track slow period 4 using fuzzy

fn blend(a, b) {
    let result = a and b
    return result
}

tv trust = 0.7
tv hope = 0.8
tv outcome = blend(trust, hope)

print(outcome)
```

## A Complete Example

Let's put it all together with a real cognitive model:

```haack
# fear_response.haack
# Models how fear and courage interact to produce decisions

track main period 1 using classical
track slow period 4 using fuzzy
track syncop period 7 using paraconsistent

# Environmental inputs
tv threat = 0.8
tv resources = 0.6

# Set track-specific perceptions
threat.main = 0.9      # Immediate: high threat
threat.slow = 0.7      # Considered: moderate threat
threat.syncop = 0.5    # Intuitive: uncertain

resources.main = 0.7   # Immediate: good resources
resources.slow = 0.6   # Considered: adequate
resources.syncop = 0.8 # Intuitive: confident

# Cognitive states
tv fear = threat and not resources
tv courage = resources and not threat

# Decision context
context decision using logic fuzzy {
    tv should_flee = fear
    tv should_fight = courage
    
    print(should_flee)
    print(should_fight)
}

print(fear)
print(courage)
```

Run it and observe how fear and courage have different values on each track, reflecting different cognitive processes!

## Next Steps

Now you understand the basics! Try:

1. **Experiment** with different track periods
2. **Play** with logic types (classical, fuzzy, paraconsistent)
3. **Create** your own cognitive models
4. **Read** the specification (`haack_lang_specification.md`) for advanced features
5. **Study** the examples in `examples/` directory

## Key Takeaways

1. **Tracks** = Independent logical timelines with their own period and logic
2. **Truth values** = Variables with different values on each track
3. **Polylogical operators** = One operator, multiple logics
4. **Contexts** = Organizing reasoning into cognitive domains
5. **Guards** = Rhythmic conditional execution
6. **The Philosophy** = Logic is a toolbox, not a religion

Welcome to polyrhythmic, polylogical programming!
