raw_registers = [
    {"name": "  Nguyen Van An  ", "email": "an.nguyen@gmail.com", "phone": "0987654321"},
    {"name": "Tran Thi Bich", "email": "bich_gmail.com", "phone": "0912345678"},
    {"name": "Le Hoang Cuong", "email": "cuong@rikkei.edu.vn", "phone": "0123456789"},
    {"name": "  Pham Minh Dung ", "email": "dung@gmail.com  ", "phone": "0355667788"}
]


def validate_registration_input(name, email, phone):
    new_name = name.strip()
    new_email = email.strip()
    new_phone = phone.strip()

    email_valid = "@" in new_email

    phone_valid = ("03", "05", "07", "08", "09")
    phone_true = len(new_phone) == 10 and new_phone.isdigit() and new_phone.startswith(phone_valid)

    return new_name, new_phone, new_email, email_valid, phone_true


for res in raw_registers:
    clean_name, clean_phone, clean_email, email_valid, phone_valid = validate_registration_input(res["name"], res["email"], res["phone"])
    status = "HỢP LỆ" if (email_valid and phone_valid) else "KHÔNG HỢP LỆ"

    print(f"[{clean_name}] Email: {clean_email} | SDT: {clean_phone} -> {status}")