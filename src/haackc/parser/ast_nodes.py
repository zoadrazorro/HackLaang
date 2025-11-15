"""
AST Node definitions for HaackLang.
"""

from typing import Any, List, Optional, Dict
from enum import Enum


class LogicType(Enum):
    """
    Enumeration of the types of logic supported by HaackLang.
    """
    CLASSICAL = "classical"
    FUZZY = "fuzzy"
    PARACONSISTENT = "paraconsistent"


class ASTNode:
    """
    Base class for all AST nodes.

    Attributes:
        line (int): The line number where the node appears in the source code.
        column (int): The column number where the node appears in the source code.
    """
    def __init__(self, line: int = 0, column: int = 0):
        self.line = line
        self.column = column


class Program(ASTNode):
    """
    Root node representing a complete program.

    Attributes:
        declarations (List[ASTNode]): A list of top-level declarations in the program.
    """
    def __init__(self, declarations: List[ASTNode], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.declarations = declarations


class TrackDecl(ASTNode):
    """
    Track declaration: track name period N phase M using logic.

    Attributes:
        name (str): The name of the track.
        period (int): The period of the track.
        phase (int): The phase of the track.
        logic (LogicType): The logic system used by the track.
    """
    def __init__(self, name: str, period: int, phase: int = 0, 
                 logic: LogicType = LogicType.CLASSICAL, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.period = period
        self.phase = phase
        self.logic = logic


class ContextDecl(ASTNode):
    """
    Context declaration with logic and rules.

    Attributes:
        name (str): The name of the context.
        logic (Optional[LogicType]): The logic system used by the context.
        track (Optional[str]): The track associated with the context.
        body (List[ASTNode]): A list of declarations within the context.
    """
    def __init__(self, name: str, logic: Optional[LogicType], track: Optional[str],
                 body: List[ASTNode], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.logic = logic
        self.track = track
        self.body = body


class TruthValueDecl(ASTNode):
    """
    Truth value (BoolRhythm) variable declaration.

    Attributes:
        name (str): The name of the truth value variable.
        initial_value (Optional['Expression']): The initial value of the variable.
        restricted_tracks (Optional[List[str]]): A list of tracks to which the
            variable is restricted.
    """
    def __init__(self, name: str, initial_value: Optional['Expression'] = None,
                 restricted_tracks: Optional[List[str]] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.initial_value = initial_value
        self.restricted_tracks = restricted_tracks


class Assignment(ASTNode):
    """
    Variable assignment.

    Attributes:
        target (str): The name of the variable being assigned.
        track (Optional[str]): The track in which the assignment occurs.
        value (Expression): The value being assigned to the variable.
    """
    def __init__(self, target: str, track: Optional[str], value: 'Expression',
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.target = target
        self.track = track
        self.value = value


class Expression(ASTNode):
    """
    Base class for all expression nodes.
    """
    pass


class NumberLiteral(Expression):
    """
    Numeric literal.

    Attributes:
        value (float): The value of the number.
    """
    def __init__(self, value: float, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value


class BoolLiteral(Expression):
    """
    Boolean literal.

    Attributes:
        value (bool): The value of the boolean.
    """
    def __init__(self, value: bool, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value


class Variable(Expression):
    """
    Variable reference.

    Attributes:
        name (str): The name of the variable.
        track (Optional[str]): The track from which to read the variable's value.
    """
    def __init__(self, name: str, track: Optional[str] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.track = track


class BinaryOp(Expression):
    """
    Binary operation.

    Attributes:
        operator (str): The binary operator.
        left (Expression): The left operand.
        right (Expression): The right operand.
    """
    def __init__(self, operator: str, left: Expression, right: Expression,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.operator = operator
        self.left = left
        self.right = right


class UnaryOp(Expression):
    """
    Unary operation.

    Attributes:
        operator (str): The unary operator.
        operand (Expression): The operand.
    """
    def __init__(self, operator: str, operand: Expression, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand


class FunctionCall(Expression):
    """
    Function call.

    Attributes:
        name (str): The name of the function.
        args (List[Expression]): A list of arguments to the function.
    """
    def __init__(self, name: str, args: List[Expression], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.args = args


class IfStatement(ASTNode):
    """
    If statement.

    Attributes:
        condition (Expression): The condition to be evaluated.
        then_body (List[ASTNode]): The block of code to execute if the condition is true.
        else_body (Optional[List[ASTNode]]): The block of code to execute if the
            condition is false.
        paraconsistent (bool): Whether the if statement is paraconsistent.
    """
    def __init__(self, condition: Expression, then_body: List[ASTNode],
                 else_body: Optional[List[ASTNode]] = None, paraconsistent: bool = False,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
        self.paraconsistent = paraconsistent


class GuardStatement(ASTNode):
    """
    Guard statement: guard track condition { body }.

    Attributes:
        track (str): The track to which the guard applies.
        condition (Expression): The condition to be met for the guard to pass.
        body (List[ASTNode]): The block of code to execute if the guard passes.
    """
    def __init__(self, track: str, condition: Expression, body: List[ASTNode],
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.track = track
        self.condition = condition
        self.body = body


class RuleDecl(ASTNode):
    """
    Rule declaration.

    Attributes:
        name (str): The name of the rule.
        body (List[ASTNode]): The block of code that defines the rule.
    """
    def __init__(self, name: str, body: List[ASTNode], line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.body = body


class FunctionDecl(ASTNode):
    """
    Function declaration.

    Attributes:
        name (str): The name of the function.
        params (List[str]): A list of parameter names.
        body (List[ASTNode]): The block of code that defines the function.
    """
    def __init__(self, name: str, params: List[str], body: List[ASTNode],
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.body = body


class ReturnStatement(ASTNode):
    """
    Return statement.

    Attributes:
        value (Optional[Expression]): The value to be returned.
    """
    def __init__(self, value: Optional[Expression] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value


class ExpressionStatement(ASTNode):
    """
    Statement consisting of just an expression.

    Attributes:
        expression (Expression): The expression that makes up the statement.
    """
    def __init__(self, expression: Expression, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.expression = expression
