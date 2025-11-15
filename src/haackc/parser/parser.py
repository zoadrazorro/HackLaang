"""
Parser implementation for HaackLang.
"""

from typing import List, Optional
from ..lexer import Token, TokenType
from .ast_nodes import *


class Parser:
    """
    A recursive descent parser for the HaackLang programming language.

    The parser takes a list of tokens from the lexer and builds an Abstract
    Syntax Tree (AST) that represents the structure of the program.

    Attributes:
        tokens (List[Token]): The list of tokens to be parsed.
        pos (int): The current position in the token list.
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initializes the Parser with a list of tokens.

        Args:
            tokens (List[Token]): The tokens to be parsed.
        """
        self.tokens = tokens
        self.pos = 0
    
    def error(self, message: str):
        """
        Raises a parser error.

        Args:
            message (str): The error message to be raised.

        Raises:
            SyntaxError: Always raises a SyntaxError with the given message.
        """
        token = self.current()
        raise SyntaxError(f"Parse error at {token.line}:{token.column}: {message}")
    
    def current(self) -> Token:
        """
        Gets the current token.

        Returns:
            Token: The current token, or the EOF token if the end of the
                token list has been reached.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek(self, offset: int = 0) -> Token:
        """
        Looks ahead at a token without consuming it.

        Args:
            offset (int): The offset from the current position.

        Returns:
            Token: The token at the specified position, or the EOF token if
                the position is out of bounds.
        """
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self) -> Token:
        """
        Consumes and returns the current token.

        This method moves the parser's position forward by one token.

        Returns:
            Token: The token that was consumed.
        """
        token = self.current()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token
    
    def match(self, *types: TokenType) -> bool:
        """
        Checks if the current token matches any of the given types.

        Args:
            *types (TokenType): The token types to match against.

        Returns:
            bool: True if the current token's type is in the given types,
                False otherwise.
        """
        return self.current().type in types
    
    def expect(self, token_type: TokenType) -> Token:
        """
        Consumes a token of the expected type or raises an error.

        Args:
            token_type (TokenType): The expected type of the token.

        Returns:
            Token: The consumed token if it matches the expected type.

        Raises:
            SyntaxError: If the current token does not match the expected type.
        """
        if not self.match(token_type):
            self.error(f"Expected {token_type.name}, got {self.current().type.name}")
        return self.advance()
    
    def parse(self) -> Program:
        """
        Parses a complete HaackLang program.

        This method iterates through the tokens and parses top-level declarations
        until the end of the file is reached.

        Returns:
            Program: The root of the AST, representing the entire program.
        """
        declarations = []
        
        while not self.match(TokenType.EOF):
            decl = self.parse_declaration()
            if decl:
                declarations.append(decl)
        
        return Program(declarations=declarations)
    
    def parse_declaration(self) -> Optional[ASTNode]:
        """
        Parses a top-level declaration.

        This method determines the type of declaration and calls the
        appropriate parsing method.

        Returns:
            Optional[ASTNode]: The parsed declaration node, or None if no
                declaration is found.
        """
        token = self.current()
        
        if self.match(TokenType.TRACK):
            return self.parse_track_decl()
        elif self.match(TokenType.CONTEXT):
            return self.parse_context_decl()
        elif self.match(TokenType.TV, TokenType.TRUTHVALUE):
            return self.parse_truthvalue_decl()
        elif self.match(TokenType.RULE):
            return self.parse_rule_decl()
        elif self.match(TokenType.FN):
            return self.parse_function_decl()
        else:
            return self.parse_statement()
    
    def parse_track_decl(self) -> TrackDecl:
        """
        Parses a track declaration.

        Syntax: track <name> period <N> [phase <M>] [using <logic>]

        Returns:
            TrackDecl: The parsed track declaration node.
        """
        track_token = self.expect(TokenType.TRACK)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.PERIOD)
        period_token = self.expect(TokenType.NUMBER)
        period = int(period_token.value)
        
        phase = 0
        if self.match(TokenType.PHASE):
            self.advance()
            phase_token = self.expect(TokenType.NUMBER)
            phase = int(phase_token.value)
        
        logic = LogicType.CLASSICAL
        if self.match(TokenType.USING):
            self.advance()
            if self.match(TokenType.CLASSICAL):
                logic = LogicType.CLASSICAL
                self.advance()
            elif self.match(TokenType.FUZZY):
                logic = LogicType.FUZZY
                self.advance()
            elif self.match(TokenType.PARACONSISTENT):
                logic = LogicType.PARACONSISTENT
                self.advance()
            else:
                self.error("Expected logic type")
        
        return TrackDecl(
            name=name,
            period=period,
            phase=phase,
            logic=logic,
            line=track_token.line,
            column=track_token.column
        )
    
    def parse_context_decl(self) -> ContextDecl:
        """
        Parses a context declaration.

        Syntax: context <name> [using logic <logic> | using track <track>] { <body> }

        Returns:
            ContextDecl: The parsed context declaration node.
        """
        context_token = self.expect(TokenType.CONTEXT)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        logic = None
        track = None
        
        # Optional: using logic/track before body
        if self.match(TokenType.USING):
            self.advance()
            if self.match(TokenType.LOGIC):
                self.advance()
                if self.match(TokenType.CLASSICAL):
                    logic = LogicType.CLASSICAL
                    self.advance()
                elif self.match(TokenType.FUZZY):
                    logic = LogicType.FUZZY
                    self.advance()
                elif self.match(TokenType.PARACONSISTENT):
                    logic = LogicType.PARACONSISTENT
                    self.advance()
            elif self.match(TokenType.TRACK):
                self.advance()
                track_token = self.expect(TokenType.IDENTIFIER)
                track = track_token.value
        
        self.expect(TokenType.LBRACE)
        
        body = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_declaration()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RBRACE)
        
        return ContextDecl(
            name=name,
            logic=logic,
            track=track,
            body=body,
            line=context_token.line,
            column=context_token.column
        )
    
    def parse_truthvalue_decl(self) -> TruthValueDecl:
        """
        Parses a truth value declaration.

        Syntax: tv <name> [= <value>]

        Returns:
            TruthValueDecl: The parsed truth value declaration node.
        """
        tv_token = self.advance()  # TV or TRUTHVALUE
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        initial_value = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initial_value = self.parse_expression()
        
        return TruthValueDecl(
            name=name,
            initial_value=initial_value,
            line=tv_token.line,
            column=tv_token.column
        )
    
    def parse_rule_decl(self) -> RuleDecl:
        """
        Parses a rule declaration.

        Syntax: rule <name> { <body> }

        Returns:
            RuleDecl: The parsed rule declaration node.
        """
        rule_token = self.expect(TokenType.RULE)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LBRACE)
        
        body = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RBRACE)
        
        return RuleDecl(
            name=name,
            body=body,
            line=rule_token.line,
            column=rule_token.column
        )
    
    def parse_function_decl(self) -> FunctionDecl:
        """
        Parses a function declaration.

        Syntax: fn <name>(<params>) { <body> }

        Returns:
            FunctionDecl: The parsed function declaration node.
        """
        fn_token = self.expect(TokenType.FN)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        
        params = []
        while not self.match(TokenType.RPAREN):
            param_token = self.expect(TokenType.IDENTIFIER)
            params.append(param_token.value)
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        
        body = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RBRACE)
        
        return FunctionDecl(
            name=name,
            params=params,
            body=body,
            line=fn_token.line,
            column=fn_token.column
        )
    
    def parse_statement(self) -> Optional[ASTNode]:
        """
        Parses a statement.

        This method determines the type of statement and calls the
        appropriate parsing method.

        Returns:
            Optional[ASTNode]: The parsed statement node, or None if no
                statement is found.
        """
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.GUARD):
            return self.parse_guard_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.LET):
            return self.parse_let_statement()
        elif self.match(TokenType.IDENTIFIER):
            # Could be assignment or expression
            return self.parse_assignment_or_expression()
        else:
            # Try expression statement
            expr = self.parse_expression()
            return ExpressionStatement(expression=expr, line=expr.line, column=expr.column)
    
    def parse_if_statement(self) -> IfStatement:
        """
        Parses an if statement.

        Syntax: if <condition> { <body> } [else { <body> }]

        Returns:
            IfStatement: The parsed if statement node.
        """
        if_token = self.expect(TokenType.IF)
        
        condition = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        then_body = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
        self.expect(TokenType.RBRACE)
        
        else_body = None
        if self.match(TokenType.ELSE):
            self.advance()
            self.expect(TokenType.LBRACE)
            else_body = []
            while not self.match(TokenType.RBRACE, TokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
            self.expect(TokenType.RBRACE)
        
        return IfStatement(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            line=if_token.line,
            column=if_token.column
        )
    
    def parse_guard_statement(self) -> GuardStatement:
        """
        Parses a guard statement.

        Syntax: guard <track> <condition> { <body> }

        Returns:
            GuardStatement: The parsed guard statement node.
        """
        guard_token = self.expect(TokenType.GUARD)
        track_token = self.expect(TokenType.IDENTIFIER)
        track = track_token.value
        
        condition = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        body = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE)
        
        return GuardStatement(
            track=track,
            condition=condition,
            body=body,
            line=guard_token.line,
            column=guard_token.column
        )
    
    def parse_return_statement(self) -> ReturnStatement:
        """
        Parses a return statement.

        Syntax: return [<expression>]

        Returns:
            ReturnStatement: The parsed return statement node.
        """
        return_token = self.expect(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        
        return ReturnStatement(
            value=value,
            line=return_token.line,
            column=return_token.column
        )
    
    def parse_let_statement(self) -> Assignment:
        """
        Parses a let statement.

        Syntax: let <name> = <expression>

        Returns:
            Assignment: The parsed assignment node.
        """
        let_token = self.expect(TokenType.LET)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        
        return Assignment(
            target=name,
            track=None,
            value=value,
            line=let_token.line,
            column=let_token.column
        )
    
    def parse_assignment_or_expression(self) -> ASTNode:
        """
        Parses an assignment or an expression statement.

        This method handles the ambiguity between an assignment and an
        expression statement by looking ahead for an assignment operator.

        Returns:
            ASTNode: The parsed assignment or expression statement node.
        """
        name_token = self.advance()
        name = name_token.value
        
        track = None
        # Check for track qualifier: name.track
        if self.match(TokenType.DOT):
            self.advance()
            track_token = self.expect(TokenType.IDENTIFIER)
            track = track_token.value
        
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
            return Assignment(
                target=name,
                track=track,
                value=value,
                line=name_token.line,
                column=name_token.column
            )
        elif self.match(TokenType.LPAREN) and track is None:
            # It's a function call
            self.advance()
            args = []
            while not self.match(TokenType.RPAREN):
                args.append(self.parse_expression())
                if self.match(TokenType.COMMA):
                    self.advance()
            self.expect(TokenType.RPAREN)
            call = FunctionCall(name=name, args=args, line=name_token.line, column=name_token.column)
            return ExpressionStatement(expression=call, line=name_token.line, column=name_token.column)
        else:
            # It's an expression, put the variable back in context
            var = Variable(name=name, track=track, line=name_token.line, column=name_token.column)
            # Continue parsing as expression
            expr = self.parse_expression_continuation(var)
            return ExpressionStatement(expression=expr, line=name_token.line, column=name_token.column)
    
    def parse_expression(self) -> Expression:
        """
        Parses an expression.

        This method starts the recursive descent parsing of an expression.

        Returns:
            Expression: The parsed expression node.
        """
        return self.parse_or_expression()
    
    def parse_or_expression(self) -> Expression:
        """
        Parses an OR expression.

        Returns:
            Expression: The parsed expression node.
        """
        left = self.parse_and_expression()
        
        while self.match(TokenType.OR):
            op_token = self.advance()
            right = self.parse_and_expression()
            left = BinaryOp(
                operator='or',
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_and_expression(self) -> Expression:
        """
        Parses an AND expression.

        Returns:
            Expression: The parsed expression node.
        """
        left = self.parse_comparison_expression()
        
        while self.match(TokenType.AND):
            op_token = self.advance()
            right = self.parse_comparison_expression()
            left = BinaryOp(
                operator='and',
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_comparison_expression(self) -> Expression:
        """
        Parses a comparison expression.

        Returns:
            Expression: The parsed expression node.
        """
        left = self.parse_additive_expression()
        
        if self.match(TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op_token = self.advance()
            op_map = {
                TokenType.EQ: '==',
                TokenType.NE: '!=',
                TokenType.LT: '<',
                TokenType.LE: '<=',
                TokenType.GT: '>',
                TokenType.GE: '>=',
            }
            right = self.parse_additive_expression()
            left = BinaryOp(
                operator=op_map[op_token.type],
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_additive_expression(self) -> Expression:
        """
        Parses an additive expression.

        Returns:
            Expression: The parsed expression node.
        """
        left = self.parse_multiplicative_expression()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            op = '+' if op_token.type == TokenType.PLUS else '-'
            right = self.parse_multiplicative_expression()
            left = BinaryOp(
                operator=op,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_multiplicative_expression(self) -> Expression:
        """
        Parses a multiplicative expression.

        Returns:
            Expression: The parsed expression node.
        """
        left = self.parse_unary_expression()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.advance()
            op = '*' if op_token.type == TokenType.MULTIPLY else '/'
            right = self.parse_unary_expression()
            left = BinaryOp(
                operator=op,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_unary_expression(self) -> Expression:
        """
        Parses a unary expression.

        Returns:
            Expression: The parsed expression node.
        """
        if self.match(TokenType.NOT, TokenType.MINUS):
            op_token = self.advance()
            op = 'not' if op_token.type == TokenType.NOT else '-'
            operand = self.parse_unary_expression()
            return UnaryOp(
                operator=op,
                operand=operand,
                line=op_token.line,
                column=op_token.column
            )
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self) -> Expression:
        """
        Parses a primary expression.

        Primary expressions are the building blocks of other expressions,
        including literals, variables, and parenthesized expressions.

        Returns:
            Expression: The parsed expression node.

        Raises:
            SyntaxError: If an unexpected token is encountered.
        """
        token = self.current()
        
        # Number
        if self.match(TokenType.NUMBER):
            self.advance()
            return NumberLiteral(value=token.value, line=token.line, column=token.column)
        
        # Identifier (variable or function call)
        if self.match(TokenType.IDENTIFIER):
            self.advance()
            name = token.value
            
            # Check for track qualifier
            track = None
            if self.match(TokenType.DOT):
                self.advance()
                track_token = self.expect(TokenType.IDENTIFIER)
                track = track_token.value
            
            # Check for function call
            if self.match(TokenType.LPAREN):
                self.advance()
                args = []
                while not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    if self.match(TokenType.COMMA):
                        self.advance()
                self.expect(TokenType.RPAREN)
                return FunctionCall(name=name, args=args, line=token.line, column=token.column)
            
            return Variable(name=name, track=track, line=token.line, column=token.column)
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token in expression: {token.type.name}")
    
    def parse_expression_continuation(self, left: Expression) -> Expression:
        """
        Continues parsing an expression with the left side already parsed.

        This method is a placeholder for future extensions to the parser.

        Args:
            left (Expression): The already parsed left side of the expression.

        Returns:
            Expression: The parsed expression node.
        """
        # This handles cases where we've already consumed part of an expression
        # For now, just return left as-is
        return left
