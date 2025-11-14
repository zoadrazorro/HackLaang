"""
AST Node definitions for HaackLang.
"""

from typing import Any, List, Optional, Dict
from enum import Enum


class LogicType(Enum):
    """Types of logic supported by HaackLang."""
    CLASSICAL = "classical"
    FUZZY = "fuzzy"
    PARACONSISTENT = "paraconsistent"


class ASTNode:
    """Base class for all AST nodes."""
    def __init__(self, line: int = 0, column: int = 0):
        self.line = line
        self.column = column


class Program(ASTNode):
    """Root node representing a complete program."""
    def __init__(self, declarations: List[ASTNode], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.declarations = declarations


class TrackDecl(ASTNode):
    """Track declaration: track name period N using logic."""
    def __init__(self, name: str, period: int, phase: int = 0, 
                 logic: LogicType = LogicType.CLASSICAL, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.period = period
        self.phase = phase
        self.logic = logic


class ContextDecl(ASTNode):
    """Context declaration with logic and rules."""
    def __init__(self, name: str, logic: Optional[LogicType], track: Optional[str],
                 body: List[ASTNode], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.logic = logic
        self.track = track
        self.body = body


class TruthValueDecl(ASTNode):
    """Truth value (BoolRhythm) variable declaration."""
    def __init__(self, name: str, initial_value: Optional['Expression'] = None,
                 restricted_tracks: Optional[List[str]] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.initial_value = initial_value
        self.restricted_tracks = restricted_tracks


class Assignment(ASTNode):
    """Variable assignment."""
    def __init__(self, target: str, track: Optional[str], value: 'Expression',
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.target = target
        self.track = track
        self.value = value


class Expression(ASTNode):
    """Base class for expressions."""
    pass


class NumberLiteral(Expression):
    """Numeric literal."""
    def __init__(self, value: float, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value


class BoolLiteral(Expression):
    """Boolean literal."""
    def __init__(self, value: bool, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value


class Variable(Expression):
    """Variable reference."""
    def __init__(self, name: str, track: Optional[str] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.track = track


class BinaryOp(Expression):
    """Binary operation."""
    def __init__(self, operator: str, left: Expression, right: Expression,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.operator = operator
        self.left = left
        self.right = right


class UnaryOp(Expression):
    """Unary operation."""
    def __init__(self, operator: str, operand: Expression, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand


class FunctionCall(Expression):
    """Function call."""
    def __init__(self, name: str, args: List[Expression], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.args = args


class IfStatement(ASTNode):
    """If statement."""
    def __init__(self, condition: Expression, then_body: List[ASTNode],
                 else_body: Optional[List[ASTNode]] = None, paraconsistent: bool = False,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
        self.paraconsistent = paraconsistent


class GuardStatement(ASTNode):
    """Guard statement: guard track condition { body }."""
    def __init__(self, track: str, condition: Expression, body: List[ASTNode],
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.track = track
        self.condition = condition
        self.body = body


class RuleDecl(ASTNode):
    """Rule declaration."""
    def __init__(self, name: str, body: List[ASTNode], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.body = body


class FunctionDecl(ASTNode):
    """Function declaration."""
    def __init__(self, name: str, params: List[str], body: List[ASTNode],
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.body = body


class ReturnStatement(ASTNode):
    """Return statement."""
    def __init__(self, value: Optional[Expression] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value


class ExpressionStatement(ASTNode):
    """Statement consisting of just an expression."""
    def __init__(self, expression: Expression, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.expression = expression
