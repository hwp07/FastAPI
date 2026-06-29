# phân tích
# 1. input: danh sách books
# 2. output: danh sách có sô lượng <= 5 hoặc thông báo k có sách nào xắp hết
# 3. điều kiện: số lượng sách <= 5

# giải pháp
# 1. dùng vòng lặp for, duyệt qua từng quyển sách, kiểm tra validate và trả về kết quả
# 2. dùng list comprehension để lọc các sách thỏa mãn điều kiện

# so sánh giải pháp
# vòng lặp for:
#     dễ hiểu
#     dễ xử lý bẫy dữ liệu
#     dễ bảo trì


# list comprehension:
#     ngắn gọn
#     khó đọc hơn khi có nhiều điều kiện

from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]

@app.get("/books/low-stock")
def get_low_stock_books():
    low_stock_books = []

    for book in books:
        if "quantity" not in book:
            continue

        if book["quantity"] < 0:
            continue

        if book["quantity"] <= 5:
            low_stock_books.append(book)

    if len(low_stock_books) == 0:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock_books
    }