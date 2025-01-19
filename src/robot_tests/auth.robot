*** Settings ***
Resource    navigation.robot


*** Variables ***
${login_url}            http://127.0.0.1:8000/accounts/login/
${logout_url}           http://127.0.0.1:8000/accounts/logout/

${username_field}       id=id_username
${password_field}       id=id_password

${username}         admin
${password}         admin


*** Keywords ***
Open Chrome
    ${firefox_options}=    Evaluate    sys.modules['selenium.webdriver'].FirefoxOptions()    sys, selenium.webdriver
    Call Method    ${firefox_options}    add_argument    --headless
    Open Browser    ${login_url}    Firefox    options=${firefox_options}
    Set Window Size    1920    1080


Login
    Go To    ${login_url}

    Wait Until And Input Text    ${username_field}    ${username}
    Wait Until And Input Text    ${password_field}    ${password}

    Submit Form

    Wait Until Location Is Not    ${login_url}
    Wait Until Loading Is Complete

Logout
    Go To    ${logout_url}

Open Browser And Login
    Open Chrome
    Login