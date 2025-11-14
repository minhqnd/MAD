# Cây Biểu Thức (Expression Tree)

Dự án này cung cấp một bộ công cụ dòng lệnh (CLI) để xây dựng, duyệt, và tính toán các cây biểu thức từ các công thức toán học dạng infix.

Đây là bài làm cho yêu cầu được mô tả trong file `debai.txt`, bao gồm việc hiện thực cây biểu thức, các thuật toán duyệt cây (pre-order, in-order, post-order), chuyển đổi sang ký pháp prefix/postfix, và tính toán giá trị mà không sử dụng các thư viện cấu trúc dữ liệu có sẵn.

## Tính năng

- **Xây dựng cây từ Infix**: Chuyển đổi một chuỗi biểu thức infix thành một cây biểu thức.
- **Duyệt cây**: Hỗ trợ các phép duyệt **Pre-order** (tiền tự), **In-order** (trung tự), và **Post-order** (hậu tự).
- **Chuyển đổi ký pháp**: Tạo ra các biểu thức **Prefix** (tiền tố) và **Postfix** (hậu tố) tương ứng.
- **Tính toán giá trị**: Tính toán kết quả của biểu thức từ dạng prefix và postfix.
- **Trực quan hóa**: Hiển thị cấu trúc cây dưới dạng văn bản (ASCII art) để dễ dàng gỡ lỗi và kiểm tra.
- **Giao diện dòng lệnh (CLI)**: Cho phép người dùng chạy các biểu thức mặc định hoặc cung cấp biểu thức tùy chỉnh.

## Cấu trúc dự án

- `src/main.py`: Điểm vào chính của chương trình CLI. Chịu trách nhiệm phân tích tham số dòng lệnh và điều phối việc xử lý các biểu thức.
- `src/expression_tree.py`: Chứa logic cốt lõi cho việc xây dựng cây.
    - Tách biểu thức (tokenize).
    - Chuyển đổi infix sang postfix bằng thuật toán **Shunting-yard**.
    - Xây dựng cây từ biểu thức postfix.
    - Hiện thực các thuật toán duyệt cây.
- `src/evaluator.py`: Chứa logic để tính toán giá trị của các biểu thức dạng prefix và postfix. Hỗ trợ các toán tử `+`, `-`, `*`, `:`, `^` và xử lý lỗi chia cho không.
- `tests/test_expression_tree.py`: Bộ kiểm thử `unittest` để xác minh tính đúng đắn của toàn bộ chu trình xử lý.

## Hướng dẫn sử dụng

1.  **Cài đặt môi trường ảo (khuyến khích):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Chạy chương trình:**
    - Để chạy với các biểu thức mặc định trong đề bài:
      ```bash
      python -m src.main
      ```
    - Để chạy với một hoặc nhiều biểu thức tùy chỉnh:
      ```bash
      python -m src.main --expr "(10 + 5) * 2" --expr "3^2 + 4"
      ```

3.  **Chạy kiểm thử:**
    ```bash
    python -m unittest
    ```

## Ví dụ kết quả

Khi chạy với biểu thức `(3^2 + 5) - 4 : 2`, chương trình sẽ cho ra kết quả tương tự như sau:

```
Biểu thức: (3^2 + 5) - 4 : 2

1. Duyệt cây
   • Tiền tố (Prefix) : - + ^ 3 2 5 : 4 2
   • Hậu tố (Postfix) : 3 2 ^ 5 + 4 2 : -

2. Kết quả tính toán
   • Giá trị Prefix   : 12
   • Giá trị Postfix  : 12

3. Cây biểu thức
└── -
    ├── +
    │   ├── ^
    │   │   ├── 3
    │   │   └── 2
    │   └── 5
    └── :
        ├── 4
        └── 2
```
