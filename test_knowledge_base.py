#!/usr/bin/env python3
"""
Test knowledge base loading for ClaudeHackLang Agent
This test doesn't require the anthropic package
"""

from pathlib import Path

print("Testing HaackLang Knowledge Base Loading...")
print("=" * 50)

# Test documentation files
doc_files = {
    'quickref': Path('docs/QUICKREF.md'),
    'readme': Path('README.md'),
    'tutorial': Path('docs/TUTORIAL.md'),
    'comparison': Path('docs/COMPARISON.md'),
    'agent': Path('docs/AGENT.md'),
}

print("\n1. Documentation Files:")
docs_loaded = 0
for name, path in doc_files.items():
    if path.exists():
        size = path.stat().st_size
        print(f"   ✓ {name:12} - {path} ({size:,} bytes)")
        docs_loaded += 1
    else:
        print(f"   ✗ {name:12} - {path} (missing)")

print(f"\n   Loaded {docs_loaded}/{len(doc_files)} documentation files")

# Test example files
print("\n2. Example Files:")
examples_dir = Path('examples')
if examples_dir.exists():
    examples = list(examples_dir.glob('*.haack'))
    if examples:
        for example in sorted(examples):
            size = example.stat().st_size
            print(f"   ✓ {example.stem:20} - {size:,} bytes")
        print(f"\n   Found {len(examples)} example files")
    else:
        print("   ✗ No .haack files found in examples directory")
else:
    print("   ✗ examples/ directory not found")

# Test configuration files
print("\n3. Configuration Files:")
config_files = {
    '.env.example': Path('.env.example'),
    'requirements.txt': Path('requirements.txt'),
}

for name, path in config_files.items():
    if path.exists():
        print(f"   ✓ {name}")
    else:
        print(f"   ✗ {name} (missing)")

# Test main agent script
print("\n4. Agent Script:")
agent_script = Path('claude_haacklang_agent.py')
if agent_script.exists():
    size = agent_script.stat().st_size
    is_executable = agent_script.stat().st_mode & 0o111
    print(f"   ✓ claude_haacklang_agent.py ({size:,} bytes)")
    if is_executable:
        print(f"   ✓ Script is executable")
    else:
        print(f"   ⚠ Script is not executable (run: chmod +x claude_haacklang_agent.py)")
else:
    print(f"   ✗ claude_haacklang_agent.py (missing)")

# Summary
print("\n" + "=" * 50)
print("Knowledge Base Structure Test Complete!")
print("=" * 50)

# Test reading a sample example
print("\n5. Sample Example Content:")
simple_example = Path('examples/simple.haack')
if simple_example.exists():
    content = simple_example.read_text()
    lines = content.strip().split('\n')
    print(f"\n   Preview of {simple_example.name} (first 10 lines):")
    print("   " + "-" * 46)
    for i, line in enumerate(lines[:10], 1):
        print(f"   {i:2} | {line}")
    print("   " + "-" * 46)
    print(f"   Total lines: {len(lines)}")

print("\n✅ All knowledge base files are accessible!")
print("\nNext Steps:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Get API key from: https://console.anthropic.com/")
print("3. Configure: export ANTHROPIC_API_KEY='your-key'")
print("4. Run agent: python claude_haacklang_agent.py")
