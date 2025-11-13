"""
Bài tập: Cây Biểu thức và Duyệt Cây
Tree Traversal: Pre-order, In-order, Post-order
Expression Evaluation: Prefix, Infix, Postfix
"""

class TreeNode:
    """Lớp Node cho cây biểu thức"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class ExpressionTree:
    """Lớp xử lý cây biểu thức"""
    
    def __init__(self):
        self.root = None
        self.precedence = {'^': 3, '*': 2, ':': 2, '+': 1, '-': 1}
    
    def is_operator(self, char):
        """Kiểm tra ký tự có phải toán tử không"""
        return char in ['+', '-', '*', ':', '^']
    
    def tokenize(self, expression):
        """Tách biểu thức thành các token"""
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i] == ' ':
                i += 1
                continue
            if expression[i].isdigit():
                num = ''
                while i < len(expression) and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                tokens.append(num)
            else:
                tokens.append(expression[i])
                i += 1
        return tokens
    
    def build_tree(self, infix_expr):
        """Xây dựng cây biểu thức từ biểu thức infix"""
        tokens = self.tokenize(infix_expr)
        operators = []
        operands = []
        
        for token in tokens:
            if token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._create_node(operators, operands)
                operators.pop()  # Xóa '('
            elif self.is_operator(token):
                # Xử lý ưu tiên toán tử
                while (operators and 
                       operators[-1] != '(' and
                       operators[-1] in self.precedence and
                       self.precedence[operators[-1]] >= self.precedence[token] and
                       not (token == '^' and operators[-1] == '^')):
                    self._create_node(operators, operands)
                operators.append(token)
            else:
                # Toán hạng (số)
                node = TreeNode(token)
                operands.append(node)
        
        while operators:
            self._create_node(operators, operands)
        
        self.root = operands[0] if operands else None
        return self.root
    
    def _create_node(self, operators, operands):
        """Tạo node từ toán tử và hai toán hạng"""
        operator = operators.pop()
        node = TreeNode(operator)
        node.right = operands.pop()
        node.left = operands.pop()
        operands.append(node)
    
    # === THUẬT TOÁN DUYỆT CÂY ===
    
    def pre_order(self, node=None, result=None):
        """
        Duyệt cây theo Pre-order (Tiền tự - NLR)
        Node -> Left -> Right
        Iterative implementation to avoid recursion depth limit
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        stack = []
        current = node
        while current or stack:
            while current:
                result.append(current.value)
                stack.append(current)
                current = current.left
            current = stack.pop()
            current = current.right
        return result
    
    def in_order(self, node=None, result=None):
        """
        Duyệt cây theo In-order (Trung tự - LNR)
        Left -> Node -> Right
        Iterative implementation to avoid recursion depth limit
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        stack = []
        current = node
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.value)
            current = current.right
        return result
    
    def post_order(self, node=None, result=None):
        """
        Duyệt cây theo Post-order (Hậu tự - LRN)
        Left -> Right -> Node
        Iterative implementation to avoid recursion depth limit
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        stack = []
        current = node
        last_visited = None
        while current or stack:
            if current:
                stack.append(current)
                current = current.left
            else:
                peek = stack[-1]
                if peek.right and last_visited != peek.right:
                    current = peek.right
                else:
                    result.append(peek.value)
                    last_visited = stack.pop()
        return result
    
    def visualize(self, node=None, prefix="", is_tail=True):
        """Hiển thị cây dạng text"""
        if node is None:
            node = self.root
        
        if node is not None:
            print(prefix + ("└── " if is_tail else "├── ") + str(node.value))
            
            children = []
            if node.left is not None:
                children.append(node.left)
            if node.right is not None:
                children.append(node.right)
            
            for i, child in enumerate(children):
                extension = "    " if is_tail else "│   "
                self.visualize(child, prefix + extension, i == len(children) - 1)


