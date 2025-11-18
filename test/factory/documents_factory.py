import uuid

from app.models.document import DocumentCreate


def create_document_request_factory() -> DocumentCreate:
    return DocumentCreate(title=f"title_{uuid.uuid4().hex}", description=f"description {uuid.uuid4().hex}")

