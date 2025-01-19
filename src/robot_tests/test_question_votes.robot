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
Test Question Upvote
    Create Question    q_with_upvote    q_with_upvote

    Wait Until And Click Element    ${question_upvote_button}

    Element Should Contain    ${question_score}    1

Test Question Downvote
    Create Question    q_with_downvote    q_with_downvote

    Wait Until And Click Element    ${question_downvote_button}

    Element Should Contain    ${question_score}    -1

Test Question Upvote Then Downvote
    Create Question    q_with_up_then_downvote    q_with_up_then_downvote

    Wait Until And Click Element    ${question_upvote_button}
    Wait Until And Click Element    ${question_downvote_button}

    Element Should Contain    ${question_score}    -1
