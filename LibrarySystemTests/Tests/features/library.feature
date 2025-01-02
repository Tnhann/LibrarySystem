Feature: Library Management System Tests

  Scenario: Login to the system
    Given I am on the login page
    When I enter username "admin" and password "admin123"
    Then I should be logged in successfully

  Scenario: Search for a book
    Given I am logged in
    When I search for book "1984"
    And I select category "Roman"
    And I select availability "Mevcut"
    Then I should see the book in results

  Scenario: Loan a book
    Given I am logged in
    And I am on the loan page
    When I select a book to loan
    And I set the due date
    Then the book should be marked as loaned 