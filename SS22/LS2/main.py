from fastapi import FastAPI

from routers.medical import router as medical_router
from routers.prescriptions import router as prescription_router


app = FastAPI(
    title="MedCare E-Prescription API",
    version="1.0.0",
)


app.include_router(medical_router)
app.include_router(prescription_router)


@app.get("/")
def root():
    return {
        "message": "MedCare API is running"
    }