Feature: User service integration test
  Scenario: Register a new user
    Given Flask app is running
    When We save a user
    Then We find the user

  Scenario: Update user
    Given Flask app is running
    And We have an user
    When We update the user
    Then The user is updated

  Scenario: Login user
    Given Flask app is running
    When Submit login data
    Then User is logged in