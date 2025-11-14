#!/usr/bin/env python3
"""
Test script for ClaudeHackLang Agent
Tests knowledge base loading and basic structure (doesn't require API key)
"""

import sys
from pathlib import Path

# Test imports
try:
    from claude_haacklang_agent import HaackLangKnowledgeBase, load_api_key
    print("✓ Successfully imported agent modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test knowledge base loading
print("\nTesting Knowledge Base...")
try:
    kb = HaackLangKnowledgeBase('.')
    print("✓ Knowledge base initialized")

    # Check documentation loaded
    if kb.docs:
        print(f"✓ Loaded {len(kb.docs)} documentation files:")
        for doc_name in kb.docs.keys():
            print(f"  - {doc_name}")
    else:
        print("✗ No documentation loaded")

    # Check examples loaded
    if kb.examples:
        print(f"✓ Loaded {len(kb.examples)} example files:")
        for example_name in kb.examples.keys():
            print(f"  - {example_name}")
    else:
        print("✗ No examples loaded")

    # Test example retrieval
    examples_list = kb.list_examples()
    if examples_list:
        test_example = examples_list[0]
        example_code = kb.get_example(test_example)
        if example_code:
            print(f"✓ Successfully retrieved example '{test_example}'")
            print(f"  Length: {len(example_code)} characters")
        else:
            print(f"✗ Failed to retrieve example '{test_example}'")

    # Test context summary
    context = kb.get_context_summary()
    if context and len(context) > 100:
        print(f"✓ Generated context summary ({len(context)} characters)")
    else:
        print("✗ Context summary too short or empty")

except Exception as e:
    print(f"✗ Error testing knowledge base: {e}")
    sys.exit(1)

# Test API key loading (shouldn't fail if no key present)
print("\nTesting API Key Loading...")
try:
    api_key = load_api_key()
    if api_key:
        print(f"✓ API key found (length: {len(api_key)})")
    else:
        print("⚠ No API key found (expected if not configured)")
        print("  To configure: export ANTHROPIC_API_KEY='your-key' or create .env file")
except Exception as e:
    print(f"✗ Error loading API key: {e}")

# Test .env.example exists
print("\nChecking Configuration Files...")
if Path('.env.example').exists():
    print("✓ .env.example file exists")
else:
    print("✗ .env.example file missing")

if Path('requirements.txt').exists():
    print("✓ requirements.txt exists")
else:
    print("✗ requirements.txt missing")

if Path('docs/AGENT.md').exists():
    print("✓ Agent documentation exists")
else:
    print("✗ Agent documentation missing")

print("\n" + "="*50)
print("Knowledge Base Test Complete!")
print("="*50)
print("\nTo fully test the agent with API calls:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Set API key: export ANTHROPIC_API_KEY='your-key'")
print("3. Run agent: python claude_haacklang_agent.py")
