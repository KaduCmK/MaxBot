from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import chromedriver_autoinstaller
import pathlib


class Scraper:
    def __init__(self) -> None:
        chromedriver_autoinstaller.install()

        options = Options()
        options.add_argument('--headful')
        options.add_argument(f'user-data-dir={pathlib.Path().absolute()}\\..\\userdata')
        options.add_experimental_option('detach', True)

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def coletarContatos(self, qtdContatos):
        contatos = set()
        scroll = 600
        while len(contatos) < qtdContatos:
            atual = self.driver.find_elements(By.CLASS_NAME, "_ak8q")
            contatos.update(div.text for div in atual)
            print(f'{len(contatos)} contatos...')
            print(">>>>>>>>>>>>>>> SCROLLING\n")

            painel = self.wait.until(ec.visibility_of_element_located((By.ID, "pane-side")))
            self.driver.execute_script(f'arguments[0].scrollTop = {scroll}', painel)
            scroll += 600
            sleep(1)

        scroll = 0
        print(f'{len(contatos)} contatos coletados')
        print(contatos)

        return contatos

    def coletarEtiquetas(self, etiqueta):
        self.driver.get('https://web.whatsapp.com')

        botao = self.wait.until(ec.visibility_of_element_located(
            (By.XPATH, '//button[contains(@aria-label, "Menu de filtros de conversas")]')))
        botao.click()

        etiqueta = self.wait.until(ec.visibility_of_element_located((By.XPATH, f'//span[text()="{etiqueta}"]')))
        return etiqueta
