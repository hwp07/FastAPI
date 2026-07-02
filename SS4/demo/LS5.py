from fastapi import FastAPI,status
from pydantic import BaseModel,Field,EmailStr,field_validator


app=FastAPI()
data=[]


class Students(BaseModel):
    full_name:str=Field(...,min_length=3,)
    email:EmailStr
    age:int=Field(...,ge=15,le=60)
    phone:str=Field(...,min_length=10,max_length=11,examples=["0464848286"])
    note:str=Field(...,max_length=200,examples=["Anh Dương"])
    @field_validator("phone")
    def check(phone):
        if not phone.isdigit():
            raise ValueError("Sai định dạng")
        return False


@app.post("/students/regitster",status_code=status.HTTP_201_CREATED)
def create_student(student:Students):
    data.append(student.model_dump())
    return {
        "message":"Đã thêm code thành công",
        "data":student
    }
