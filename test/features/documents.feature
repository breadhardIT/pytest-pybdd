Feature: Document Management

  Scenario: GET documents without documents
    Given API is running
    When I get all documents
    Then response is 200
    And response is an empty list

  Scenario: GET documents with documents
    Given API is running
    And Database contains documents
    When I get all documents
    Then response is 200
    And response contains a list of documents

  Scenario: GET /documents/document with non existing documents
    Given API is running
    And Database contains documents
    When I get a non existing document
    Then response is 404

  Scenario: GET /documents/document with existing documents
    Given API is running
    And Database contains documents
    When I get an existing document
    Then response is 200
    And response is the expected document