"""Evaluate prefix and postfix arithmetic expressions."""

from __future__ import annotations

from typing import Iterable, List

from .expression_tree import OPERATORS


def _apply_operator(op: str, left: float, right: float) -> float:
    if op == "+":
        return left + right
    if op == "-":
        return left - right
    if op == "*":
        return left * right
    if op == ":":
        if right == 0:
            raise ZeroDivisionError("Division by zero encountered.")
        return left / right
    if op == "^":
        return left**right
    raise ValueError(f"Unsupported operator '{op}'.")


def _coerce(token: str) -> float:
    try:
        return float(token)
    except ValueError as exc:
        raise ValueError(f"Token '{token}' is not a valid number.") from exc


def evaluate_prefix(tokens: Iterable[str]) -> float:
    """Evaluate a prefix expression represented as tokens."""
    stack: List[float] = []
    for token in reversed(list(tokens)):
        if token in OPERATORS:
            if len(stack) < 2:
                raise ValueError("Invalid prefix expression.")
            left = stack.pop()
            right = stack.pop()
            stack.append(_apply_operator(token, left, right))
        else:
            stack.append(_coerce(token))
    if len(stack) != 1:
        raise ValueError("Prefix expression reduced to multiple values.")
    return stack[0]


def evaluate_postfix(tokens: Iterable[str]) -> float:
    """Evaluate a postfix expression represented as tokens."""
    stack: List[float] = []
    for token in tokens:
        if token in OPERATORS:
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression.")
            right = stack.pop()
            left = stack.pop()
            stack.append(_apply_operator(token, left, right))
        else:
            stack.append(_coerce(token))
    if len(stack) != 1:
        raise ValueError("Postfix expression reduced to multiple values.")
    return stack[0]


def evaluate_prefix_expression(expression: str) -> float:
    """Evaluate a whitespace-delimited prefix string."""
    tokens = [token for token in expression.split() if token]
    return evaluate_prefix(tokens)


def evaluate_postfix_expression(expression: str) -> float:
    """Evaluate a whitespace-delimited postfix string."""
    tokens = [token for token in expression.split() if token]
    return evaluate_postfix(tokens)
