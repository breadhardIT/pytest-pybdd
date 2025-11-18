from typing import Optional

from pydantic import BaseModel


class Document(BaseModel):
    """
    Represents the metadata for accessing a Document
    Attributes:
        id (str): Unique document identifier
        title (str): Document title
        description (str): Document description
        key (str): The unique file name where the file resides
        file_path (str): The URL where the document can be accessed
    """
    id: str
    title: str
    description: str
    key: str
    file_path: Optional[str]


class DocumentCreate(BaseModel):
    title: str
    description: str
