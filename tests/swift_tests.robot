*** Settings ***
Documentation     SWIFT CH20 Error Reproduction Suite
Library           RequestsLibrary
Library           Process
Library           DataDriver    file=../data/records.csv    dialect=unix    delimiter=,
Resource          ../resources/swift_keywords.resource
Suite Setup       Start Test Environment
Suite Teardown    Stop Test Environment
Test Template     Process Payment Record

*** Test Cases ***
Scenario for Record ${record_id}    Default    Default    Default    Default

*** Keywords ***
Start Test Environment
    [Documentation]    Starts the mock server and waits for readiness.
    # Start the mock server
    ${server_proc} =    Start Process    python3    scripts/mock_server.py    cwd=${CURDIR}/..
    Set Suite Variable    ${SERVER_PROC}    ${server_proc}
    
    # Wait for the server to be ready and initialize the session
    Start SWIFT Mock Server    http://localhost:5005

Stop Test Environment
    [Documentation]    Gracefully terminates the mock server process.
    Log    Stopping mock server process...    level=INFO
    Terminate Process    ${SERVER_PROC}

Process Payment Record
    [Arguments]    ${record_id}    ${currency}    ${amount}    ${expected_status}
    Log    Processing Record: ${record_id} | Currency: ${currency} | Amount: ${amount} | Expected: ${expected_status}    level=INFO
    Given a SWIFT payment record exists for ${record_id}
    When I submit the payment for ${currency} with amount ${amount}
    Then the transaction should be ${expected_status}
