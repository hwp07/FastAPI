from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import Base,engine,get_db
from schemas import DocumentCreate
from document_service import get_documents_service,create_document_service,delete_document_service

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/documents",status_code=status.HTTP_200_OK)
def get_documents(db: Session = Depends(get_db)):
    documents = get_documents_service(db)

    return {
        "message": "Document list",
        "data": documents
    }


@app.post("/documents",status_code=status.HTTP_201_CREATED)
def create_document(document: DocumentCreate,db: Session = Depends(get_db)):
    new_document = create_document_service(db,document)

    return {
        "message": "Document created successfully",
        "data": new_document
    }

@app.delete("/documents/{document_id}",status_code=status.HTTP_200_OK)
def delete_document(document_id: int,db: Session = Depends(get_db)):
    document = delete_document_service(db,document_id)

    return {
        "message": "Document deleted successfully",
        "data": document
    }