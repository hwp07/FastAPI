orders = [
    {"id": "DH01", "name": "iPhone 15 Pro Max", "price": 32000000},
    {"id": "DH02", "name": "Tai nghe AirPods Pro", "price": 5500000},
    {"id": "DH03", "name": "MacBook Pro M3 Max", "price": 65000000},
    {"id": "DH04", "name": "Chuot khong day", "price": 450000},
    {"id": "DH05", "name": "Samsung Galaxy S24", "price": 22000000}
]

# Tính tổng doanh thu toàn bộ đơn hàng trong ngày.
total = sum(order["price"] for order in orders)


# Đếm số lượng đơn hàng có giá trị VIP (>= 15,000,000 VND).
count = 0
for price in orders:
    if price["price"] >= 15_000_000:
        count += 1

# Tìm đơn hàng có giá trị cao nhất và thấp nhất chỉ bằng 1 vòng lặp duy nhất (Single Pass).
max_price = min_price = orders[0]

for price in orders:
    if price["price"] > max_price["price"]:
        max_price = price
    elif price["price"] < min_price["price"]:
        min_price = price

# Sử dụng Tư duy Cắm Cờ (Flag is_suspicious = False): Nếu có đơn hàng > 50,000,000 VND, bật cờ True.
is_suspicious = False
for price in orders:
    if price["price"] >= 65_000_000:
        is_suspicious = True

        print(
                f"CANH BAO RUI RO: Phat hien don {price['id']} "
                f"co gia tri {price['price']:,} VND > 50tr!"
            )


print(f"Tong doanh thu: {total:,} VND")
print(f"So don hang VIP (>= 15tr): {count} don")

print(
    f"Don hang gia tri CAO NHAT: "
    f"{max_price['id']} - {max_price['name']} "
    f"({max_price['price']:,} VND)"
)

print(
    f"Don hang gia tri THAP NHAT: "
    f"{min_price['id']} - {min_price['name']} "
    f"({min_price['price']:,} VND)"
)

print(f"KET LUAN CAM CO: Co is_suspicious = {is_suspicious}")