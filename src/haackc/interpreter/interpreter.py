"""
Interpreter implementation for HaackLang.
"""

from typing import Any, Dict, List, Optional
from ..parser.ast_nodes import *
from ..runtime.track import Track, LogicType as RuntimeLogicType
from ..runtime.truthvalue import TruthValue, apply_logic_operator
from ..runtime.context import Context


class Interpreter:
    """Interprets HaackLang AST."""
    
    def __init__(self):
        self.tracks: Dict[str, Track] = {}
        self.contexts: Dict[str, Context] = {}
        self.variables: Dict[str, Any] = {}
        self.truthvalues: Dict[str, TruthValue] = {}
        self.global_beat = 0
        self.current_context: Optional[Context] = None
        self.functions: Dict[str, FunctionDecl] = {}
        
        # Default tracks
        self._create_default_tracks()
    
    def _create_default_tracks(self):
        """Create default tracks (main, slow, syncop)."""
        self.tracks['main'] = Track('main', period=1, phase=0, logic=RuntimeLogicType.CLASSICAL)
        self.tracks['slow'] = Track('slow', period=4, phase=0, logic=RuntimeLogicType.FUZZY)
        self.tracks['syncop'] = Track('syncop', period=7, phase=0, logic=RuntimeLogicType.PARACONSISTENT)
    
    def error(self, message: str, node: Optional[ASTNode] = None):
        """Raise an interpreter error."""
        if node:
            raise RuntimeError(f"Runtime error at {node.line}:{node.column}: {message}")
        raise RuntimeError(f"Runtime error: {message}")
    
    def interpret(self, program: Program):
        """Interpret a program."""
        for decl in program.declarations:
            self.execute_declaration(decl)
    
    def execute_declaration(self, node: ASTNode):
        """Execute a top-level declaration."""
        if isinstance(node, TrackDecl):
            self.execute_track_decl(node)
        elif isinstance(node, ContextDecl):
            self.execute_context_decl(node)
        elif isinstance(node, TruthValueDecl):
            self.execute_truthvalue_decl(node)
        elif isinstance(node, RuleDecl):
            self.execute_rule_decl(node)
        elif isinstance(node, FunctionDecl):
            self.functions[node.name] = node
        elif isinstance(node, Assignment):
            self.execute_assignment(node)
        elif isinstance(node, IfStatement):
            self.execute_if_statement(node)
        elif isinstance(node, GuardStatement):
            self.execute_guard_statement(node)
        elif isinstance(node, ExpressionStatement):
            self.evaluate_expression(node.expression)
        else:
            self.error(f"Unknown declaration type: {type(node).__name__}", node)
    
    def execute_track_decl(self, node: TrackDecl):
        """Execute track declaration."""
        logic_map = {
            LogicType.CLASSICAL: RuntimeLogicType.CLASSICAL,
            LogicType.FUZZY: RuntimeLogicType.FUZZY,
            LogicType.PARACONSISTENT: RuntimeLogicType.PARACONSISTENT,
        }
        
        track = Track(
            name=node.name,
            period=node.period,
            phase=node.phase,
            logic=logic_map[node.logic]
        )
        self.tracks[node.name] = track
    
    def execute_context_decl(self, node: ContextDecl):
        """Execute context declaration."""
        logic_map = {
            LogicType.CLASSICAL: RuntimeLogicType.CLASSICAL,
            LogicType.FUZZY: RuntimeLogicType.FUZZY,
            LogicType.PARACONSISTENT: RuntimeLogicType.PARACONSISTENT,
        }
        
        runtime_logic = logic_map.get(node.logic) if node.logic else None
        context = Context(
            name=node.name,
            logic=runtime_logic,
            track=node.track
        )
        self.contexts[node.name] = context
        
        # Execute context body in the context
        old_context = self.current_context
        self.current_context = context
        
        for stmt in node.body:
            self.execute_declaration(stmt)
        
        self.current_context = old_context
    
    def execute_truthvalue_decl(self, node: TruthValueDecl):
        """Execute truth value declaration."""
        initial_val = 0.0
        if node.initial_value:
            result = self.evaluate_expression(node.initial_value)
            if isinstance(result, (int, float)):
                initial_val = float(result)
            elif isinstance(result, TruthValue):
                # Use the TruthValue as-is
                self.truthvalues[node.name] = result
                return
        
        tv = TruthValue(self.tracks, initial_val)
        self.truthvalues[node.name] = tv
    
    def execute_rule_decl(self, node: RuleDecl):
        """Execute rule declaration."""
        # For now, rules are executed immediately
        # In a full implementation, rules would be stored and evaluated on each beat
        for stmt in node.body:
            if isinstance(stmt, (Assignment, IfStatement, GuardStatement, ExpressionStatement)):
                self.execute_declaration(stmt)
    
    def execute_assignment(self, node: Assignment):
        """Execute assignment."""
        value = self.evaluate_expression(node.value)
        
        # Check if it's a track-qualified assignment
        if node.track:
            # Assigning to a specific track of a truthvalue
            if node.target in self.truthvalues:
                tv = self.truthvalues[node.target]
                if isinstance(value, (int, float)):
                    tv.set(node.track, float(value))
                else:
                    self.error(f"Cannot assign {type(value).__name__} to track", node)
            else:
                self.error(f"Variable {node.target} is not a truth value", node)
        else:
            # Regular assignment
            if isinstance(value, TruthValue):
                self.truthvalues[node.target] = value
            else:
                self.variables[node.target] = value
    
    def execute_if_statement(self, node: IfStatement):
        """Execute if statement."""
        condition = self.evaluate_expression(node.condition)
        
        # Convert condition to boolean
        if isinstance(condition, TruthValue):
            condition_bool = condition.to_classical()
        elif isinstance(condition, (int, float)):
            condition_bool = condition >= 0.5
        else:
            condition_bool = bool(condition)
        
        if condition_bool:
            for stmt in node.then_body:
                self.execute_declaration(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                self.execute_declaration(stmt)
    
    def execute_guard_statement(self, node: GuardStatement):
        """Execute guard statement - only if specified track is active."""
        if node.track not in self.tracks:
            self.error(f"Unknown track: {node.track}", node)
        
        track = self.tracks[node.track]
        
        # Check if track is active on current beat
        if not track.is_active(self.global_beat):
            return  # Skip guard body
        
        # Evaluate condition
        condition = self.evaluate_expression(node.condition)
        
        if isinstance(condition, TruthValue):
            condition_bool = condition.get(node.track) >= 0.5
        elif isinstance(condition, (int, float)):
            condition_bool = condition >= 0.5
        else:
            condition_bool = bool(condition)
        
        if condition_bool:
            for stmt in node.body:
                self.execute_declaration(stmt)
    
    def evaluate_expression(self, node: Expression) -> Any:
        """Evaluate an expression."""
        if isinstance(node, NumberLiteral):
            return node.value
        
        elif isinstance(node, BoolLiteral):
            return 1.0 if node.value else 0.0
        
        elif isinstance(node, Variable):
            return self.evaluate_variable(node)
        
        elif isinstance(node, BinaryOp):
            return self.evaluate_binary_op(node)
        
        elif isinstance(node, UnaryOp):
            return self.evaluate_unary_op(node)
        
        elif isinstance(node, FunctionCall):
            return self.evaluate_function_call(node)
        
        else:
            self.error(f"Unknown expression type: {type(node).__name__}", node)
    
    def evaluate_variable(self, node: Variable) -> Any:
        """Evaluate a variable reference."""
        name = node.name
        
        # Check if it's a track-qualified reference
        if node.track:
            if name in self.truthvalues:
                tv = self.truthvalues[name]
                return tv.get(node.track)
            else:
                self.error(f"Variable {name} is not a truth value", node)
        
        # Regular variable lookup
        if name in self.truthvalues:
            return self.truthvalues[name]
        elif name in self.variables:
            return self.variables[name]
        elif self.current_context and name in self.current_context.variables:
            return self.current_context.variables[name]
        else:
            self.error(f"Undefined variable: {name}", node)
    
    def evaluate_binary_op(self, node: BinaryOp) -> Any:
        """Evaluate binary operation."""
        left = self.evaluate_expression(node.left)
        right = self.evaluate_expression(node.right)
        
        # Handle logical operators with polylogical semantics
        if node.operator in ['and', 'or']:
            return self.evaluate_logical_op(node.operator, left, right)
        
        # Arithmetic and comparison operators
        # Convert TruthValues to float
        if isinstance(left, TruthValue):
            left = float(left)
        if isinstance(right, TruthValue):
            right = float(right)
        
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                self.error("Division by zero", node)
            return left / right
        elif node.operator == '==':
            return 1.0 if abs(left - right) < 1e-9 else 0.0
        elif node.operator == '!=':
            return 1.0 if abs(left - right) >= 1e-9 else 0.0
        elif node.operator == '<':
            return 1.0 if left < right else 0.0
        elif node.operator == '<=':
            return 1.0 if left <= right else 0.0
        elif node.operator == '>':
            return 1.0 if left > right else 0.0
        elif node.operator == '>=':
            return 1.0 if left >= right else 0.0
        else:
            self.error(f"Unknown operator: {node.operator}", node)
    
    def evaluate_logical_op(self, op: str, left: Any, right: Any) -> Any:
        """Evaluate logical operation with polylogical semantics."""
        # If both operands are TruthValues, apply track-wise operations
        if isinstance(left, TruthValue) and isinstance(right, TruthValue):
            result = TruthValue(self.tracks)
            for track_name, track in self.tracks.items():
                left_val = left.get(track_name)
                right_val = right.get(track_name)
                result_val = apply_logic_operator(op, track.logic, left_val, right_val)
                result.set(track_name, result_val)
            return result
        
        # If one is TruthValue, convert the other to TruthValue
        if isinstance(left, TruthValue) or isinstance(right, TruthValue):
            if not isinstance(left, TruthValue):
                left = self._to_truthvalue(left)
            if not isinstance(right, TruthValue):
                right = self._to_truthvalue(right)
            return self.evaluate_logical_op(op, left, right)
        
        # Both are scalars - use classical logic
        left_val = float(left) if isinstance(left, (int, float)) else 0.0
        right_val = float(right) if isinstance(right, (int, float)) else 0.0
        result = apply_logic_operator(op, RuntimeLogicType.CLASSICAL, left_val, right_val)
        return result
    
    def evaluate_unary_op(self, node: UnaryOp) -> Any:
        """Evaluate unary operation."""
        operand = self.evaluate_expression(node.operand)
        
        if node.operator == 'not':
            if isinstance(operand, TruthValue):
                result = TruthValue(self.tracks)
                for track_name, track in self.tracks.items():
                    val = operand.get(track_name)
                    result_val = apply_logic_operator('not', track.logic, val)
                    result.set(track_name, result_val)
                return result
            else:
                val = float(operand) if isinstance(operand, (int, float)) else 0.0
                return apply_logic_operator('not', RuntimeLogicType.CLASSICAL, val)
        
        elif node.operator == '-':
            if isinstance(operand, TruthValue):
                return -float(operand)
            return -operand
        
        else:
            self.error(f"Unknown unary operator: {node.operator}", node)
    
    def evaluate_function_call(self, node: FunctionCall) -> Any:
        """Evaluate function call."""
        # Built-in functions
        if node.name == 'print':
            args = [self.evaluate_expression(arg) for arg in node.args]
            for arg in args:
                if isinstance(arg, TruthValue):
                    print(arg)
                else:
                    print(arg)
            return 0.0
        
        # User-defined functions
        if node.name in self.functions:
            func = self.functions[node.name]
            args = [self.evaluate_expression(arg) for arg in node.args]
            
            # Create new scope
            old_vars = self.variables.copy()
            
            # Bind parameters
            if len(args) != len(func.params):
                self.error(f"Function {node.name} expects {len(func.params)} arguments, got {len(args)}", node)
            
            for param, arg in zip(func.params, args):
                self.variables[param] = arg
            
            # Execute function body
            result = None
            try:
                for stmt in func.body:
                    if isinstance(stmt, ReturnStatement):
                        if stmt.value:
                            result = self.evaluate_expression(stmt.value)
                        break
                    else:
                        self.execute_declaration(stmt)
            finally:
                # Restore scope
                self.variables = old_vars
            
            return result if result is not None else 0.0
        
        self.error(f"Unknown function: {node.name}", node)
    
    def _to_truthvalue(self, value: Any) -> TruthValue:
        """Convert a scalar value to a TruthValue."""
        if isinstance(value, TruthValue):
            return value
        val = float(value) if isinstance(value, (int, float)) else 0.0
        return TruthValue(self.tracks, val)
    
    def advance_beat(self):
        """Advance the global beat counter."""
        self.global_beat += 1
        for track in self.tracks.values():
            track.advance()
