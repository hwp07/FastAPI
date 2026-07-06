from fastapi import FastAPI,HTTPException,status


app = FastAPI()

orders_list = [
    {"id": 1, "code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    {"id": 2, "code": "SP002", "payment_status": "UNPAID", "method": "NONE"}
]

@app.get('/orders/{order_id}/payment')
def get_order(order_id:int):
    try:
        product = orders_list.get(order_id)
        if not product :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='khong tim thay id'
            )
        return {
            'payment_status' : product['payment_status'],
            'method' : product['method']
        }
    except HTTPException  :
        raise
    except Exception as e :
        raise HTTPException (
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f'loi do server'
        )