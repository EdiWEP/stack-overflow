*** Settings ***
Resource            auth.robot
Resource            setup.robot
Resource            navigation.robot
Resource            questions.robot

Suite Setup         Register Keyword To Run On Failure    Log Source And Capture Screenshot
Suite Teardown      Close All Browsers
Test Setup          Open Browser And Login
Test Teardown       Logout




*** Test Cases ***
Test Question Creation
    Create Question    test    test

    Element Should Contain    ${question_detail_title}    test
    Element Should Contain    ${question_detail_content}    test
    Page Should Contain Element    ${quesiton_edit_button}
    Page Should Contain Element    ${quesiton_delete_button}
