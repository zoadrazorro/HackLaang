# ClaudeHackLang Agent Quick Start Guide

Get up and running with the AI coding assistant in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install anthropic
```

Or install all recommended dependencies:
```bash
pip install -r requirements.txt
```

## Step 2: Get Your API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Create an API key
4. Copy your key (starts with `sk-ant-...`)

## Step 3: Configure the API Key

Choose one method:

### Method A: Environment Variable (Recommended for single session)
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

### Method B: .env File (Recommended for persistent use)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
echo 'ANTHROPIC_API_KEY=sk-ant-your-key-here' > .env
```

## Step 4: Run the Agent

### Interactive Mode (Recommended for beginners)
```bash
python claude_haacklang_agent.py
```

You'll see:
```
ClaudeHackLang Agent - Interactive Mode
==================================================
Commands:
  /help          - Show this help
  /examples      - List available examples
  /example <name> - Explain an example
  /analyze <file> - Analyze a HaackLang file
  /debug <file>   - Debug a HaackLang file
  /reset         - Reset conversation
  /quit          - Exit
==================================================

You:
```

### Try Your First Question
```
You: How do I create a track with fuzzy logic?

Claude: To create a track with fuzzy logic in HaackLang...
[detailed explanation with code examples]
```

## Quick Examples

### 1. Ask a Quick Question (No interaction mode)
```bash
python claude_haacklang_agent.py -q "What is a truth value in HaackLang?"
```

### 2. Generate Code
```bash
python claude_haacklang_agent.py -g "Create a program with two tracks that models uncertainty"
```

Output:
```haack
# HaackLang program modeling uncertainty
track main period 1 using classical
track uncertain period 3 using fuzzy

tv confidence = 0.6
tv doubt = 0.4
...
```

### 3. Analyze an Example
```bash
python claude_haacklang_agent.py -a examples/simple.haack
```

Output:
```
This program demonstrates basic HaackLang concepts:

1. Track Declarations: ...
2. Truth Values: ...
...
```

### 4. Debug Your Code
Create a file `myprogram.haack`:
```haack
track main period 1 using classical
tv fear = 0.8
print(fear)
```

Debug it:
```bash
python claude_haacklang_agent.py -d myprogram.haack
```

### 5. Explore Examples
```bash
# List all examples
python claude_haacklang_agent.py

You: /examples

Claude: Available examples: simple, polylogical, contexts, guards, functions, fear_model, decision_making

You: /example polylogical

Claude: [Detailed explanation of the polylogical example]
```

## Interactive Mode Commands

Once in interactive mode (`python claude_haacklang_agent.py`):

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all commands | `/help` |
| `/examples` | List available examples | `/examples` |
| `/example <name>` | Explain a specific example | `/example polylogical` |
| `/analyze <file>` | Analyze a file | `/analyze examples/simple.haack` |
| `/debug <file>` | Debug a file | `/debug mycode.haack` |
| `/reset` | Clear conversation history | `/reset` |
| `/quit` | Exit the agent | `/quit` |

## Common Use Cases

### Learning HaackLang
```
You: Explain the difference between classical and fuzzy logic

You: Show me an example of polylogical operations

You: What are guards used for?
```

### Writing Code
```
You: Create a program that models emotional states using three tracks

You: How do I use a guard statement?

You: Generate a function that combines two truth values
```

### Debugging
```
You: /debug my_program.haack

You: Why isn't my guard firing?

You: What's wrong with this syntax: tv fear = and courage
```

### Iterative Development
```
You: Create a simple program with one track

Claude: [generates code]

You: Now add a second track with fuzzy logic

Claude: [adds to existing code]

You: Add a guard that prints when a value exceeds 0.7

Claude: [adds guard]
```

## Tips for Better Results

1. **Be Specific**
   - ✗ "Make a program"
   - ✓ "Create a program with 3 tracks (periods 1, 4, 7) that models decision-making"

2. **Ask Follow-up Questions**
   - First: "Create a basic program"
   - Then: "Add a fuzzy track"
   - Then: "Explain how the polylogical operations work"

3. **Reference Examples**
   - "Create something like the fear_model example but for trust"

4. **Request Explanations**
   - "Explain the code you just generated"
   - "Why did you use fuzzy logic here?"

5. **Use the Right Mode**
   - Learning? Use interactive mode and ask questions
   - Quick task? Use command-line mode (`-q`, `-g`, `-a`, `-d`)
   - Exploring? Use `/examples` and `/example <name>`

## Troubleshooting

### "Error: No API key provided"
- Make sure you set ANTHROPIC_API_KEY
- Check for typos in your .env file
- Verify the key starts with `sk-ant-`

### "ModuleNotFoundError: No module named 'anthropic'"
```bash
pip install anthropic
```

### "API Error: 401"
- Your API key is invalid or expired
- Get a new key from https://console.anthropic.com/

### Agent gives wrong syntax
- HaackLang is a new language; Claude might occasionally make mistakes
- Always test generated code with: `python src/haackc/main.py yourfile.haack`
- Report issues so we can improve the agent's knowledge

### Slow responses
- Claude API calls take 2-10 seconds depending on complexity
- More complex requests (code generation) take longer than simple questions

## What's Next?

1. **Read the full documentation**: [docs/AGENT.md](docs/AGENT.md)
2. **Learn HaackLang**: [docs/QUICKREF.md](docs/QUICKREF.md)
3. **Try the examples**: `ls examples/`
4. **Read the philosophy**: `haack_lang_specification.md` (sections 1-3)
5. **Write your first program**: Ask the agent for help!

## Example Session

Here's a complete example session:

```bash
$ python claude_haacklang_agent.py
ClaudeHackLang Agent - Interactive Mode
...

You: I want to create a program that models fear and courage as opposing forces

Claude: Great! Let me help you create a program that models fear and courage.
Here's a HaackLang program that represents these opposing emotional states:

```haack
# Fear vs Courage Model
track main period 1 using classical
track emotional period 3 using fuzzy
track subconscious period 5 using paraconsistent

# Define the emotional states
tv fear = 0.6
tv courage = 0.4

# Set track-specific values
fear.main = 0.7          # Conscious fear
fear.emotional = 0.6     # Emotional fear (gradual)
fear.subconscious = 0.5  # Unconscious fear

courage.main = 0.3       # Conscious courage
courage.emotional = 0.4  # Emotional courage (gradual)
courage.subconscious = 0.5  # May coexist with fear!

# Compute the balance
tv balance = courage and not fear

# Guards to monitor states
guard main balance > 0.5 {
    print(balance)
}

guard emotional fear > 0.6 {
    print(fear)
}
```

This program uses:
1. Three tracks with different periods representing different cognitive layers
2. Track-qualified assignment to set different values across tracks
3. Polylogical operations (the `and not` uses different logic on each track)
4. Guards that fire at different rhythms to monitor the states

The paraconsistent track allows fear and courage to coexist without contradiction!

You: Can you add a function that calculates the overall emotional state?

Claude: Absolutely! Let me add a function that combines fear and courage to determine
the overall emotional state:

[... continues with enhanced code ...]

You: /quit
Goodbye!
```

## API Costs

Typical costs (approximate):
- Simple question: $0.01 - $0.05
- Code generation: $0.05 - $0.15
- File analysis: $0.10 - $0.30
- Interactive session (10-15 exchanges): $0.50 - $2.00

Current Claude Sonnet 4 pricing:
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

## Support

- **Issues**: Open an issue on GitHub
- **Questions**: Ask the agent itself!
- **Feedback**: Contribute to the project

---

**Ready to start?** Run: `python claude_haacklang_agent.py`
