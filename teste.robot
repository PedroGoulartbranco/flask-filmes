*** Settings ***
Library    SeleniumLibrary
Library    String

*** Variables ***
${URL}        http://127.0.0.1:5000
${BROWSER}    Chrome

*** Test Cases ***
Cadastro e Uso da IA
    [Documentation]    Testa o fluxo completo do Mooflix
    Abrir o Site
    Fazer Cadastro
    Verificar se Entrou no Dashboard
    Pedir Recomendacao Musical
    [Teardown]    Close Browser

*** Keywords ***
Abrir o Site
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.5 seconds

Fazer Cadastro
    # Gera string aleatória para o email
    ${RANDOM_STRING}=    Generate Random String    5    [LOWER]
    ${EMAIL_TESTE}=      Set Variable    robo_${RANDOM_STRING}@teste.com
    
    # Preenche os campos
    Input Text      name=nome     Robo Framework
    Input Text      name=email    ${EMAIL_TESTE}
    Input Text      name=senha    123456
    Click Button    xpath=//button

Verificar se Entrou no Dashboard
    Wait Until Location Contains    dashboard    timeout=5s
    Page Should Contain    O que você quer ouvir hoje?

Pedir Recomendacao Musical
    Input Text      name=gosto_usuario    Rock clássico
    Click Button    xpath=//button
    Wait Until Page Contains    Sua Recomendação    timeout=10s
    Page Should Contain    -