import logging
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_403_FORBIDDEN

from app.models.document import Document, DocumentCreate

LOG = logging.getLogger(__name__)


class DocumentMongoRepository:
    """
    A repository for accessing Documents collection
    Attributes:
        client (AsyncIOMotorClient): Motor MongoDB client
        db_name (str): The Database name
    """

    def __init__(self, client: AsyncIOMotorClient, db_name: str = "tdd_workshop"):
        self.client: AsyncIOMotorClient = client
        self.db_name = client[db_name]
        self.collection = self.db_name["documents"]

    async def list_documents(self,owner_id: str) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs

    async def get_document(self, doc_id: str,owner_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(f"Find by id: {doc_id}")
        doc = await self.collection.find_one({"_id": ObjectId(doc_id)})
        LOG.debug(f"Response: {doc}")
        if doc:
            doc["id"] = str(doc["_id"])
            if doc["owner_id"] == owner_id:
              return Document(**doc)
            else:
              raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail="Forbidden")
        return None

    async def create_document(self, document_create: DocumentCreate,current_user: str) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(Path(document_create.title).name, safe="")
        document: Document = Document(
            id="",
            title=document_create.title,
            description=document_create.description,
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def delete_document(self, doc_id: str,current_user: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = await self.collection.delete_one({"_id": doc_id})
        return result.deleted_count > 0
