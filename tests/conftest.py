import os

import pytest
from selenium import webdriver

from . import config, credentials


def pytest_addoption(parser):
    parser.addoption('--baseurl',
                     action='store',
                     default='https://the-internet.herokuapp.com',
                     help='endereço do site alvo do teste'

                     )
    parser.addoption('--host',
                     action='store',
                     default='saucelabs',
                     help='ambiente em que vou executar os testes'

                     )
    parser.addoption('--browser',
                     action='store',
                     default='chrome',
                     help='Navegador padrão'

                     )
    parser.addoption('--browserversion',
                     action='store',
                     default='97.0',
                     help='versão do navegador'

                     )
    parser.addoption('--platform',
                     action='store',
                     default='Windows 10',
                     help='Sistema Operacional'
                     )


@pytest.fixture
def driver(request):
    config.baseurl = request.config.getoption('--baseurl')
    config.host = request.config.getoption('--host')
    config.browser = request.config.getoption('--browser')
    config.browserversion = request.config.getoption('--browserversion')
    config.platform = request.config.getoption('--platform')
    # Configuração pra rodar no sauceLabs
    if config.host == 'saucelabs':
        test_name = request.node.name  # Adicionar o nome do teste baseado no script
        capabilities = {
            'browserName': config.browser,
            'browserVersion': config.browserversion,
            'platformName': config.platform,
            'sauce:options': {
                'name': test_name  # Nome do teste conforme acima
            }
        }
        # credenciais
        _credentials = credentials.SAUCE_USERNAME + ':' + credentials.SAUCE_ACCESS_KEY
        _url = 'https://' + _credentials + '@ondemand.us-west-1.saucelabs.com:443/wd/hub'
        # Chamada para o SauceLabs
        driver_ = webdriver.Remote(_url, capabilities)
    else:  # Configuração para execução local
        if config.browser == 'chrome':
            _chromedriver = os.path.join(os.getcwd(), 'vendor', 'chromedriver.exe')
            if os.path.isfile(_chromedriver):
                driver_ = webdriver.Chrome(_chromedriver)
            else:
                driver_ = webdriver.Chrome()  # Vai usar o chrome driver apontado nas variaveis de ambiente
        elif config.browser == 'firefox':
            _geckodriver = os.path.join(os.getcwd(), 'vendor', 'geckodriver.exe')
            if os.path.isfile(_geckodriver):
                driver_ = webdriver.Firefox(_geckodriver)
            else:
                driver_ = webdriver.Firefox()

    def quit():  # sub-função para finallizar o objeto do Selenium
        # Atualização do status de passou ou falhou
        sauce_result = 'failed' if request.node.rep_call.failed else 'passed'
        driver_.execute_script('sauce:job-result={}'.format(sauce_result))
        driver_.quit()

    request.addfinalizer(quit)
    return driver_


# Configurar o gtilho para a geração do relatório
@pytest.hookimpl(hookwrapper=True, tryfirst=True)  # ativa o gatilho na iniciaçização da requisição
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()  # Variavel de relatório que irá guardar o resultado

    # Atributos do relatorio
    setattr(item, 'rep_' + report.when, report)
