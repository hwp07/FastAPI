# Dataset inventory & students:
inventory = [
    {"id": "SP1", "ten": "Tai nghe Sony", "gia": 1200000, "danh_muc": "Phụ kiện"},
    {"id": "SP2", "ten": "Chuột không dây", "gia": 450000, "danh_muc": "Phụ kiện"},
    {"id": "SP3", "ten": "Bàn phím Cơ", "gia": 950000, "danh_muc": "Phụ kiện"},
    {"id": "SP4", "ten": "Màn hình Dell 27 inch", "gia": 4500000, "danh_muc": "Thiết bị"},
    {"id": "SP5", "ten": "Sạc dự phòng 20000mAh", "gia": 350000, "danh_muc": "Phụ kiện"}
]


def linear_search_filter(cart, target_category, max_price):
    result = []
    for item in cart:
        if item["gia"] <= max_price and item["danh_muc"] == target_category:
            result.append(item)

    return result


target_category = "Phụ kiện"
max_price = 1_000_000

result = linear_search_filter(inventory, target_category, max_price)

# In kết quả
print("KẾT QUẢ LỌC SẢN PHẨM (LINEAR SEARCH MULTI-CRITERIA)")
print(f"Danh mục tìm kiếm: {target_category} | Giá tối đa: {max_price:,} VNĐ")
print(f"Tìm thấy {len(result)} sản phẩm phù hợp:")

for item in result:
    print(f"  -> [{item['id']}] {item['ten']} | Giá: {item['gia']:,} VNĐ")