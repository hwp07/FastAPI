orders = [
    {"id": "DH01", "total": "12500000", "discount_code": "VIP10", "is_vip": True},
    {"id": "DH02", "total": "450000", "discount_code": "INVALID", "is_vip": False},
    {"id": "DH03", "total": "ABC_ERROR", "discount_code": "", "is_vip": False},
    {"id": "DH04", "total": "8500000", "discount_code": "VIP20", "is_vip": True}
]


def safe_process_invoice(order_id, raw_total, discount_code, is_vip):
    try:
        total = float(raw_total)

        discount = 0

        if is_vip:
            if discount_code == "VIP10":
                discount = total * 0.10
            elif discount_code == "VIP20":
                discount = total * 0.20

        after_discount = total - discount
        vat = after_discount * 0.10
        final_total = after_discount + vat

        if is_vip and final_total >= 10000000:
            category = "HÓA ĐƠN LỚN (VIP)"
        else:
            category = "HÓA ĐƠN THƯỜNG"

        if discount > 0:
            print(f"[{order_id}] Tiền hàng: {total:,.0f} | CK ({discount_code}): {discount:,.0f} | VAT 10%: {vat:,.0f} -> Tổng: {final_total:,.0f} VNĐ [{category}]")
        else:
            print(f"[{order_id}] Tiền hàng: {total:,.0f} | CK: 0 | VAT 10%: {vat:,.0f} -> Tổng: {final_total:,.0f} VNĐ [{category}]")

    except ValueError:
        print(f"Xử lý lỗi [{order_id}]: Số tiền '{raw_total}' không hợp lệ! Bỏ qua đơn hàng.")


print("BÁO CÁO XỬ LÝ HÓA ĐƠN AN TOÀN (TRY-EXCEPT & VAT)")

for order in orders:
    safe_process_invoice(order["id"], order["total"], order["discount_code"], order["is_vip"])