from fastapi import FastAPI, status, HTTPException, Request
from typing import Any
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

orders_db = [
    {"id": 1, "code": "SP001", "status": "PENDING"},
    {"id": 2, "code": "SP002", "status": "DELIVERED"},
]
app = FastAPI()


# Any nó là kiểu dữ liệu bất kỳ
# định nghĩa cho 1 hàm để dùng chung cho cả 3 tầng
def respone_json(
    statusCode: int, message: str, data: Any, error: str, timestamp: str, path: str
):
    return JSONResponse(
        satus_code=statusCode,
        content={
            "statusCode": statusCode,
            "message": message,
            "data": data,
            "error": error,
            "timestamp": timestamp,
            "path": path,
        },
    )


# tầng 1 lỗi do người dùng
# duy nhất tàng RequestValidationError có phương thức error()
@app.exception_handler(RequestValidationError)
def exception_validate(request: Request, exception: RequestValidationError):
    return respone_json(
        statusCode=status.HTTPException_422_UNPROCESSABLE_ENTITY,  # còn ở đây ko raise ra nên mình phải tự định nghĩa
        # nếu nó raise ra thì . như cái dưới
        message="Lỗi người dùng",
        data=None,
        error=request.error(),
        path=request.url.path,
    )


# tầng 2 :Lỗi do dev
@app.exception_handler(HTTPException)
def execption_http(request: Request, exc: HTTPException):
    return respone_json(
        statusCode=exc.status_code,  # ở đây vì nó sẽ đc raise ra nên là mình có thể . ra như này
        message=exc.detail,
        data=None,
        error=exc.detail,
        path=request.url.path,
    )


# taangf 3:Lỗi do server
@app.exception_handler(Exception)
def exception_Exception(request: Request, exc: Exception):
    # còn ở đây ko raise ra nên mình phải tự định nghĩa
    # nếu nó raise ra thì . như cái thứ 2
    return respone_json(
        statusCode=500,
        message="Lỗi do server",
        data=None,
        error=str(e),
        path=request.url.path,
    )


@app.delete("/orders/{order_id}", status_code=status.HTTP_200_OK)
def del_order_id(order_id: int, request: Request):
    is_flag = None
    for i in orders_db:
        if i["id"] == order_id:
            is_flag = i
            break
    if is_flag is None:
        raise HTTPException(status_code=404, detail="loi k tim thay id")

    if is_flag["status"] == "DELIVERED":
        raise HTTPException(status_code=400, detail="k dc phep huy")

    is_flag["status"] = "CANCELLED"

    return respone_json(
        statusCode=200,
        message="da thay doi trang thai thanh cong",
        data=is_flag,
        error=None,
        path=request.path.url,
    )