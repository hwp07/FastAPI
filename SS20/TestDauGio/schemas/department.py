from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    id: int
    department_code: str
    department_name: str

    class Config:
        from_attributes = True
