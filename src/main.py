"""CLI quản lý cây biểu thức: dựng cây, duyệt và tính toán."""

from __future__ import annotations

import argparse
from typing import Iterable, List

from .evaluator import evaluate_postfix, evaluate_prefix
from .expression_tree import ExpressionTree, build_expression_tree

DEFAULT_EXPRESSIONS = [
    "(3^2 + 5) - 4 : 2",
    "((3^2 + 5) - 4) : 2",
    "(1 + 2) * (3 + 4) + (5 * 6)",
    "1 + (2 * 3) + (4 + 5) * 6",
    "(1 + 2 * 3) : (4 - 5 - 6 +7)",
]


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Khởi tạo bộ phân tích tham số cho CLI."""
    parser = argparse.ArgumentParser(
        description="Build expression trees and display traversals.",
    )
    parser.add_argument(
        "--expr",
        action="append",
        help="Custom infix expression to evaluate. Can be supplied multiple times.",
    )
    return parser.parse_args(argv)


def render_results(expression: str) -> str:
    """Dựng cây cho một biểu thức cụ thể và trả về nội dung cần in."""
    tree = build_expression_tree(expression)
    prefix_tokens = tree.preorder()
    postfix_tokens = tree.postorder()
    prefix = " ".join(prefix_tokens)
    postfix = " ".join(postfix_tokens)
    art = tree.render_ascii()

    def safe_eval(func, tokens: List[str]) -> str:
        try:
            return f"{func(tokens):.4g}"
        except ZeroDivisionError:
            return "undefined (division by zero)"

    prefix_value = safe_eval(evaluate_prefix, prefix_tokens)
    postfix_value = safe_eval(evaluate_postfix, postfix_tokens)

    lines = [
        f"Expression : {expression}",
        f"Prefix     : {prefix}",
        f"Postfix    : {postfix}",
        f"Prefix eval: {prefix_value}",
        f"Postfix eval: {postfix_value}",
        "Tree:",
        art,
    ]
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> None:
    """Điểm vào chính: đọc danh sách biểu thức và in kết quả."""
    args = parse_args(argv)
    expressions = args.expr if args.expr else DEFAULT_EXPRESSIONS
    for index, expr in enumerate(expressions, start=1):
        if index > 1:
            print("-" * 40)
        print(render_results(expr))


if __name__ == "__main__":
    main()
