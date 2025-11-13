# Bài tập cây biểu thức

Kho lưu trữ này hiện thực các yêu cầu trong `debai.txt`: dựng cây biểu thức từ công thức infix, thực hiện duyệt pre/in/post-order, chuyển sang prefix/postfix và tính giá trị mà không dùng thư viện cấu trúc dữ liệu sẵn có.

## Cấu trúc thư mục

- `src/expression_tree.py` – hàm tách token, chuyển đổi shunting-yard và các thuật toán duyệt cây.
- `src/evaluator.py` – bộ tính giá trị prefix/postfix, hỗ trợ `+ - * : ^` và kiểm tra chia cho 0.
- `src/main.py` – chương trình CLI tạo cây cho các biểu thức trong đề và in kết quả.
- `tests/test_expression_tree.py` – bộ kiểm thử `unittest` cho toàn bộ biểu thức yêu cầu.

## Hướng dẫn chạy

```bash
python -m venv .venv
source .venv/bin/activate
python -m src.main            # chạy demo tất cả biểu thức
python -m src.main --expr "1 + 2 * 3"   # truyền biểu thức tùy ý
python -m unittest             # chạy toàn bộ test
```

CLI sẽ in từng biểu thức, chuỗi prefix/postfix tương ứng và kết quả tính toán. Nếu gặp chia cho 0, chương trình vẫn hiển thị duyệt cây và chú thích “undefined (division by zero)” để dễ kiểm tra.
