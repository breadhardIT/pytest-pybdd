Feature: As user I wan't to manage documents

  Scenario: A user gets an empty list when there are no documents
    Given API is running
    When I get all documents
    Then response is 200
    And response is an empty list

  Scenario: A user get the list of documents where are documents
    Given API is running
    And Database contains documents
    When I get all documents
    Then response is 200
    And response contains a list of documents

  Scenario: A user gets not found when get a non existing document
    Given API is running
    And Database contains documents
    When I get a non existing document
    Then response is 404

  Scenario: A user get the expected document when get an existing document
    Given API is running
    And Database contains documents
    When I get an existing document
    Then response is 200
    And response is the expected document

  Scenario: A user can delete an existing document
    Given API is running
    And Database contains documents
    When I delete an existing document
    Then response is 204
    And document was deleted
    And document doesn't exist in bucket

  Scenario: A user get not found when delete a non existing document
    Given API is running
    And Database contains documents
    When I delete a non existing document
    Then response is 404
