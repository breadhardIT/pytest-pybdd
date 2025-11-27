import logging
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.config import settings
from app.models.document import Document, DocumentCreate
from app.repository.document_mongo_repository import DocumentMongoRepository
from app.repository.document_s3_repository import S3Repository

LOG = logging.getLogger(__name__)
router = APIRouter()
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_get_mongo_repo__mutmut_orig() -> DocumentMongoRepository:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
    return DocumentMongoRepository(client, db_name=settings.mongodb_db)


def x_get_mongo_repo__mutmut_1() -> DocumentMongoRepository:
    client: AsyncIOMotorClient = None
    return DocumentMongoRepository(client, db_name=settings.mongodb_db)


def x_get_mongo_repo__mutmut_2() -> DocumentMongoRepository:
    client: AsyncIOMotorClient = AsyncIOMotorClient(None)
    return DocumentMongoRepository(client, db_name=settings.mongodb_db)


def x_get_mongo_repo__mutmut_3() -> DocumentMongoRepository:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
    return DocumentMongoRepository(None, db_name=settings.mongodb_db)


def x_get_mongo_repo__mutmut_4() -> DocumentMongoRepository:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
    return DocumentMongoRepository(client, db_name=None)


def x_get_mongo_repo__mutmut_5() -> DocumentMongoRepository:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
    return DocumentMongoRepository(db_name=settings.mongodb_db)


def x_get_mongo_repo__mutmut_6() -> DocumentMongoRepository:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
    return DocumentMongoRepository(client, )

x_get_mongo_repo__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_mongo_repo__mutmut_1': x_get_mongo_repo__mutmut_1, 
    'x_get_mongo_repo__mutmut_2': x_get_mongo_repo__mutmut_2, 
    'x_get_mongo_repo__mutmut_3': x_get_mongo_repo__mutmut_3, 
    'x_get_mongo_repo__mutmut_4': x_get_mongo_repo__mutmut_4, 
    'x_get_mongo_repo__mutmut_5': x_get_mongo_repo__mutmut_5, 
    'x_get_mongo_repo__mutmut_6': x_get_mongo_repo__mutmut_6
}

def get_mongo_repo(*args, **kwargs):
    result = _mutmut_trampoline(x_get_mongo_repo__mutmut_orig, x_get_mongo_repo__mutmut_mutants, args, kwargs)
    return result 

get_mongo_repo.__signature__ = _mutmut_signature(x_get_mongo_repo__mutmut_orig)
x_get_mongo_repo__mutmut_orig.__name__ = 'x_get_mongo_repo'


def x_get_s3_repo__mutmut_orig() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        bucket=settings.s3_bucket,
    )


def x_get_s3_repo__mutmut_1() -> S3Repository:
    return S3Repository(
        endpoint_url=None,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        bucket=settings.s3_bucket,
    )


def x_get_s3_repo__mutmut_2() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=None,
        secret_key=settings.s3_secret_key,
        bucket=settings.s3_bucket,
    )


def x_get_s3_repo__mutmut_3() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        secret_key=None,
        bucket=settings.s3_bucket,
    )


def x_get_s3_repo__mutmut_4() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        bucket=None,
    )


def x_get_s3_repo__mutmut_5() -> S3Repository:
    return S3Repository(
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        bucket=settings.s3_bucket,
    )


def x_get_s3_repo__mutmut_6() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        secret_key=settings.s3_secret_key,
        bucket=settings.s3_bucket,
    )


def x_get_s3_repo__mutmut_7() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        bucket=settings.s3_bucket,
    )


def x_get_s3_repo__mutmut_8() -> S3Repository:
    return S3Repository(
        endpoint_url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        )

x_get_s3_repo__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_s3_repo__mutmut_1': x_get_s3_repo__mutmut_1, 
    'x_get_s3_repo__mutmut_2': x_get_s3_repo__mutmut_2, 
    'x_get_s3_repo__mutmut_3': x_get_s3_repo__mutmut_3, 
    'x_get_s3_repo__mutmut_4': x_get_s3_repo__mutmut_4, 
    'x_get_s3_repo__mutmut_5': x_get_s3_repo__mutmut_5, 
    'x_get_s3_repo__mutmut_6': x_get_s3_repo__mutmut_6, 
    'x_get_s3_repo__mutmut_7': x_get_s3_repo__mutmut_7, 
    'x_get_s3_repo__mutmut_8': x_get_s3_repo__mutmut_8
}

def get_s3_repo(*args, **kwargs):
    result = _mutmut_trampoline(x_get_s3_repo__mutmut_orig, x_get_s3_repo__mutmut_mutants, args, kwargs)
    return result 

get_s3_repo.__signature__ = _mutmut_signature(x_get_s3_repo__mutmut_orig)
x_get_s3_repo__mutmut_orig.__name__ = 'x_get_s3_repo'


def x_document_create_form__mutmut_orig(
    title: str = Form(...), description: str = Form(...)
) -> DocumentCreate:
    return DocumentCreate(title=title, description=description)


def x_document_create_form__mutmut_1(
    title: str = Form(...), description: str = Form(...)
) -> DocumentCreate:
    return DocumentCreate(title=None, description=description)


def x_document_create_form__mutmut_2(
    title: str = Form(...), description: str = Form(...)
) -> DocumentCreate:
    return DocumentCreate(title=title, description=None)


def x_document_create_form__mutmut_3(
    title: str = Form(...), description: str = Form(...)
) -> DocumentCreate:
    return DocumentCreate(description=description)


def x_document_create_form__mutmut_4(
    title: str = Form(...), description: str = Form(...)
) -> DocumentCreate:
    return DocumentCreate(title=title, )

x_document_create_form__mutmut_mutants : ClassVar[MutantDict] = {
'x_document_create_form__mutmut_1': x_document_create_form__mutmut_1, 
    'x_document_create_form__mutmut_2': x_document_create_form__mutmut_2, 
    'x_document_create_form__mutmut_3': x_document_create_form__mutmut_3, 
    'x_document_create_form__mutmut_4': x_document_create_form__mutmut_4
}

def document_create_form(*args, **kwargs):
    result = _mutmut_trampoline(x_document_create_form__mutmut_orig, x_document_create_form__mutmut_mutants, args, kwargs)
    return result 

document_create_form.__signature__ = _mutmut_signature(x_document_create_form__mutmut_orig)
x_document_create_form__mutmut_orig.__name__ = 'x_document_create_form'


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


@router.post("/", response_model=Document, status_code=HTTP_201_CREATED)
async def post_document(
    metadata: DocumentCreate = Depends(document_create_form),
    file: UploadFile = File(...),
    mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
    s3_repo: S3Repository = Depends(get_s3_repo),
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
    s3_repo: S3Repository = Depends(get_s3_repo),
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


@router.delete("/{document_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    mongo_repo: DocumentMongoRepository = Depends(get_mongo_repo),
    s3_repo: S3Repository = Depends(get_s3_repo),
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
        raise HTTPException(status_code=404, detail="Document not found")
    s3_repo.delete_file(doc.key)
    await mongo_repo.delete_document(document_id)
