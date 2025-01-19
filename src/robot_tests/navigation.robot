*** Settings ***
Library             SeleniumLibrary


*** Keywords ***
Wait Until Element
    [Arguments]    ${element}

    Wait Until Page Contains Element     ${element}
    Wait Until Element Is Visible        ${element}
    Wait Until Element Is Enabled        ${element}

Wait Until And Click Element
    [Arguments]    ${element}

    Wait Until Element                   ${element}
    Click Element                        ${element}

Wait Until And Click Button
    [Arguments]    ${button}

    Wait Until Element                   ${button}
    Click Button                         ${button}

Wait Until And Input Text
    [Arguments]    ${element}    ${text}

    Clear Element Text                   ${element}
    Wait Until Element                   ${element}
    Input Text                           ${element}    ${text}

Wait Until Loading Is Complete
    Wait For Condition    return document.readyState == "complete"

Wait Until And Mouse Over
    [Arguments]    ${element}

    Wait Until Element    ${element}
    Mouse Over            ${element}