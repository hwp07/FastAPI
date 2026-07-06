from fastapi import FastAPI, Response, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date
from typing import Optional

app = FastAPI()

class Carrier(BaseModel):
    code: str
    name: str
    max_weight_capacity: int
    status: str

class Shipment(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int
    dispatch_date: date
    shift: str



carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]

@app.post("/carriers", status_code=status.HTTP_201_CREATED)
def create_carrier(carrier: Carrier):
    for c in carriers:
        if c["code"].lower() == carrier.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Carrier code đã tồn tại"
            )

    if not carrier.name or len(carrier.name.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Tên không hợp lệ"
        )

    if carrier.max_weight_capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Khối lượng không hợp lệ"
        )

    if carrier.status not in ["ACTIVE", "INACTIVE", "SUSPENDED"]:
        raise HTTPException(
            status_code=400,
            detail="Trạng thái không hợp lệ"
        )

    new_carrier = {
        "id": len(carriers) + 1,
        "code": carrier.code,
        "name": carrier.name,
        "max_weight_capacity": carrier.max_weight_capacity,
        "status": carrier.status
    }

    carriers.append(new_carrier)
    return new_carrier

@app.get("/carriers", status_code=status.HTTP_200_OK)
def get_carrier():
    return {
        'message': "Lấy danh sách thành công",
        'data': carriers
    }

@app.get("/carriers/{carrier_id}", status_code=status.HTTP_200_OK)
def get_carrier_detail(carrier_id: int):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            return {
                "message": f"Carrier {carrier['name']}",
                "data": carrier
            }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy Carrier"
    )

@app.put("/carriers/{carrier_id}", status_code=status.HTTP_200_OK)
def update_carrier(carrier_id: int, carrier: Carrier):
    for c in carriers:
        if c["id"] != carrier_id and c["code"].lower() == carrier.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Carrier code đã tồn tại"
            )

    if len(carrier.name.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Tên không hợp lệ"
        )

    if carrier.max_weight_capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Khối lượng không hợp lệ"
        )

    if carrier.status not in ["ACTIVE", "INACTIVE", "SUSPENDED"]:
        raise HTTPException(
            status_code=400,
            detail="Trạng thái không hợp lệ"
        )

    for c in carriers:
        if c["id"] == carrier_id:
            c["code"] = carrier.code
            c["name"] = carrier.name
            c["max_weight_capacity"] = carrier.max_weight_capacity
            c["status"] = carrier.status

            return {
                "message": "Cập nhật thành công",
                "data": c
            }

    raise HTTPException(
        status_code=404,
        detail="Carrier not found"
    )

@app.delete("/carriers/{carrier_id}", status_code=status.HTTP_200_OK)
def delete_carrier(carrier_id: int):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            carriers.remove(carrier)

            return {
                "message": "Xóa thành công"
            }

    raise HTTPException(
        status_code=404,
        detail="Carrier not found"
    )

@app.get("/carriers", status_code=status.HTTP_200_OK)
def get_carrier(
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        min_weight: Optional[int] = None
):

    result = carriers

    if keyword:
        result = [
            c for c in result
            if keyword.lower() in c["code"].lower()
            or keyword.lower() in c["name"].lower()
        ]

    if status:
        result = [
            c for c in result
            if c["status"] == status
        ]

    if min_weight:
        result = [
            c for c in result
            if c["max_weight_capacity"] >= min_weight
        ]

    return {
        "message": "Lấy danh sách thành công",
        "data": result
    }


@app.post("/shipments", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: Shipment):
    carrier = None

    for c in carriers:
        if c["id"] == shipment.carrier_id:
            carrier = c
            break

    if carrier is None:
        raise HTTPException(
            status_code=404,
            detail="Carrier not found"
        )

    if carrier["status"] != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Carrier is not ACTIVE"
        )

    if shipment.total_weight <= 0:
        raise HTTPException(
            status_code=400,
            detail="Khối lượng không hợp lệ"
        )

    if shipment.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Vượt quá tải trọng cho phép"
        )

    if shipment.shift not in ["MORNING", "AFTERNOON", "NIGHT"]:
        raise HTTPException(
            status_code=400,
            detail="Shift không hợp lệ"
        )

    for s in shipments:
        if (
            s["carrier_id"] == shipment.carrier_id
            and s["dispatch_date"] == str(shipment.dispatch_date)
            and s["shift"] == shipment.shift
        ):
            raise HTTPException(
                status_code=400,
                detail="Carrier đã có chuyến trong ca này"
            )

    new_shipment = {
        "id": len(shipments) + 1,
        "carrier_id": shipment.carrier_id,
        "order_reference": shipment.order_reference,
        "total_weight": shipment.total_weight,
        "dispatch_date": str(shipment.dispatch_date),
        "shift": shipment.shift
    }

    shipments.append(new_shipment)

    return new_shipment

@app.get("/shipments", status_code=status.HTTP_200_OK)
def get_shipments():
    return {
        "message": "Lấy danh sách shipment thành công",
        "data": shipments
    }