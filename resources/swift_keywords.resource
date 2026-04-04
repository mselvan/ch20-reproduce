*** Settings ***
Library    RequestsLibrary
Library    OperatingSystem
Library    XML
Library    xml_builder.py

*** Keywords ***
Start SWIFT Mock Server
    [Arguments]    ${host}=http://localhost:5005
    Log    Waiting for mock server at ${host} to be ready...    level=INFO
    Wait For Mock Server    ${host}
    Create Session    swift_session    ${host}

Wait For Mock Server
    [Arguments]    ${host}
    Wait Until Keyword Succeeds    30s    2s    Get Health Status    ${host}

Get Health Status
    [Arguments]    ${host}
    ${response} =    GET    ${host}/health    expected_status=200
    Should Be Equal As Strings    ${response.text}    READY
Process Payment Record
    [Arguments]    ${record_id}    ${currency}    ${amount}    ${expected_status}
    Log    Processing Record: ${record_id} | Currency: ${currency} | Amount: ${amount} | Expected: ${expected_status}    level=INFO
    Given a SWIFT payment record exists for ${record_id}
    When I submit the payment for ${currency} with amount ${amount}
    Then the transaction should be ${expected_status}

Given a SWIFT payment record exists for ${record_id}
    # Mocking record context
    Set Test Variable    ${RECORD_ID}    ${record_id}
    Log    Setting up context for record ${record_id}    level=DEBUG

When I submit the payment for ${currency} with amount ${amount}
    ${xml_content} =    Build Swift Xml    ${RECORD_ID}    ${currency}    ${amount}
    Set Test Variable    ${CURRENT_XML}    ${xml_content}
    
    Log    Generated SWIFT XML (pain.001):\n${xml_content}    level=DEBUG
    Log    Sending POST request to mock server /upload    level=INFO
    
    ${response} =    POST On Session    swift_session    /upload    data=${xml_content}    expected_status=any
    Set Test Variable    ${LATEST_RESPONSE}    ${response}
    Log    Server Response: ${response.status_code} - ${response.text}    level=INFO

Then the transaction should be ${expected_status}
    Log    Verifying transaction status in SWIFT XML response (pain.002)    level=INFO
    
    # Use professional Python parser from xml_builder library
    ${result} =    Parse Pain002 Response    ${LATEST_RESPONSE.text}
    
    ${txn_sts} =    Set Variable    ${result['status']}
    ${reason_code} =    Set Variable    ${result['reason']}

    IF    '${expected_status}' == 'ACCEPTED'
        Should Be Equal As Integers    ${LATEST_RESPONSE.status_code}    200
        Should Be Equal As Strings    ${txn_sts}    ACTC
        Log    Payment successfully ACCEPTED (Status: ACTC).    level=INFO
    ELSE IF    '${expected_status}' == 'REJECTED'
        Should Be Equal As Integers    ${LATEST_RESPONSE.status_code}    400
        Should Be Equal As Strings    ${txn_sts}    RJCT
        Should Be Equal As Strings    ${reason_code}    CH20
        Log    Payment correctly REJECTED with CH20 error (Status: RJCT).    level=INFO
    END
