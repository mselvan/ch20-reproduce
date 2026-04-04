*** Settings ***
Library    RequestsLibrary
Library    OperatingSystem
Library    xml_builder.py

*** Keywords ***


Given a SWIFT payment record for ${RecordId} in ${Currency} with amount ${Amount}
    ${xml_content} =    Build Swift Xml    ${RecordId}    ${Currency}    ${Amount}
    Set Test Variable    ${CURRENT_XML}    ${xml_content}
    Log    Generated SWIFT XML:\n${xml_content}    level=DEBUG

When the record is sent to the mock server
    Log    Sending POST request to mock server /upload    level=INFO
    ${response} =    POST On Session    swift_session    /upload    data=${CURRENT_XML}    expected_status=any
    Set Test Variable    ${LATEST_RESPONSE}    ${response}
    Log    Server Response: ${response.status_code} - ${response.text}    level=INFO

Then the response should be ${ExpectedStatus}
    Log    Verifying response status matches expected: ${ExpectedStatus}    level=INFO
    IF    '${ExpectedStatus}' == 'ACCEPTED'
        Should Be Equal As Integers    ${LATEST_RESPONSE.status_code}    200
        ${json} =    Set Variable    ${LATEST_RESPONSE.json()}
        Should Be Equal As Strings    ${json['status']}    ACCEPTED
        Log    Payment successfully ACCEPTED.    level=INFO
    ELSE IF    '${ExpectedStatus}' == 'REJECTED'
        Should Be Equal As Integers    ${LATEST_RESPONSE.status_code}    400
        ${json} =    Set Variable    ${LATEST_RESPONSE.json()}
        Should Be Equal As Strings    ${json['status']}    REJECTED
        Should Be Equal As Strings    ${json['error_code']}    CH20
        Log    Payment correctly REJECTED with CH20 error.    level=INFO
    END
