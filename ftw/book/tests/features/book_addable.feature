Feature: Add a book.
  In order create and print a book
  As an editor
  I need to be able to create a book object.

  Scenario: Create a new book
    Given I am logged in as "hugo.boss"
    And I am on the site root
    When I click on "Add..."
    Then I see "Book"