class ExpressionEvaluator:
    """Lớp tính toán biểu thức Prefix và Postfix"""
    
    @staticmethod
    def is_operator(token):
        return token in ['+', '-', '*', ':', '^']
    
    @staticmethod
    def calculate(op1, op2, operator):
        """Thực hiện phép tính"""
        op1, op2 = float(op1), float(op2)
        if operator == '+':
            return op1 + op2
        elif operator == '-':
            return op1 - op2
        elif operator == '*':
            return op1 * op2
        elif operator == ':':
            if op2 == 0:
                raise ValueError("Division by zero")
            return op1 / op2
        elif operator == '^':
            return op1 ** op2
    
    @classmethod
    def evaluate_prefix(cls, tokens):
        """
        Tính toán biểu thức Prefix (tiền tố)
        Duyệt từ phải sang trái
        """
        stack = []
        
        # Duyệt từ phải sang trái
        for i in range(len(tokens) - 1, -1, -1):
            token = tokens[i]
            
            if not cls.is_operator(token):
                stack.append(token)
            else:
                # Lấy hai toán hạng
                operand1 = stack.pop()
                operand2 = stack.pop()
                result = cls.calculate(operand1, operand2, token)
                stack.append(result)
        
        return stack[0]
    
    @classmethod
    def evaluate_postfix(cls, tokens):
        """
        Tính toán biểu thức Postfix (hậu tố)
        Duyệt từ trái sang phải
        """
        stack = []
        
        for token in tokens:
            if not cls.is_operator(token):
                stack.append(token)
            else:
                # Lấy hai toán hạng (chú ý thứ tự)
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = cls.calculate(operand1, operand2, token)
                stack.append(result)
        
        return stack[0]


def print_separator(char="=", length=70):
    """In dòng phân cách"""
    print(char * length)


def process_expression(expr_num, expression):
    """Xử lý một biểu thức"""
    print(f"\n{'='*70}")
    print(f"CÔNG THỨC {expr_num}: {expression}")
    print(f"{'='*70}\n")
    
    # Xây dựng cây
    tree = ExpressionTree()
    tree.build_tree(expression)
    
    print("1. CẤU TRÚC CÂY:")
    print("-" * 70)
    tree.visualize()
    
    # Duyệt cây
    print(f"\n2. DUYỆT CÂY:")
    print("-" * 70)
    
    prefix = tree.pre_order()
    infix = tree.in_order()
    postfix = tree.post_order()
    
    print(f"Pre-order (Prefix)  : {' '.join(prefix)}")
    print(f"In-order (Infix)    : {' '.join(infix)}")
    print(f"Post-order (Postfix): {' '.join(postfix)}")
    
    # Tính toán
    print(f"\n3. TÍNH TOÁN:")
    print("-" * 70)
    
    evaluator = ExpressionEvaluator()
    
    try:
        prefix_result = evaluator.evaluate_prefix(prefix)
        print(f"Kết quả từ Prefix  : {prefix_result}")
    except ValueError as e:
        prefix_result = str(e)
        print(f"Lỗi từ Prefix     : {e}")
    
    try:
        postfix_result = evaluator.evaluate_postfix(postfix)
        print(f"Kết quả từ Postfix : {postfix_result}")
    except ValueError as e:
        postfix_result = str(e)
        print(f"Lỗi từ Postfix    : {e}")
    
    # Kiểm tra
    if isinstance(prefix_result, (int, float)) and isinstance(postfix_result, (int, float)):
        if abs(prefix_result - postfix_result) < 0.0001:
            print(f"✓ Kết quả khớp: {prefix_result}")
        else:
            print(f"✗ Lỗi: Kết quả không khớp!")
    elif prefix_result == postfix_result:
        print(f"✓ Cùng lỗi: {prefix_result}")
    else:
        print(f"✗ Lỗi khác nhau!")


def main():
    """Hàm chính"""
    print("\n" + "="*70)
    print(" "*15 + "BÀI TẬP: CÂY BIỂU THỨC VÀ DUYỆT CÂY")
    print(" "*10 + "Tree Traversal & Expression Evaluation")
    print("="*70)
    
    # Danh sách các công thức
    expressions = [
        "(3^2 + 5) - 4 : 2",
        "((3^2 + 5) - 4) : 2",
        "(1 + 2) * (3 + 4) + (5 * 6)",
        "1 + (2 * 3) + (4 + 5) * 6",
        "(1 + 2 * 3) : (4 - 5 - 6 + 7)"
    ]
    
    # Xử lý từng công thức
    for i, expr in enumerate(expressions, 1):
        process_expression(i, expr)
    
    print("\n" + "="*70)
    print(" "*20 + "HOÀN THÀNH!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()