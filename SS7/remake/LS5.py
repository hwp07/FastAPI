from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

orders_db = [
    {"id": 1, "code": "SP001", "status": "PENDING"},
    {"id": 2, "code": "SP002", "status": "DELIVERED"},
]


# Hàm trả về response chung
def response_json(
    statusCode: int,
    message: str,
    data: Any,
    error: Any,
    path: str,
):
    return JSONResponse(
        status_code=statusCode,
        content={
            "statusCode": statusCode,
            "message": message,
            "data": data,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "path": path,
        },
    )


# =========================
# Exception tầng 1: Lỗi người dùng
# =========================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return response_json(
        statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Dữ liệu đầu vào không hợp lệ",
        data=None,
        error=exc.errors(),
        path=request.url.path,
    )


# =========================
# Exception tầng 2: Lỗi nghiệp vụ (HTTPException)
# =========================
@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    return response_json(
        statusCode=exc.status_code,
        message=exc.detail,
        data=None,
        error=exc.detail,
        path=request.url.path,
    )


# =========================
# Exception tầng 3: Lỗi server
# =========================
@app.exception_handler(Exception)
async def exception_handler(
    request: Request,
    exc: Exception,
):
    return response_json(
        statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Lỗi hệ thống",
        data=None,
        error=str(exc),
        path=request.url.path,
    )


# =========================
# API hủy đơn hàng
# =========================
@app.delete("/orders/{order_id}", status_code=status.HTTP_200_OK)
def cancel_order(order_id: int, request: Request):

    order = None

    for item in orders_db:
        if item["id"] == order_id:
            order = item
            break

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đơn hàng",
        )

    if order["status"] == "DELIVERED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không được phép hủy đơn hàng đã giao",
        )

    if order["status"] == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Đơn hàng đã được hủy trước đó",
        )

    order["status"] = "CANCELLED"

    return response_json(
        statusCode=status.HTTP_200_OK,
        message="Hủy đơn hàng thành công",
        data=order,
        error=None,
        path=request.url.path,
    )