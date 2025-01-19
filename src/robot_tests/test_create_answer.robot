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
Test Answer Creation
    Create Question    q_with_answer    q_with_answer
    Create Answer    answer_content

    Page Should Contain    answer_content
    Page Should Contain Element    ${answer_edit_button}
    Page Should Contain Element    ${answer_delete_button}
