# phân tích
# 1. endpoint hiện tại có path parameter
# 2. path parameter: /orders/status/{status}
# 3. status = "pending"
# 4. vì hàm không sử dụng giá trị status để lọc dữ liệu mà trả về toàn bộ danh sách orders
# 5. return orders - dòng code đang khiến API bỏ qua giá trị status

from fastapi import FastAPI

app = FastAPI()

orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]

@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    valid_status = ["pending", "paid", "cancelled"]

    if status not in valid_status:
        return {
            "message": "TRạng thái đơn hàng không đúng"
        }

    result = []

    for order in orders:
        if order["status"] == status:
            result.append(order)

    return result