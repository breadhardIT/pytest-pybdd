import logging
from typing import List

from bson import ObjectId
from pytest_bdd import given, parsers, scenarios, then, when

from app.models.document import Document
from app.repository.document_s3_repository import S3Repository
from conftest import jwt_token_for_user, create_test_token, get_auth_headers
from factory.documents_mother import create_document_request

scenarios("../features/documents.feature")
LOG = logging.getLogger(__name__)


@given("Database contains documents")
def there_are_documents_in_database(client, context):
    LOG.debug("Loading documents")
    documents: list[Document] = []
    for _ in range(10):
        response = client.post(
            "/documents",
            data=create_document_request().model_dump(),
            files={"file": ("file_name.txt", b"Document content", "text/plain")},
            headers=get_auth_headers(context=context)
        )
        assert response.status_code == 201
        assert response.json()
        documents.append(Document.model_validate(response.json()))
        LOG.debug(f"Document {response.json()} loaded")
    context["documents"] = documents

@given("documents owned by:")
def documents_owned_by(datatable, client, context):

    if not "documents" in context:
      context["documents"] = []

    for row in datatable:
        user_id = row[0]
        documents = int(row[1])
        for _ in range(documents):
            token = create_test_token(user_id=user_id)
            response = client.post(
                "/documents",
                data=create_document_request().model_dump(),
                files={"file": ("file_name.txt", b"Document content", "text/plain")},
                headers={"Authorization": f"Bearer {token}"}
            )

        assert response.status_code == 201
        context["documents"].append(Document.model_validate(response.json()))


@given("a document create request")
def document_create_request(context):
    context["document"] = create_document_request()

@given("API is running")
def api_running(client,context):
    response = client.get("/docs")
    assert response.status_code == 200


@when("I get all documents")
def get_documents(client, context):
    response = client.get("/documents",headers=get_auth_headers(context=context))
    context["response"] = response


@when("I get a non existing document")
def get_non_existing_document(client, context):
    response = client.get(f"/documents/{str(ObjectId())}",headers=get_auth_headers(context=context))
    context["response"] = response


@when("I delete a existing document")
def get_delete_existing_document(client, context):
    response = client.delete(f'/documents/{str(context["documents"][0].id)}',headers=get_auth_headers(context=context))
    context["response"] = response


@when("I delete a non existing document")
def get_delete_non_existing_document(client, context):
    response = client.delete(f"/documents/{str(ObjectId())}",headers=get_auth_headers(context=context))
    context["response"] = response


@when("I get an existing document")
def get_existing_document(client, context):
    response = client.get(f'/documents/{context["documents"][0].id}',headers=get_auth_headers(context=context))
    context["response"] = response

@when("I create a document")
def post_document(client,context):
    response = client.post(
        "/documents",
        data=create_document_request().model_dump(),
        files={"file": ("file_name.txt", b"Document content", "text/plain")},
        headers=get_auth_headers(context=context)
    )
    context["response"] = response


@then(parsers.parse("response is {code:d}"))
def check_status(context, code):
    assert context["response"].status_code == code


@then("response is an empty list")
def check_empty_list(context):
    assert context["response"].json() == []


@then("response contains a list of documents")
def response_contains_a_list_of_documents(context):
    assert isinstance(context["response"].json(), list)
    assert all(isinstance(element, dict) for element in context["response"].json())
    assert all(
        Document.model_validate(element) for element in context["response"].json()
    )

@then("response contains only my documents")
def response_only_my_documents(context):
    docs : List[Document] = []
    [docs.append(Document.model_validate(element)) for element in context["response"].json()]
    assert not [doc for doc in docs if doc.owner_id != context["user_id"]]

@then("response is the expected document")
def response_is_expected_document(context):
    LOG.debug(f'Response: {context["response"]}')
    LOG.debug(f'Response body: {context["response"].json()}')
    doc: Document = Document.model_validate(context["response"].json())
    assert doc.id == context["documents"][0].id
    assert doc.description == context["documents"][0].description


@then("document was deleted")
def document_was_deleted(client, context):
    response = client.get(f'/documents/{context["documents"][0].id}',headers=get_auth_headers(context=context))
    assert response.status_code == 404


@then("document doesn't exist in bucket")
def document_doesnt_exist_in_bucket(s3_repo: S3Repository, context):
    assert not s3_repo.file_exists(context["documents"][0].title)
