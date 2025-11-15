#!/usr/bin/env python3
"""
HaackLang compiler CLI - compile and run HaackLang programs.
"""

import sys
import argparse
from pathlib import Path

from haackc.lexer import Lexer
from haackc.parser import Parser
from haackc.interpreter import Interpreter


def main():
    """
    Command-line interface for the HaackLang compiler.

    This function parses command-line arguments to compile and run a HaackLang
    source file. It handles file reading, lexing, parsing, and interpretation,
    providing options for verbose output and debugging stages.
    """
    parser = argparse.ArgumentParser(
        description='HaackLang Reference Compiler - A polyrhythmic, polylogical programming language'
    )
    parser.add_argument('file', help='HaackLang source file (.haack)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--lex-only', action='store_true', help='Only run lexer and print tokens')
    parser.add_argument('--parse-only', action='store_true', help='Only run parser and print AST')
    
    args = parser.parse_args()
    
    # Read source file
    source_path = Path(args.file)
    if not source_path.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    source = source_path.read_text()
    
    try:
        # Lexical analysis
        if args.verbose:
            print("=== Lexing ===")
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if args.verbose or args.lex_only:
            print(f"Tokens ({len(tokens)}):")
            for token in tokens:
                print(f"  {token}")
        
        if args.lex_only:
            return
        
        # Parsing
        if args.verbose:
            print("\n=== Parsing ===")
        parser = Parser(tokens)
        ast = parser.parse()
        
        if args.verbose or args.parse_only:
            print(f"AST:")
            print(f"  {ast}")
        
        if args.parse_only:
            return
        
        # Interpretation
        if args.verbose:
            print("\n=== Interpreting ===")
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        if args.verbose:
            print("\n=== Execution Complete ===")
            print(f"Tracks defined: {list(interpreter.tracks.keys())}")
            print(f"Truth values: {list(interpreter.truthvalues.keys())}")
    
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
