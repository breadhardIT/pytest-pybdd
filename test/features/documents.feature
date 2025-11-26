Feature: Document Management

  Scenario: An unauthenticated user can't create a document
    Given API is running
    When I create a document
    Then response is 401

  Scenario: A user with invalid token can't create a document
    Given API is running
    And an invalid JWT token for user John
    When I create a document
    Then response is 401

  Scenario: A valid user can create a document
    Given API is running
    And a valid JWT token for user John
    When I create a document
    Then response is 201

  Scenario: A valid user retrieves an empty list when there are no documents
    Given API is running
    And a valid JWT token for user John
    When I get all documents
    Then response is an empty list

  Scenario: A valid user can get their documents
    Given API is running
    And a valid JWT token for user John
    And documents owned by:
        | John | 5 |
        | Alice | 10 |
        | Bob   | 3  |
    When I get all documents
    Then response is 200
    And response contains only my documents

  Scenario: A valid user retrieves an empty list where he doesn't own documents
    Given API is running
    And a valid JWT token for user John
    And documents owned by:
        | Alice | 1 |
        | Bob   | 1 |
    When I get all documents
    Then response is 200
    And response is an empty list

