from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    # Função de inicialização da classe
    def __init__(self, driver):
        self.driver = driver

    # Funçãoi para abrir uma página
    def _visitar(self, url):
        self.driver.get(url)

    # Função genérica para localização e elemento
    def _procurar(self, locator):
        return self.driver.find_element(locator['by'], locator['value'])

    # Função para clicar em um elemento pelo localizador
    def _clicar(self, locator):
        self._procurar(locator).click()

    # Função para digitar em um elemento
    def _digitar(self, locator, input_text):
        self._procurar(locator).send_keys(input_text)

    # Função para ler o texto de um elemento
    def _ler(self, locator):
        self._procurar(locator).text()

    # Função para verificar se o elemento está visivel
    def _esta_visivel(self, locator, timeout=0):
        # Se precisa esperar
        if timeout > 0:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    expected_conditions.visibility_of_element_located(
                        (locator['by'], locator['value'])
                    )
                )
            # Esgotou o tempo de espera
            except TimeoutException:
                return False  # Não encontrou o elemento
            return True  # Encontrou o elemento
        # Se não precisa esperar
        else:
            try:
                return self._procurar(locator).is_displayed()
            except NoSuchElementException:
                return False  # Não encontrou o elemento
            # return True
