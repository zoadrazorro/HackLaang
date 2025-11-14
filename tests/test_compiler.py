"""
Unit tests for HaackLang compiler.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from haackc.lexer import Lexer, TokenType
from haackc.parser import Parser
from haackc.interpreter import Interpreter


class TestLexer(unittest.TestCase):
    """Test the lexer."""
    
    def test_keywords(self):
        """Test keyword tokenization."""
        source = "track period using logic classical fuzzy paraconsistent"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.TRACK)
        self.assertEqual(tokens[1].type, TokenType.PERIOD)
        self.assertEqual(tokens[2].type, TokenType.USING)
        self.assertEqual(tokens[3].type, TokenType.LOGIC)
        self.assertEqual(tokens[4].type, TokenType.CLASSICAL)
        self.assertEqual(tokens[5].type, TokenType.FUZZY)
        self.assertEqual(tokens[6].type, TokenType.PARACONSISTENT)
    
    def test_numbers(self):
        """Test number tokenization."""
        source = "42 3.14 0.5"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, 3.14)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, 0.5)
    
    def test_operators(self):
        """Test operator tokenization."""
        source = "+ - * / == != < > <= >= and or not"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT,
            TokenType.LE, TokenType.GE, TokenType.AND, TokenType.OR, TokenType.NOT
        ]
        
        for i, expected_type in enumerate(expected):
            self.assertEqual(tokens[i].type, expected_type)


class TestParser(unittest.TestCase):
    """Test the parser."""
    
    def test_track_declaration(self):
        """Test track declaration parsing."""
        source = "track main period 1 using classical"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.declarations), 1)
        decl = ast.declarations[0]
        self.assertEqual(decl.name, "main")
        self.assertEqual(decl.period, 1)
    
    def test_truthvalue_declaration(self):
        """Test truth value declaration parsing."""
        source = "tv fear = 0.5"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.declarations), 1)
        decl = ast.declarations[0]
        self.assertEqual(decl.name, "fear")


class TestInterpreter(unittest.TestCase):
    """Test the interpreter."""
    
    def test_track_creation(self):
        """Test track creation."""
        source = "track main period 1 using classical"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertIn("main", interpreter.tracks)
        self.assertEqual(interpreter.tracks["main"].period, 1)
    
    def test_truthvalue_creation(self):
        """Test truth value creation."""
        source = """
        track main period 1 using classical
        tv fear = 0.5
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertIn("fear", interpreter.truthvalues)
        self.assertEqual(interpreter.truthvalues["fear"].get("main"), 0.5)
    
    def test_polylogical_and(self):
        """Test polylogical AND operation."""
        source = """
        track main period 1 using classical
        track slow period 4 using fuzzy
        tv a = 0.7
        tv b = 0.6
        tv result = a and b
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        result = interpreter.truthvalues["result"]
        # Classical: 0.7 >= 0.5 AND 0.6 >= 0.5 = True = 1.0
        self.assertEqual(result.get("main"), 1.0)
        # Fuzzy: min(0.7, 0.6) = 0.6
        self.assertEqual(result.get("slow"), 0.6)


if __name__ == "__main__":
    unittest.main()
