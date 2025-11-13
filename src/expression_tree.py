"""Xây dựng cây biểu thức và các phép duyệt cho các công thức số học."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional


OPERATORS = {"+", "-", "*", ":", "^"}
RIGHT_ASSOCIATIVE = {"^"}
PRECEDENCE = {"+": 1, "-": 1, "*": 2, ":": 2, "^": 3}


@dataclass
class Node:
    """Đại diện cho một nút trong cây biểu thức (toán hạng hoặc toán tử)."""

    value: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def is_leaf(self) -> bool:
        """Kiểm tra nút có phải lá (không có con trái/phải) hay không."""
        return self.left is None and self.right is None


def _emit_number(buffer: List[str], tokens: List[str]) -> None:
    """Đẩy chuỗi chữ số đang gom vào danh sách token rồi xóa bộ đệm."""
    if buffer:
        tokens.append("".join(buffer))
        buffer.clear()


def tokenize(expression: str) -> List[str]:
    """Tách biểu thức infix thành danh sách token (số, toán tử, ngoặc)."""
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
    """Trả về True nếu token là toán hạng (số) hợp lệ."""
    if not token:
        return False
    if token in OPERATORS or token in {"(", ")"}:
        return False
    return True


def infix_to_postfix(tokens: Iterable[str]) -> List[str]:
    """Chuyển biểu thức infix (đã tách token) sang postfix bằng giải thuật shunting-yard."""
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
    """Dựng cây biểu thức từ chuỗi token postfix."""
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
    """Hàm tiện ích: nhận biểu thức infix và trả về `ExpressionTree` tương ứng."""
    return ExpressionTree.from_infix(expression)


def _pre_order(node: Optional[Node], acc: List[str]) -> None:
    """Duyệt tiền tự (NLR) và ghi kết quả vào `acc`."""
    if not node:
        return
    acc.append(node.value)
    _pre_order(node.left, acc)
    _pre_order(node.right, acc)


def _in_order(node: Optional[Node], acc: List[str]) -> None:
    """Duyệt trung tự (LNR) và ghi kết quả vào `acc`."""
    if not node:
        return
    _in_order(node.left, acc)
    acc.append(node.value)
    _in_order(node.right, acc)


def _post_order(node: Optional[Node], acc: List[str]) -> None:
    """Duyệt hậu tự (LRN) và ghi kết quả vào `acc`."""
    if not node:
        return
    _post_order(node.left, acc)
    _post_order(node.right, acc)
    acc.append(node.value)


def _render_ascii(node: Optional[Node], prefix: str, is_tail: bool, acc: List[str]) -> None:
    """Đệ quy dựng từng dòng ASCII thể hiện quan hệ cha-con."""
    if not node:
        return
    connector = "└── " if is_tail else "├── "
    acc.append(f"{prefix}{connector}{node.value}")
    children = []
    if node.left:
        children.append(node.left)
    if node.right:
        children.append(node.right)
    for index, child in enumerate(children):
        extension = "    " if is_tail else "│   "
        _render_ascii(child, prefix + extension, index == len(children) - 1, acc)


class ExpressionTree:
    """Bao bọc cây biểu thức và cung cấp các thao tác xây dựng + duyệt."""

    def __init__(self, root: Node, expression: str) -> None:
        self.root = root
        self.expression = expression

    @classmethod
    def from_infix(cls, expression: str) -> "ExpressionTree":
        """Khởi tạo cây trực tiếp từ biểu thức infix."""
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        root = build_tree_from_postfix(postfix)
        return cls(root=root, expression=expression)

    def preorder(self) -> List[str]:
        """Trả về danh sách token theo thứ tự duyệt tiền tự."""
        result: List[str] = []
        _pre_order(self.root, result)
        return result

    def inorder(self) -> List[str]:
        """Trả về danh sách token theo thứ tự duyệt trung tự."""
        result: List[str] = []
        _in_order(self.root, result)
        return result

    def postorder(self) -> List[str]:
        """Trả về danh sách token theo thứ tự duyệt hậu tự."""
        result: List[str] = []
        _post_order(self.root, result)
        return result

    def render_ascii(self) -> str:
        """Trả về chuỗi ASCII mô tả cây theo dạng gạch kết nối."""
        lines: List[str] = []
        if self.root:
            _render_ascii(self.root, "", True, lines)
        return "\n".join(lines)
