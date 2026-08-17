from pydantic import BaseModel, CongifDict


class ClassroomResponse(BaseModel):
    class_code: str
    class_name: str
    status: str
    max_students: int

    model_config = ConfigDict(from_attibutes=True)