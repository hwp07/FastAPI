from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    subject: str
    document_type: str
    file_url: str

class DocumentResponse(BaseModel):
    id: int
    title: str
    subject: str
    document_type: str
    file_url: str

