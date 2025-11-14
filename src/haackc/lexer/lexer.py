"""
Token definitions and Lexer implementation for HaackLang.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List, Optional
import re


class TokenType(Enum):
    """Token types for HaackLang."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords
    TRACK = auto()
    PERIOD = auto()
    PHASE = auto()
    USING = auto()
    LOGIC = auto()
    CONTEXT = auto()
    TV = auto()
    TRUTHVALUE = auto()
    META = auto()
    RULE = auto()
    FN = auto()
    MODULE = auto()
    IF = auto()
    ELSE = auto()
    GUARD = auto()
    WHEN = auto()
    ENTER = auto()
    EXIT = auto()
    RETURN = auto()
    LET = auto()
    
    # Logic types
    CLASSICAL = auto()
    FUZZY = auto()
    PARACONSISTENT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Comparison
    EQ = auto()           # ==
    NE = auto()           # !=
    LT = auto()           # <
    LE = auto()           # <=
    GT = auto()           # >
    GE = auto()           # >=
    ASSIGN = auto()       # =
    
    # Delimiters
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    COMMA = auto()        # ,
    SEMICOLON = auto()    # ;
    COLON = auto()        # :
    DOT = auto()          # .
    AT = auto()           # @
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token:
    """Represents a single token in HaackLang source code."""
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Lexer:
    """Lexical analyzer for HaackLang."""
    
    KEYWORDS = {
        'track': TokenType.TRACK,
        'period': TokenType.PERIOD,
        'phase': TokenType.PHASE,
        'using': TokenType.USING,
        'logic': TokenType.LOGIC,
        'context': TokenType.CONTEXT,
        'tv': TokenType.TV,
        'truthvalue': TokenType.TRUTHVALUE,
        'meta': TokenType.META,
        'rule': TokenType.RULE,
        'fn': TokenType.FN,
        'module': TokenType.MODULE,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'guard': TokenType.GUARD,
        'when': TokenType.WHEN,
        'enter': TokenType.ENTER,
        'exit': TokenType.EXIT,
        'return': TokenType.RETURN,
        'let': TokenType.LET,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
        'classical': TokenType.CLASSICAL,
        'fuzzy': TokenType.FUZZY,
        'paraconsistent': TokenType.PARACONSISTENT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def error(self, message: str):
        """Raise a lexer error."""
        raise SyntaxError(f"Lexer error at {self.line}:{self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Look at character at current position + offset."""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Consume and return current character."""
        if self.pos >= len(self.source):
            return None
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace but not newlines."""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comment."""
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (integer or float)."""
        start_line = self.line
        start_col = self.column
        num_str = ''
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.advance()
        
        try:
            value = float(num_str) if '.' in num_str else int(num_str)
        except ValueError:
            self.error(f"Invalid number: {num_str}")
        
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_string(self) -> Token:
        """Read a string literal."""
        start_line = self.line
        start_col = self.column
        
        quote = self.advance()  # consume opening quote
        string_val = ''
        
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                if next_char == 'n':
                    string_val += '\n'
                elif next_char == 't':
                    string_val += '\t'
                elif next_char == '\\':
                    string_val += '\\'
                elif next_char == quote:
                    string_val += quote
                else:
                    string_val += next_char
            else:
                string_val += self.advance()
        
        if not self.peek():
            self.error("Unterminated string")
        
        self.advance()  # consume closing quote
        return Token(TokenType.STRING, string_val, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start_line = self.line
        start_col = self.column
        ident = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        
        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        return Token(token_type, ident, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if not self.peek():
                break
            
            # Comments
            if self.peek() == '#':
                self.skip_comment()
                continue
            
            # Newlines
            if self.peek() == '\n':
                line, col = self.line, self.column
                self.advance()
                # Skip multiple newlines
                while self.peek() == '\n':
                    self.advance()
                continue
            
            # Numbers
            if self.peek().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.peek() in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Two-character operators
            line, col = self.line, self.column
            char = self.peek()
            next_char = self.peek(1)
            
            if char == '=' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQ, '==', line, col))
                continue
            
            if char == '!' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NE, '!=', line, col))
                continue
            
            if char == '<' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LE, '<=', line, col))
                continue
            
            if char == '>' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GE, '>=', line, col))
                continue
            
            # Single-character tokens
            char = self.advance()
            
            if char == '+':
                self.tokens.append(Token(TokenType.PLUS, char, line, col))
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, char, line, col))
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, char, line, col))
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, char, line, col))
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, char, line, col))
            elif char == '<':
                self.tokens.append(Token(TokenType.LT, char, line, col))
            elif char == '>':
                self.tokens.append(Token(TokenType.GT, char, line, col))
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, char, line, col))
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, char, line, col))
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, char, line, col))
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, char, line, col))
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, char, line, col))
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, char, line, col))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, char, line, col))
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, char, line, col))
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, char, line, col))
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, char, line, col))
            elif char == '@':
                self.tokens.append(Token(TokenType.AT, char, line, col))
            else:
                self.error(f"Unexpected character: {char!r}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
