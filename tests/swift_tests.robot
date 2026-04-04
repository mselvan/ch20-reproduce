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
    [Documentation]    Starts the mock server process and waits for readiness.
    ${server_proc} =    Start Process    python3    scripts/mock_server.py    cwd=${CURDIR}/..
    Set Suite Variable    ${SERVER_PROC}    ${server_proc}
    # Wait for the server to be ready and initialize the session
    Start SWIFT Mock Server    http://localhost:5005

Stop Test Environment
    [Documentation]    Gracefully terminates the mock server process.
    Log    Stopping mock server process...    level=INFO
    Terminate Process    ${SERVER_PROC}
