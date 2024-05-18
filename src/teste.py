from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import chromedriver_autoinstaller
import pathlib

chromedriver_autoinstaller.install()

options = Options()
options.add_argument('--headful')
options.add_argument(f'user-data-dir={pathlib.Path().absolute()}\\userdata')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get('https://web.whatsapp.com')

botao = wait.until(ec.visibility_of_element_located(
    (By.XPATH, '//button[contains(@aria-label, "Menu de filtros de conversas")]'))
)
botao.click()

etiqueta = wait.until(ec.visibility_of_element_located((By.XPATH, '//span[text()="Novo cliente"]')))
