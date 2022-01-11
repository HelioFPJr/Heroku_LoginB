import pytest

from . import config


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
    if config.host == 'saucelabs':
        test_name = request.node.name  # Adicionar o nome do teste baseado no script
        capabilities = {
            'browserName': config.browser,
            'browserVersion': config.browserversion,
            'platformName': config.platform,
            'sauce.options': {
                'name': test_name,  # Nome do teste conforme acima
            }
        }
