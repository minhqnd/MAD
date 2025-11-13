"""Bộ kiểm thử đảm bảo cây biểu thức hoạt động như mô tả trong đề bài."""

import math
import unittest

from src.evaluator import evaluate_postfix, evaluate_prefix
from src.expression_tree import build_expression_tree


EXPRESSIONS = [
    ("(3^2 + 5) - 4 : 2", 12),
    ("((3^2 + 5) - 4) : 2", 5),
    ("(1 + 2) * (3 + 4) + (5 * 6)", 51),
    ("1 + (2 * 3) + (4 + 5) * 6", 61),
]


class ExpressionTreeTests(unittest.TestCase):
    """Nhóm test xác minh kết quả duyệt cây và tính toán."""

    def test_traversal_evaluations_match(self) -> None:
        """Mỗi biểu thức mẫu phải cho cùng giá trị ở cả prefix và postfix."""
        for expression, expected in EXPRESSIONS:
            tree = build_expression_tree(expression)
            prefix_tokens = tree.preorder()
            postfix_tokens = tree.postorder()
            prefix_value = evaluate_prefix(prefix_tokens)
            postfix_value = evaluate_postfix(postfix_tokens)
            self.assertTrue(math.isclose(prefix_value, expected))
            self.assertTrue(math.isclose(postfix_value, expected))

    def test_zero_division_expression(self) -> None:
        """Biểu thức chia cho 0 cần ném `ZeroDivisionError` để cảnh báo."""
        expression = "(1 + 2 * 3) : (4 - 5 - 6 +7)"
        tree = build_expression_tree(expression)
        with self.assertRaises(ZeroDivisionError):
            evaluate_prefix(tree.preorder())
        with self.assertRaises(ZeroDivisionError):
            evaluate_postfix(tree.postorder())


if __name__ == "__main__":
    unittest.main()
