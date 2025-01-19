*** Settings ***
Resource    navigation.robot
Library            SeleniumLibrary

Resource            navigation.robot

*** Variables ***
${create_question_button}       id=create_question_nav
${title_text}                   id=id_title
${content_text}                 id=cke_1_contents
${submit_create_question}       id=submit_question

${question_detail_title}        id=question_title
${question_detail_content}      id=question_content
${quesiton_edit_button}         id=question_edit
${quesiton_delete_button}       id=question_delete

${question_upvote_button}       id=question_upvote
${question_downvote_button}     id=question_downvote
${question_score}               id=question_score

${answers_list}                 id=answers_list

${add_answer_button}            id=add_answer
${submit_answer_button}         id=submit_answer
${answer_edit_button}           id=answer_edit
${answer_delete_button}         id=answer_delete


*** Keywords ***
Create Question
    [Arguments]    ${title}    ${content}
    Wait Until And Click Element    ${create_question_button}
    Wait Until And Input Text    ${title_text}    ${title}
    Wait Until And Click Element    ${content_text}
    Press Keys    ${content_text}    ${content}
    Wait Until And Click Button    ${submit_create_question}

    Wait Until Element    ${question_detail_title}
    Wait Until Element    ${question_detail_content}

Create Answer
    [Arguments]    ${content}

    Wait Until And Click Element    ${add_answer_button}
    Wait Until And Click Element    ${content_text}
    Press Keys    ${content_text}    ${content}
    Wait Until And Click Element    ${submit_answer_button}

    Wait Until Element    ${answers_list}
