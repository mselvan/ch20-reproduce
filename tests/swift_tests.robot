*** Settings ***
Documentation     SWIFT CH20 Error Reproduction Suite
Library           RequestsLibrary
Library           DataDriver    file=../data/records.csv    dialect=unix    delimiter=,
Resource          ../resources/swift_keywords.resource
Suite Setup       Create Session    swift_session    http://localhost:5005

*** Test Cases ***
Process SWIFT Transaction for Record ${record_id}
    [Template]    Process Payment Record
    ${record_id}    ${currency}    ${amount}    ${expected_status}

*** Keywords ***
Process Payment Record
    [Arguments]    ${record_id}    ${currency}    ${amount}    ${expected_status}
    Log    Processing Record: ${record_id} | Currency: ${currency} | Amount: ${amount} | Expected: ${expected_status}    level=INFO
    Given a SWIFT payment record exists for ${record_id}
    When I submit the payment for ${currency} with amount ${amount}
    Then the transaction should be ${expected_status}
