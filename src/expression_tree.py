"""Expression tree creation and traversals for arithmetic formulas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional


OPERATORS = {"+", "-", "*", ":", "^"}
RIGHT_ASSOCIATIVE = {"^"}
PRECEDENCE = {"+": 1, "-": 1, "*": 2, ":": 2, "^": 3}


@dataclass
class Node:
    """Single node inside an expression tree."""

    value: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def _emit_number(buffer: List[str], tokens: List[str]) -> None:
    if buffer:
        tokens.append("".join(buffer))
        buffer.clear()


def tokenize(expression: str) -> List[str]:
    """Convert an infix expression into discrete tokens."""
    tokens: List[str] = []
    number_buffer: List[str] = []
    for char in expression:
        if char.isdigit():
            number_buffer.append(char)
            continue
        if char.isspace():
            _emit_number(number_buffer, tokens)
            continue
        if char in OPERATORS or char in {"(", ")"}:
            _emit_number(number_buffer, tokens)
            tokens.append(char)
            continue
        raise ValueError(f"Unsupported character '{char}' in expression: {expression}")

    _emit_number(number_buffer, tokens)
    return tokens


def _is_operand(token: str) -> bool:
    if not token:
        return False
    if token in OPERATORS or token in {"(", ")"}:
        return False
    return True


def infix_to_postfix(tokens: Iterable[str]) -> List[str]:
    """Convert a tokenized infix expression to postfix via the shunting-yard algorithm."""
    output: List[str] = []
    stack: List[str] = []

    for token in tokens:
        if _is_operand(token):
            output.append(token)
            continue
        if token == "(":
            stack.append(token)
            continue
        if token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses in expression.")
            stack.pop()  # Drop "("
            continue

        # Operator
        while stack and stack[-1] in OPERATORS:
            top = stack[-1]
            top_precedence = PRECEDENCE[top]
            token_precedence = PRECEDENCE[token]
            if (
                top_precedence > token_precedence
                or (
                    top_precedence == token_precedence
                    and token not in RIGHT_ASSOCIATIVE
                )
            ):
                output.append(stack.pop())
            else:
                break
        stack.append(token)

    while stack:
        top = stack.pop()
        if top in {"(", ")"}:
            raise ValueError("Mismatched parentheses in expression.")
        output.append(top)

    return output


def build_tree_from_postfix(tokens: Iterable[str]) -> Node:
    """Build an expression tree from postfix tokens."""
    stack: List[Node] = []
    for token in tokens:
        if _is_operand(token):
            stack.append(Node(token))
            continue
        if token not in OPERATORS:
            raise ValueError(f"Encountered invalid token '{token}'.")
        if len(stack) < 2:
            raise ValueError("Invalid postfix expression.")
        right = stack.pop()
        left = stack.pop()
        stack.append(Node(token, left=left, right=right))

    if len(stack) != 1:
        raise ValueError("Postfix expression did not reduce to a single tree.")
    return stack[0]


def build_expression_tree(expression: str) -> "ExpressionTree":
    """Convenience helper to create a tree directly from an infix expression."""
    return ExpressionTree.from_infix(expression)


def _pre_order(node: Optional[Node], acc: List[str]) -> None:
    if not node:
        return
    acc.append(node.value)
    _pre_order(node.left, acc)
    _pre_order(node.right, acc)


def _in_order(node: Optional[Node], acc: List[str]) -> None:
    if not node:
        return
    _in_order(node.left, acc)
    acc.append(node.value)
    _in_order(node.right, acc)


def _post_order(node: Optional[Node], acc: List[str]) -> None:
    if not node:
        return
    _post_order(node.left, acc)
    _post_order(node.right, acc)
    acc.append(node.value)


class ExpressionTree:
    """High level wrapper around the raw tree that exposes traversals."""

    def __init__(self, root: Node, expression: str) -> None:
        self.root = root
        self.expression = expression

    @classmethod
    def from_infix(cls, expression: str) -> "ExpressionTree":
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        root = build_tree_from_postfix(postfix)
        return cls(root=root, expression=expression)

    def preorder(self) -> List[str]:
        result: List[str] = []
        _pre_order(self.root, result)
        return result

    def inorder(self) -> List[str]:
        result: List[str] = []
        _in_order(self.root, result)
        return result

    def postorder(self) -> List[str]:
        result: List[str] = []
        _post_order(self.root, result)
        return result
