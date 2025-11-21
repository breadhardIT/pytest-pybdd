Feature: Document Management

  Scenario: GET documents without documents
    Given API is running
    And a valid JWT token for user "John"
    When I get all documents
    Then response is 200
    And response is an empty list

  Scenario: GET documents with documents
    Given API is running
    And a valid JWT token for user "John"
    And Database contains documents
    When I get all documents
    Then response is 200
    And response contains a list of documents

  Scenario: GET /documents/document with non existing documents
    Given API is running
    And a valid JWT token for user "John"
    And Database contains documents
    When I get a non existing document
    Then response is 404

  Scenario: GET /documents/document with existing documents
    Given API is running
    And a valid JWT token for user "John"
    And Database contains documents
    When I get an existing document
    Then response is 200
    And response is the expected document

  Scenario: DELETE /documents/document with existing documents
    Given API is running
    And a valid JWT token for user "John"
    And Database contains documents
    When I delete a non existing document
    Then response is 204
    And document was deleted

  Scenario: DELETE /documents/document with existing documents
    Given API is running
    And a valid JWT token for user "John"
    And Database contains documents
    When I delete a non existing document
    Then response is 404
    And document doesn't exist in bucket