*** Settings ***
Library           RequestsLibrary
Library           DataDriver    file=../data/records.csv    dialect=unix    delimiter=,
Resource          ../resources/swift_keywords.resource
Suite Setup       Create Session    swift_session    http://localhost:5005
Test Template     Process Payment Record Gherkin Style

*** Test Cases ***
Scenario: Process record ${RecordId} for ${Currency}    ${RecordId}    ${Currency}    ${Amount}    ${ExpectedStatus}

*** Keywords ***
Process Payment Record Gherkin Style
    [Arguments]    ${RecordId}    ${Currency}    ${Amount}    ${ExpectedStatus}
    Log    Processing Record: ${RecordId} | Currency: ${Currency} | Amount: ${Amount} | Expected: ${ExpectedStatus}    level=INFO
    Given a SWIFT payment record for ${RecordId} in ${Currency} with amount ${Amount}
    When the record is sent to the mock server
    Then the response should be ${ExpectedStatus}
