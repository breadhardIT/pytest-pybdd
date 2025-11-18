import logging

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.config import settings
from app.models.document import Document, DocumentCreate
from app.repository.document_mongo_repository import DocumentMongoRepository
from app.repository.document_s3_repository import S3Repository

LOG = logging.getLogger(__name__)
router = APIRouter()

def get_mongo_repo() -> DocumentMongoRepository:
    client = AsyncIOMotorClient(settings.mongodb_uri)
    return DocumentMongoRepository(client, db_name=settings.mongodb_db)

def get_s3_repo() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        bucket=settings.s3_bucket
    )

def document_create_form(
    title: str = Form(...),
    description: str = Form(...)
) -> DocumentCreate:
    return DocumentCreate(title=title, description=description)

@router.get("/", response_model=List[Document])
async def list_documents(
        mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
        s3_repo: S3Repository = Depends(get_s3_repo),
) -> List[Document]:
    """
    Get a List of Documents
    Args:
        mongo_repo (DocumentMongoRepository): MongoDB Repository for accessing metadata
        s3_repo (S3Repository): S3 Repository for accessing files
    Returns:
        documents (List[Document]): The whole list of existing documents
    """
    LOG.debug("Get the documents list")
    docs = await mongo_repo.list_documents()
    LOG.debug(f"Document list has {len(docs)} elements")
    for doc in docs:
        doc.file_path = s3_repo.generate_presigned_url_for_get(doc.key)
    return docs

@router.post("/", response_model=Document,status_code=HTTP_201_CREATED)
async def post_document(
    metadata: DocumentCreate = Depends(document_create_form),
    file: UploadFile = File(...),
    mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
    s3_repo: S3Repository = Depends(get_s3_repo)
) -> Document:
    """
    Post a document
    Args:
        metadata(DocumentCreate): The title and description of the document
        file(UploadFile): The file content in bytes
        mongo_repo(DocumentMongoRepository): The documents repository
        s3_repo(S3Repository): The S3 Bucket repository
    Returns:
        document (Document): The created document with a presigned url for downloading the file
    """
    content: bytes = await file.read()
    doc = await mongo_repo.create_document(metadata)
    s3_repo.upload_file(content, doc.key)
    doc.file_path = s3_repo.generate_presigned_url_for_get(doc.key)
    return doc

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
    s3_repo: S3Repository = Depends(get_s3_repo)
) -> Document:
    """
    Get a document
    Args:
        document_id (str): The unique document identifier
        mongo_repo(DocumentMongoRepository): The documents repository
        s3_repo(S3Repository): The S3 Bucket repository
    Returns:
        document (Document): The created document with a presigned url for downloading the file
    """
    LOG.debug(f"Get document {document_id}")
    doc = await mongo_repo.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.file_path = s3_repo.generate_presigned_url_for_get(doc.key)
    return doc

@router.delete("/{document_id}",status_code=HTTP_204_NO_CONTENT)
async def delete_document(
        document_id: str,
        mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
        s3_repo: S3Repository = Depends(get_s3_repo)
):
    """
    Delete document
    Args:
        document_id (str): The unique document identifier
        mongo_repo(DocumentMongoRepository): The documents repository
        s3_repo(S3Repository): The S3 Bucket repository
    """
    LOG.debug(f"Delete document {document_id}")
    doc: Document = await mongo_repo.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404,detail="Document not found")
    s3_repo.delete_file(doc.key)
    await mongo_repo.delete_document(document_id)
