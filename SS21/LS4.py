"""
 Vấn đề                                            | Nguy cơ                                                                                                                      | Cách khắc phục                                                                                                                    

 1. mật khẩu được so sánh trực tiếp                | có thể đang lưu mật khẩu dạng plaintext trong DB, nếu DB bị lộ toàn bộ mật khẩu người dùng bị lộ                             | sử dung bcrypt để băm mật khẩu và dùng verify() để kiểm tra
 2. đưa mật khẩu vào JWT                           | JWT chứa password, khiến mật khẩu trở thành một phần của token, nếu token bị đánh cắp/giải mã payload, mật khẩu có thể bị lộ | tuyệt đối không đưa password vào JWT, hỉ lưu các thông tin cần thiết như sub (user ID), role, exp
 3. hard-code JWT secret "123456"                  | secret quá yếu và nằm trực tiếp trong source code, có thể dễ dàng giả mạo JWT nếu biết secret                                | sinh secret mạnh, dài và ngẫu nhiên, lưu trong Environment Variables / Secret Manager, không hard-code
 4. không có thời gian hết hạn JWT                 | token có thể tồn tại vô thời hạn, có thể sử dụng lâu dài nếu rơi vào tay kẻ xấu sẽ rất nguy hiểm                             | thêm thời hạn sử dụng cho token
 5. tiết lộ email có tồn tại hay không             | "Email không tồn tại" và "Mật khẩu không chính xác" cho phép kẻ xấu dò danh sách tài khoảnn                                  | nên trả về thông báo chung chung, ví dụ: "Email hoặc mật khẩu không chính xác"

"""

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my-secret-key")
ALGORITHM = "HS256"


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    # check email + password
    if user is None or not pwd_context.verify(data.password,user.password):
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # tạo JWT
    payload = {
        "email": user.email,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # trả token
    return {
        "success": True,
        "access_token": token
    }

"""
luồng xử lý:
1. login
2. check
    2.1: success -> tạo JWR -> trả token
    2.2: fail -> lỗi 401
"""