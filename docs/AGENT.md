# ClaudeHackLang Agent

An intelligent AI coding assistant for HaackLang, powered by Claude (Anthropic's advanced language model).

## Overview

The ClaudeHackLang Agent helps you write, debug, and understand HaackLang programs. It leverages Claude's advanced reasoning capabilities along with deep knowledge of HaackLang's unique polyrhythmic, polylogical programming model.

## Features

- **Code Generation**: Generate HaackLang programs from natural language descriptions
- **Code Analysis**: Understand how existing HaackLang code works
- **Debugging**: Identify and fix errors in HaackLang programs
- **Explanations**: Get detailed explanations of HaackLang concepts
- **Interactive Mode**: REPL-style interface for ongoing conversations
- **Example Explorer**: Learn from built-in HaackLang examples
- **Knowledge Base**: Automatically loads HaackLang documentation and examples

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `anthropic` - Claude API client
- `python-dotenv` - For .env file support (optional)

### 2. Configure API Key

You need an Anthropic API key to use the agent. Get one at: https://console.anthropic.com/

There are three ways to provide your API key:

#### Option A: Environment Variable (Recommended)
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

#### Option B: .env File
Create a `.env` file in the HackLaang directory:
```bash
echo 'ANTHROPIC_API_KEY=your-api-key-here' > .env
```

Or use the example:
```bash
cp .env.example .env
# Edit .env and add your key
```

#### Option C: Command Line Argument
```bash
python claude_haacklang_agent.py --api-key 'your-api-key-here'
```

### 3. Make Script Executable (Optional)

```bash
chmod +x claude_haacklang_agent.py
```

## Usage

### Interactive Mode

The default mode is an interactive REPL where you can chat with the agent:

```bash
python claude_haacklang_agent.py
```

**Interactive Commands:**
- `/help` - Show available commands
- `/examples` - List all available HaackLang examples
- `/example <name>` - Get explanation of a specific example
- `/analyze <file>` - Analyze a HaackLang file
- `/debug <file>` - Debug a HaackLang file
- `/reset` - Reset the conversation history
- `/quit` - Exit the agent

**Example Session:**
```
You: How do I create a track with fuzzy logic?

Claude: To create a track with fuzzy logic in HaackLang, use the following syntax:

```haack
track <name> period <N> using fuzzy
```

For example:
```haack
track reasoning period 4 using fuzzy
```

This creates a track named "reasoning" that fires every 4 beats and uses fuzzy logic
for operations on that track...

You: /example polylogical

Claude: Let me explain the polylogical example...
```

### Command-Line Modes

#### Ask a Question
```bash
python claude_haacklang_agent.py -q "How do I use guards in HaackLang?"
```

#### Generate Code
```bash
python claude_haacklang_agent.py -g "Create a program that models emotional states with three different logical perspectives"
```

#### Analyze a File
```bash
python claude_haacklang_agent.py -a examples/simple.haack
```

#### Debug a File
```bash
python claude_haacklang_agent.py -d myprogram.haack
```

#### Explain an Example
```bash
python claude_haacklang_agent.py -e polylogical
```

## How It Works

### Knowledge Base

The agent automatically loads:
1. **Documentation**: Quick reference, README, tutorial, and comparison guides
2. **Examples**: All `.haack` files from the examples directory
3. **Context**: Understanding of HaackLang's philosophical foundations

This knowledge is injected into Claude's system prompt, giving it deep expertise in HaackLang.

### Assistant Modes

The agent operates in different modes depending on your request:

1. **Assist Mode** (default): General help and conversation
2. **Explain Mode**: Detailed explanations of concepts or code
3. **Generate Mode**: Code generation from specifications
4. **Debug Mode**: Error identification and fixes
5. **Analyze Mode**: Code analysis and explanation

### Conversation Memory

In interactive mode, the agent maintains conversation history, allowing for:
- Follow-up questions
- Iterative code refinement
- Contextual responses

Use `/reset` to clear the conversation history and start fresh.

## Examples

### Example 1: Generate a New Program

```bash
python claude_haacklang_agent.py -g "Create a program that uses three tracks with different periods to model a decision-making process under uncertainty"
```

The agent will generate a complete HaackLang program with:
- Track declarations
- Truth value definitions
- Polylogical operations
- Comments explaining the logic

### Example 2: Debug Existing Code

Create a file `test.haack`:
```haack
track main period 1 using classical
tv fear = 0.5
tv courage = fear and 0.7
print(courage)
```

Debug it:
```bash
python claude_haacklang_agent.py -d test.haack
```

The agent will analyze the code and identify any issues.

### Example 3: Interactive Learning

```bash
python claude_haacklang_agent.py

You: What's the difference between classical and fuzzy logic in HaackLang?
[Agent explains the differences]

You: Show me an example using both
[Agent generates example code]

You: How would I add a paraconsistent track?
[Agent shows how to add it]

You: /reset
You: /example polylogical
[Agent explains the polylogical example]
```

## Advanced Usage

### Custom Repository Path

If you want to use the agent from a different directory:

```bash
python claude_haacklang_agent.py --repo-path /path/to/HackLaang
```

### Scripting with the Agent

You can use the agent in your own Python scripts:

```python
from claude_haacklang_agent import ClaudeHaackLangAgent

# Initialize
agent = ClaudeHaackLangAgent(api_key='your-key', repo_path='.')

# Ask questions
response = agent.chat("How do guards work?", mode="explain")
print(response)

# Generate code
code = agent.chat("Create a simple fear-courage model", mode="generate")
print(code)

# Analyze a file
analysis = agent.analyze_file('examples/simple.haack')
print(analysis)
```

## Tips for Best Results

1. **Be Specific**: The more details you provide, the better the code generated
   - Good: "Create a program with 3 tracks (main at period 1 with classical logic, slow at period 4 with fuzzy logic, fast at period 2 with paraconsistent logic) that models threat assessment"
   - Less good: "Make a program about threats"

2. **Ask Follow-ups**: In interactive mode, refine your code iteratively
   - "Now add a guard that prints when threat > 0.7 on the main track"

3. **Use Examples**: Reference existing examples for context
   - "Create something similar to the polylogical example but for emotions"

4. **Explain Your Intent**: Share what you're trying to accomplish
   - "I want to model how different reasoning systems might evaluate the same situation"

5. **Request Explanations**: Ask the agent to explain its generated code
   - "Explain how the polylogical operations work in this code"

## Troubleshooting

### API Key Issues

**Error**: "No API key provided"
- **Solution**: Set ANTHROPIC_API_KEY environment variable or create .env file

**Error**: "APIError: 401"
- **Solution**: Check that your API key is valid and active

### Import Errors

**Error**: "ModuleNotFoundError: No module named 'anthropic'"
- **Solution**: Run `pip install anthropic`

### Knowledge Base Issues

**Error**: Example or documentation not found
- **Solution**: Make sure you're running the agent from the HackLaang directory, or use `--repo-path` to specify the correct path

## API Costs

The ClaudeHackLang Agent uses Claude Sonnet 4, which has the following pricing (as of 2025):
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

Typical costs:
- Simple question: ~$0.01-0.05
- Code generation: ~$0.05-0.15
- File analysis: ~$0.10-0.30

## Privacy & Security

- API calls are sent to Anthropic's servers
- Your code and questions are processed by Claude
- No data is stored by the agent locally beyond the conversation session
- Conversation history is reset when you close the agent
- Your API key should be kept secret (don't commit .env to git)

## Limitations

- Requires internet connection for API calls
- Depends on Claude's availability
- May occasionally generate code with minor syntax errors (always test!)
- Cannot execute HaackLang code (use the haackc compiler for that)
- Limited to Claude's knowledge cutoff date for general programming knowledge

## Future Enhancements

Potential future features:
- Automatic code execution and testing
- Integration with the HaackLang compiler for syntax checking
- Code completion suggestions
- Diff-based code editing
- Multi-file project support
- Custom example library
- Export conversations to markdown

## Contributing

To improve the agent:
1. Add more examples to the `examples/` directory
2. Enhance documentation in `docs/`
3. Submit issues or PRs with improvements

## License

Same as HaackLang (see LICENSE file).

## Support

For issues with:
- **The Agent**: Open an issue in the HackLaang repository
- **Claude API**: Contact Anthropic support
- **HaackLang Language**: See the main README.md

## Acknowledgments

- Built on Claude by Anthropic
- Inspired by HaackLang's philosophy of logical pluralism
- Powered by Susan Haack's insights on reasoning
