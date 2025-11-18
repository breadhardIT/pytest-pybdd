import logging
import uuid
from logging import getLevelName

from bson import ObjectId
from pytest_bdd import given, when, then, scenarios, parsers

from app.models.document import Document
from factory.documents_factory import create_document_request_factory

scenarios("../features/documents.feature")
LOG = logging.getLogger(__name__)

@given("Database contains documents")
def there_are_documents_in_database(client,context):
    LOG.info("Loading documents")
    documents: list[Document] = []
    for _ in range(10):
        response = client.post("/documents",
                                data=create_document_request_factory().model_dump(),
                                files={"file": ("file_name.txt",b"Document content","text/plain")},
                               )
        assert response.status_code == 201
        assert response.json()
        documents.append(Document.model_validate(response.json()))
        LOG.info(f"Document {response.json()} loaded")
    context["documents"] = documents

@given("API is running")
def api_running(client):
    response = client.get("/docs")
    assert response.status_code == 200

@when('I get all documents')
def get_documents(client, context):
    response = client.get("/documents")
    context["response"] = response

@when('I get a non existing document')
def get_non_existing_document(client,context):
    response = client.get(f"/documents/{str(ObjectId())}")
    context["response"] = response

@when('I get an existing document')
def get_existing_document(client,context):
    response = client.get(f"/documents/{context["documents"][0].id}")
    context["response"] = response

@then(parsers.parse("response is {code:d}"))
def check_status(context,code):
    assert context["response"].status_code == code


@then("response is an empty list")
def check_empty_list(context):
    assert context["response"].json() == []

@then("response contains a list of documents")
def response_contains_a_list_of_documents(context):
    assert isinstance(context["response"].json(),list)
    assert all(isinstance(element, dict) for element in context["response"].json())
    assert all(Document.model_validate(element)  for element in context["response"].json())

@then("response is the expected document")
def response_is_expected_document(context):
    LOG.info(f"Response: {context["response"]}")
    LOG.info(f"Response body: {context["response"].json()}")
    doc : Document = Document.model_validate(context["response"].json())
    assert doc.id == context["documents"][0].id
    assert doc.description == context["documents"][0].description
