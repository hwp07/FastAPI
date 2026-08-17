import re
from typing import Optional


def clean_and_validate_products(products: list[dict]) -> list[dict]:
    """Chuẩn hóa product_code và loại bỏ mã không hợp lệ."""
    result = []

    for product in products:
        code = str(product.get("product_code", "")).strip().upper()

        if re.fullmatch(r"P\d{3}", code):
            item = product.copy()
            item["product_code"] = code
            result.append(item)

    return result


def binary_search_product(
    products: list[dict],
    target_code: str
) -> Optional[dict]:
    """Binary Search trên danh sách đã tăng dần theo product_code."""
    target = target_code.strip().upper()
    left, right = 0, len(products) - 1

    while left <= right:
        mid = (left + right) // 2
        code = products[mid]["product_code"].strip().upper()

        if code == target:
            return products[mid]
        if code < target:
            left = mid + 1
        else:
            right = mid - 1

    return None


def sort_products_by_price_desc(products: list[dict]) -> list[dict]:
    """Merge Sort giảm dần theo price, không dùng sort/sorted."""
    if len(products) <= 1:
        return products.copy()

    mid = len(products) // 2
    left = sort_products_by_price_desc(products[:mid])
    right = sort_products_by_price_desc(products[mid:])

    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i]["price"] >= right[j]["price"]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def analyze_order_stats(orders: list[dict]) -> dict:
    """Tính doanh thu COMPLETED và đơn hàng có amount lớn nhất."""
    total_revenue = 0
    max_order = None

    for order in orders:
        if order.get("status") == "COMPLETED":
            total_revenue += float(order.get("amount", 0))

        if max_order is None or float(order.get("amount", 0)) > float(
            max_order.get("amount", 0)
        ):
            max_order = order

    return {
        "total_revenue": total_revenue,
        "max_order": max_order,
    }


if __name__ == "__main__":
    raw_products = [
        {"product_code": "P301", "name": "Laptop Dell XPS", "price": 25000000, "stock": 10, "status": "available"},
        {"product_code": " p101 ", "name": "Chuột Logitech", "price": 500000, "stock": 50, "status": "available"},
        {"product_code": "P202", "name": "Màn hình LG 27", "price": 6000000, "stock": 0, "status": "out_of_stock"},
        {"product_code": "P102", "name": "Bàn phím Cơ", "price": 1200000, "stock": 15, "status": "available"},
        {"product_code": "P302", "name": "Tai nghe Sony", "price": 3500000, "stock": 8, "status": "available"},
    ]

    raw_orders = [
        {"order_code": "ORD001", "customer": "Nguyễn Văn A", "amount": 15000000, "status": "COMPLETED"},
        {"order_code": "ORD002", "customer": "Trần Thị B", "amount": 2500000, "status": "COMPLETED"},
        {"order_code": "ORD003", "customer": "Lê Văn C", "amount": 8000000, "status": "PENDING"},
        {"order_code": "ORD004", "customer": "Phạm Văn D", "amount": 45000000, "status": "COMPLETED"},
    ]

    cleaned = clean_and_validate_products(raw_products)
    print("Cleaned:", cleaned)

    by_code = clean_and_validate_products(raw_products)
    by_code = sort_products_by_price_desc(by_code)
    # Binary search requires ascending order, so prepare a small ascending list manually.
    by_code = [p for p in clean_and_validate_products(raw_products)]
    by_code = sort_products_by_price_desc(by_code)  # demo of the required sort
    print("Sorted by price desc:", by_code)
    print("Stats:", analyze_order_stats(raw_orders))
