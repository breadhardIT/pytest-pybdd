import logging
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.document import Document, DocumentCreate

LOG = logging.getLogger(__name__)
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


class DocumentMongoRepository:
    """
    A repository for accessing Documents collection
    Attributes:
        client (AsyncIOMotorClient): Motor MongoDB client
        db_name (str): The Database name
    """

    def xǁDocumentMongoRepositoryǁ__init____mutmut_orig(self, client: AsyncIOMotorClient, db_name: str = "tdd_workshop"):
        self.client: AsyncIOMotorClient = client
        self.db_name = client[db_name]
        self.collection = self.db_name["documents"]

    def xǁDocumentMongoRepositoryǁ__init____mutmut_1(self, client: AsyncIOMotorClient, db_name: str = "XXtdd_workshopXX"):
        self.client: AsyncIOMotorClient = client
        self.db_name = client[db_name]
        self.collection = self.db_name["documents"]

    def xǁDocumentMongoRepositoryǁ__init____mutmut_2(self, client: AsyncIOMotorClient, db_name: str = "TDD_WORKSHOP"):
        self.client: AsyncIOMotorClient = client
        self.db_name = client[db_name]
        self.collection = self.db_name["documents"]

    def xǁDocumentMongoRepositoryǁ__init____mutmut_3(self, client: AsyncIOMotorClient, db_name: str = "tdd_workshop"):
        self.client: AsyncIOMotorClient = None
        self.db_name = client[db_name]
        self.collection = self.db_name["documents"]

    def xǁDocumentMongoRepositoryǁ__init____mutmut_4(self, client: AsyncIOMotorClient, db_name: str = "tdd_workshop"):
        self.client: AsyncIOMotorClient = client
        self.db_name = None
        self.collection = self.db_name["documents"]

    def xǁDocumentMongoRepositoryǁ__init____mutmut_5(self, client: AsyncIOMotorClient, db_name: str = "tdd_workshop"):
        self.client: AsyncIOMotorClient = client
        self.db_name = client[db_name]
        self.collection = None

    def xǁDocumentMongoRepositoryǁ__init____mutmut_6(self, client: AsyncIOMotorClient, db_name: str = "tdd_workshop"):
        self.client: AsyncIOMotorClient = client
        self.db_name = client[db_name]
        self.collection = self.db_name["XXdocumentsXX"]

    def xǁDocumentMongoRepositoryǁ__init____mutmut_7(self, client: AsyncIOMotorClient, db_name: str = "tdd_workshop"):
        self.client: AsyncIOMotorClient = client
        self.db_name = client[db_name]
        self.collection = self.db_name["DOCUMENTS"]
    
    xǁDocumentMongoRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDocumentMongoRepositoryǁ__init____mutmut_1': xǁDocumentMongoRepositoryǁ__init____mutmut_1, 
        'xǁDocumentMongoRepositoryǁ__init____mutmut_2': xǁDocumentMongoRepositoryǁ__init____mutmut_2, 
        'xǁDocumentMongoRepositoryǁ__init____mutmut_3': xǁDocumentMongoRepositoryǁ__init____mutmut_3, 
        'xǁDocumentMongoRepositoryǁ__init____mutmut_4': xǁDocumentMongoRepositoryǁ__init____mutmut_4, 
        'xǁDocumentMongoRepositoryǁ__init____mutmut_5': xǁDocumentMongoRepositoryǁ__init____mutmut_5, 
        'xǁDocumentMongoRepositoryǁ__init____mutmut_6': xǁDocumentMongoRepositoryǁ__init____mutmut_6, 
        'xǁDocumentMongoRepositoryǁ__init____mutmut_7': xǁDocumentMongoRepositoryǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDocumentMongoRepositoryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁDocumentMongoRepositoryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁDocumentMongoRepositoryǁ__init____mutmut_orig)
    xǁDocumentMongoRepositoryǁ__init____mutmut_orig.__name__ = 'xǁDocumentMongoRepositoryǁ__init__'

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_orig(self) -> List[Document]:
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

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_1(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = None
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_2(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find(None)
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_3(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.rfind({})
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_4(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = None
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_5(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["id"] = None
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_6(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["XXidXX"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_7(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["ID"] = str(doc["_id"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_8(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["id"] = str(None)
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_9(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["XX_idXX"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_10(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_ID"])
            docs.append(Document(**doc))
        return docs

    async def xǁDocumentMongoRepositoryǁlist_documents__mutmut_11(self) -> List[Document]:
        """
        Returns the whole list of documents
        Returns:
            documents (List[Document])
        """
        cursor = self.collection.find({})
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            docs.append(None)
        return docs
    
    xǁDocumentMongoRepositoryǁlist_documents__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDocumentMongoRepositoryǁlist_documents__mutmut_1': xǁDocumentMongoRepositoryǁlist_documents__mutmut_1, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_2': xǁDocumentMongoRepositoryǁlist_documents__mutmut_2, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_3': xǁDocumentMongoRepositoryǁlist_documents__mutmut_3, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_4': xǁDocumentMongoRepositoryǁlist_documents__mutmut_4, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_5': xǁDocumentMongoRepositoryǁlist_documents__mutmut_5, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_6': xǁDocumentMongoRepositoryǁlist_documents__mutmut_6, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_7': xǁDocumentMongoRepositoryǁlist_documents__mutmut_7, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_8': xǁDocumentMongoRepositoryǁlist_documents__mutmut_8, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_9': xǁDocumentMongoRepositoryǁlist_documents__mutmut_9, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_10': xǁDocumentMongoRepositoryǁlist_documents__mutmut_10, 
        'xǁDocumentMongoRepositoryǁlist_documents__mutmut_11': xǁDocumentMongoRepositoryǁlist_documents__mutmut_11
    }
    
    def list_documents(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDocumentMongoRepositoryǁlist_documents__mutmut_orig"), object.__getattribute__(self, "xǁDocumentMongoRepositoryǁlist_documents__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_documents.__signature__ = _mutmut_signature(xǁDocumentMongoRepositoryǁlist_documents__mutmut_orig)
    xǁDocumentMongoRepositoryǁlist_documents__mutmut_orig.__name__ = 'xǁDocumentMongoRepositoryǁlist_documents'

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_orig(self, doc_id: str) -> Optional[Document]:
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
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_1(self, doc_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(None)
        doc = await self.collection.find_one({"_id": ObjectId(doc_id)})
        LOG.debug(f"Response: {doc}")
        if doc:
            doc["id"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_2(self, doc_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(f"Find by id: {doc_id}")
        doc = None
        LOG.debug(f"Response: {doc}")
        if doc:
            doc["id"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_3(self, doc_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(f"Find by id: {doc_id}")
        doc = await self.collection.find_one(None)
        LOG.debug(f"Response: {doc}")
        if doc:
            doc["id"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_4(self, doc_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(f"Find by id: {doc_id}")
        doc = await self.collection.find_one({"XX_idXX": ObjectId(doc_id)})
        LOG.debug(f"Response: {doc}")
        if doc:
            doc["id"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_5(self, doc_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(f"Find by id: {doc_id}")
        doc = await self.collection.find_one({"_ID": ObjectId(doc_id)})
        LOG.debug(f"Response: {doc}")
        if doc:
            doc["id"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_6(self, doc_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(f"Find by id: {doc_id}")
        doc = await self.collection.find_one({"_id": ObjectId(None)})
        LOG.debug(f"Response: {doc}")
        if doc:
            doc["id"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_7(self, doc_id: str) -> Optional[Document]:
        """
        Get a single document by unique identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            document (Document | None): The document if found, null if not found
        """
        LOG.debug(f"Find by id: {doc_id}")
        doc = await self.collection.find_one({"_id": ObjectId(doc_id)})
        LOG.debug(None)
        if doc:
            doc["id"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_8(self, doc_id: str) -> Optional[Document]:
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
            doc["id"] = None
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_9(self, doc_id: str) -> Optional[Document]:
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
            doc["XXidXX"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_10(self, doc_id: str) -> Optional[Document]:
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
            doc["ID"] = str(doc["_id"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_11(self, doc_id: str) -> Optional[Document]:
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
            doc["id"] = str(None)
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_12(self, doc_id: str) -> Optional[Document]:
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
            doc["id"] = str(doc["XX_idXX"])
            return Document(**doc)
        return None

    async def xǁDocumentMongoRepositoryǁget_document__mutmut_13(self, doc_id: str) -> Optional[Document]:
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
            doc["id"] = str(doc["_ID"])
            return Document(**doc)
        return None
    
    xǁDocumentMongoRepositoryǁget_document__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDocumentMongoRepositoryǁget_document__mutmut_1': xǁDocumentMongoRepositoryǁget_document__mutmut_1, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_2': xǁDocumentMongoRepositoryǁget_document__mutmut_2, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_3': xǁDocumentMongoRepositoryǁget_document__mutmut_3, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_4': xǁDocumentMongoRepositoryǁget_document__mutmut_4, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_5': xǁDocumentMongoRepositoryǁget_document__mutmut_5, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_6': xǁDocumentMongoRepositoryǁget_document__mutmut_6, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_7': xǁDocumentMongoRepositoryǁget_document__mutmut_7, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_8': xǁDocumentMongoRepositoryǁget_document__mutmut_8, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_9': xǁDocumentMongoRepositoryǁget_document__mutmut_9, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_10': xǁDocumentMongoRepositoryǁget_document__mutmut_10, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_11': xǁDocumentMongoRepositoryǁget_document__mutmut_11, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_12': xǁDocumentMongoRepositoryǁget_document__mutmut_12, 
        'xǁDocumentMongoRepositoryǁget_document__mutmut_13': xǁDocumentMongoRepositoryǁget_document__mutmut_13
    }
    
    def get_document(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDocumentMongoRepositoryǁget_document__mutmut_orig"), object.__getattribute__(self, "xǁDocumentMongoRepositoryǁget_document__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_document.__signature__ = _mutmut_signature(xǁDocumentMongoRepositoryǁget_document__mutmut_orig)
    xǁDocumentMongoRepositoryǁget_document__mutmut_orig.__name__ = 'xǁDocumentMongoRepositoryǁget_document'

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_orig(self, document_create: DocumentCreate) -> Document:
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_1(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(None)
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_2(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = None
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_3(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(None, safe="")
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_4(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(Path(document_create.title).name, safe=None)
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_5(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(safe="")
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_6(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(Path(document_create.title).name, )
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_7(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(Path(None).name, safe="")
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_8(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(Path(document_create.title).name, safe="XXXX")
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

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_9(self, document_create: DocumentCreate) -> Document:
        """
        Creates a new document
        Args:
            document (Document): The document to create
        Returns:
            id (str): The unique document identifier
        """
        LOG.debug(f"Create document {document_create}")
        url = quote(Path(document_create.title).name, safe="")
        document: Document = None
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_10(self, document_create: DocumentCreate) -> Document:
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
            id=None,
            title=document_create.title,
            description=document_create.description,
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_11(self, document_create: DocumentCreate) -> Document:
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
            title=None,
            description=document_create.description,
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_12(self, document_create: DocumentCreate) -> Document:
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
            description=None,
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_13(self, document_create: DocumentCreate) -> Document:
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
            key=None,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_14(self, document_create: DocumentCreate) -> Document:
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
            title=document_create.title,
            description=document_create.description,
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_15(self, document_create: DocumentCreate) -> Document:
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
            description=document_create.description,
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_16(self, document_create: DocumentCreate) -> Document:
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
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_17(self, document_create: DocumentCreate) -> Document:
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
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_18(self, document_create: DocumentCreate) -> Document:
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
            )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_19(self, document_create: DocumentCreate) -> Document:
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
            id="XXXX",
            title=document_create.title,
            description=document_create.description,
            key=url,
            file_path=None,
        )
        data = document.model_dump(exclude={"id"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_20(self, document_create: DocumentCreate) -> Document:
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
        data = None
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_21(self, document_create: DocumentCreate) -> Document:
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
        data = document.model_dump(exclude=None)
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_22(self, document_create: DocumentCreate) -> Document:
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
        data = document.model_dump(exclude={"XXidXX"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_23(self, document_create: DocumentCreate) -> Document:
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
        data = document.model_dump(exclude={"ID"})
        result = await self.collection.insert_one(data)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_24(self, document_create: DocumentCreate) -> Document:
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
        result = None
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_25(self, document_create: DocumentCreate) -> Document:
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
        result = await self.collection.insert_one(None)
        document.id = str(result.inserted_id)
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_26(self, document_create: DocumentCreate) -> Document:
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
        document.id = None
        return document

    async def xǁDocumentMongoRepositoryǁcreate_document__mutmut_27(self, document_create: DocumentCreate) -> Document:
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
        document.id = str(None)
        return document
    
    xǁDocumentMongoRepositoryǁcreate_document__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDocumentMongoRepositoryǁcreate_document__mutmut_1': xǁDocumentMongoRepositoryǁcreate_document__mutmut_1, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_2': xǁDocumentMongoRepositoryǁcreate_document__mutmut_2, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_3': xǁDocumentMongoRepositoryǁcreate_document__mutmut_3, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_4': xǁDocumentMongoRepositoryǁcreate_document__mutmut_4, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_5': xǁDocumentMongoRepositoryǁcreate_document__mutmut_5, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_6': xǁDocumentMongoRepositoryǁcreate_document__mutmut_6, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_7': xǁDocumentMongoRepositoryǁcreate_document__mutmut_7, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_8': xǁDocumentMongoRepositoryǁcreate_document__mutmut_8, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_9': xǁDocumentMongoRepositoryǁcreate_document__mutmut_9, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_10': xǁDocumentMongoRepositoryǁcreate_document__mutmut_10, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_11': xǁDocumentMongoRepositoryǁcreate_document__mutmut_11, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_12': xǁDocumentMongoRepositoryǁcreate_document__mutmut_12, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_13': xǁDocumentMongoRepositoryǁcreate_document__mutmut_13, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_14': xǁDocumentMongoRepositoryǁcreate_document__mutmut_14, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_15': xǁDocumentMongoRepositoryǁcreate_document__mutmut_15, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_16': xǁDocumentMongoRepositoryǁcreate_document__mutmut_16, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_17': xǁDocumentMongoRepositoryǁcreate_document__mutmut_17, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_18': xǁDocumentMongoRepositoryǁcreate_document__mutmut_18, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_19': xǁDocumentMongoRepositoryǁcreate_document__mutmut_19, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_20': xǁDocumentMongoRepositoryǁcreate_document__mutmut_20, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_21': xǁDocumentMongoRepositoryǁcreate_document__mutmut_21, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_22': xǁDocumentMongoRepositoryǁcreate_document__mutmut_22, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_23': xǁDocumentMongoRepositoryǁcreate_document__mutmut_23, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_24': xǁDocumentMongoRepositoryǁcreate_document__mutmut_24, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_25': xǁDocumentMongoRepositoryǁcreate_document__mutmut_25, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_26': xǁDocumentMongoRepositoryǁcreate_document__mutmut_26, 
        'xǁDocumentMongoRepositoryǁcreate_document__mutmut_27': xǁDocumentMongoRepositoryǁcreate_document__mutmut_27
    }
    
    def create_document(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDocumentMongoRepositoryǁcreate_document__mutmut_orig"), object.__getattribute__(self, "xǁDocumentMongoRepositoryǁcreate_document__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create_document.__signature__ = _mutmut_signature(xǁDocumentMongoRepositoryǁcreate_document__mutmut_orig)
    xǁDocumentMongoRepositoryǁcreate_document__mutmut_orig.__name__ = 'xǁDocumentMongoRepositoryǁcreate_document'

    async def xǁDocumentMongoRepositoryǁdelete_document__mutmut_orig(self, doc_id: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = await self.collection.delete_one({"_id": doc_id})
        return result.deleted_count > 0

    async def xǁDocumentMongoRepositoryǁdelete_document__mutmut_1(self, doc_id: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = None
        return result.deleted_count > 0

    async def xǁDocumentMongoRepositoryǁdelete_document__mutmut_2(self, doc_id: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = await self.collection.delete_one(None)
        return result.deleted_count > 0

    async def xǁDocumentMongoRepositoryǁdelete_document__mutmut_3(self, doc_id: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = await self.collection.delete_one({"XX_idXX": doc_id})
        return result.deleted_count > 0

    async def xǁDocumentMongoRepositoryǁdelete_document__mutmut_4(self, doc_id: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = await self.collection.delete_one({"_ID": doc_id})
        return result.deleted_count > 0

    async def xǁDocumentMongoRepositoryǁdelete_document__mutmut_5(self, doc_id: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = await self.collection.delete_one({"_id": doc_id})
        return result.deleted_count >= 0

    async def xǁDocumentMongoRepositoryǁdelete_document__mutmut_6(self, doc_id: str) -> bool:
        """
        Delete the document with the provided identifier
        Args:
            doc_id (str): The unique document identifier
        Returns:
            result (bool): True if deleted, false if not found
        """
        result = await self.collection.delete_one({"_id": doc_id})
        return result.deleted_count > 1
    
    xǁDocumentMongoRepositoryǁdelete_document__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDocumentMongoRepositoryǁdelete_document__mutmut_1': xǁDocumentMongoRepositoryǁdelete_document__mutmut_1, 
        'xǁDocumentMongoRepositoryǁdelete_document__mutmut_2': xǁDocumentMongoRepositoryǁdelete_document__mutmut_2, 
        'xǁDocumentMongoRepositoryǁdelete_document__mutmut_3': xǁDocumentMongoRepositoryǁdelete_document__mutmut_3, 
        'xǁDocumentMongoRepositoryǁdelete_document__mutmut_4': xǁDocumentMongoRepositoryǁdelete_document__mutmut_4, 
        'xǁDocumentMongoRepositoryǁdelete_document__mutmut_5': xǁDocumentMongoRepositoryǁdelete_document__mutmut_5, 
        'xǁDocumentMongoRepositoryǁdelete_document__mutmut_6': xǁDocumentMongoRepositoryǁdelete_document__mutmut_6
    }
    
    def delete_document(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDocumentMongoRepositoryǁdelete_document__mutmut_orig"), object.__getattribute__(self, "xǁDocumentMongoRepositoryǁdelete_document__mutmut_mutants"), args, kwargs, self)
        return result 
    
    delete_document.__signature__ = _mutmut_signature(xǁDocumentMongoRepositoryǁdelete_document__mutmut_orig)
    xǁDocumentMongoRepositoryǁdelete_document__mutmut_orig.__name__ = 'xǁDocumentMongoRepositoryǁdelete_document'
