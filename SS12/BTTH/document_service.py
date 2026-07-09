from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import DocumentModel
from schemas import DocumentCreate

def get_documents_service(db: Session):
    return db.query(DocumentModel).all()

def create_document_service(db: Session,document: DocumentCreate):
    new_document = DocumentModel(
        title=document.title,
        subject=document.subject,
        document_type=document.document_type,
        file_url=document.file_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


def delete_document_service(db: Session,document_id: int):
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    result = {
        "id": document.id,
        "title": document.title,
        "subject": document.subject,
        "document_type": document.document_type,
        "file_url": document.file_url
    }

    db.delete(document)
    db.commit()

    return result