from pydantic import BaseModel


class Document(BaseModel):
    """
    Represents the metadata for accessing a Document
    Attributes:
        id (str): Unique document identifier
        title (str): Document title
        description (str): Document description
        file_path (str): The URL where the document can be accessed
    """
    id: str
    title: str
    description: str
    file_path: str


class DocumentCreate(BaseModel):
    title: str
    description: str
