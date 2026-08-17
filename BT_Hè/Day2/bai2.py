students = [
    {
        "id": "SV01",
        "name": " Nguyen Van An ",
        "email": " an.nguyen@rikkei.edu.vn ",
        "phone": " 0987654321 "
    },
    {
        "id": "SV02",
        "name": " Tran Thi Bich ",
        "email": " bich_gmail.com ",
        "phone": " 0912345678 "
    },
    {
        "id": "SV03",
        "name": " Le Hoang Cuong ",
        "email": " cuong@gmail.com ",
        "phone": " 09876abcde "
    },
    {
        "id": "SV04",
        "name": " Pham Minh Dung ",
        "email": " dung@gmail.com ",
        "phone": " 0355667788 "
    }
]


for student in students:
    name = student["name"].strip()
    email = student["email"].strip()
    phone = student["phone"].strip()

    email_valid = (
        email.count("@") == 1 and (
            email.endswith(".com") or email.endswith(".edu.vn")
        )
    )

    phone_valid = (
        len(phone) == 10
        and phone.startswith("0")
        and phone.isdigit()
    )

    print(f"[{student['id']}] {name} | Email: {email} | SDT: {phone}", end=" -> ")

    if email_valid and phone_valid:
        print("HO SO HOP LE")
    elif not email_valid:
        print("KHONG HOP LE (Thieu @)")
    else:
        print("KHONG HOP LE (SDT chua chu)")