import base64
import os
import pathlib
from time import sleep

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from Status import Status


class Scraper:
    """
    Classe principal. Contém as configurações do Chromedriver e os métodos de acesso
    e controle do Whatsapp Web
    """

    def __init__(self, status: int) -> None:
        """
        Construtor que inicializa o chromedriver e seta o driver para o Whatsapp Web
        """

        chromedriver_autoinstaller.install()

        options = Options()
        options.add_argument('--headful')
        options.add_argument(f'user-data-dir={os.path.join(pathlib.Path().absolute(), "userdata")}')
        # options.add_experimental_option('detach', True)

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get('https://web.whatsapp.com')

        status = 0

    def authenticateWithQRCode(self, status) -> int:
        """
        Método responsável por gerenciar a autenticação via QRCode

        O método entrará em um loop que constantemente vai checar pela presença e pela
        atualização do QRCode de autenticação do Whatsapp. Sempre que o QR for criado ou
        atualizado, ele será escrito em um arquivo 'canvas.png' na raíz do projeto.
        Após a autenticação, a função retorna com um código de retorno\n
        :return: o código de retorno.
            0 significa sucesso na autenticação, enquanto
            -1 significa um erro
        """

        self.statusString = Status.CARREGANDO_QR
        status = 1

        c_base64 = None  # inicializa um base64 vazio

        while True:
            print('\nchecando QRCode...')

            login = self.wait.until(ec.any_of(
                ec.visibility_of_element_located((By.TAG_NAME, 'canvas')),
                ec.visibility_of_element_located((By.CLASS_NAME, '_aly_'))
            ))

            if login.tag_name == 'canvas':
                self.statusString = Status.AGUARDANDO_AUTENTICACAO
                status = 2

                new_c_base64 = self.driver.execute_script('return arguments[0].toDataURL("image.png").substring(21);',
                                                          login)

                if new_c_base64 != c_base64:
                    print('QRCodes diferentes, atualizando...')

                    c_base64 = new_c_base64
                    c_png = base64.b64decode(c_base64)

                    with open(r'res/canvas.png', 'wb') as f:
                        f.write(c_png)
                else:
                    print('QRCodes ainda sao iguais')
            elif login.tag_name == 'div':
                self.statusString = Status.IDLE
                print('Logado com sucesso')
                return 0

            sleep(3)

    def coletarEtiquetas(self) -> set[str]:
        """**MÉTODO EM DESENVOLVIMENTO**\n
        Irá coletar as etiquetas do usuário e retornar em um set

        :return: set contendo as etiquetas do usuário
        """

        print('Coletando etiquetas...')
        self.statusString = Status.COLETANDO_ETIQUETAS

        # botao = self.wait.until(ec.visibility_of_element_located(
        #     (By.XPATH, '//button[contains(@aria-label, "Menu de filtros de conversas")]')))
        # botao.click()

        # TODO: coleta de etiquetas
        etiqueta = self.wait.until(ec.visibility_of_element_located((By.XPATH, f'//span[text()="{etiqueta}"]')))
        etiquetas = self.driver.find_elements(By.CLASS_NAME, "x9f619 x193iq5w x1y1aw1k xqmdsaz xwib8y2 xbbxn1n x6ikm8r x10wlt62")
        print(etiquetas)

        self.statusString = Status.IDLE

        # return set(["etiqueta1", "etiqueta2", "etiqueta3"])
        return etiquetas

    def coletarContatos(self, qtdContatos: int) -> set[str]:
        """
        **DOCUMENTAÇÃO EM ANDAMENTO**\n
        Método responsável por coletar n contatos, sendo n >= qtdContatos


        :param qtdContatos: quantidade minima de contatos a ser coletada
        :return: um set com os nomes dos contatos coletados
        """

        self.statusString = Status.COLETANDO_CONTATOS

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

        contatos.discard('Arquivadas')
        print(f'{len(contatos)} contatos válidos coletados: \n{contatos}')
        sleep(3)

        self.statusString = Status.IDLE

        return contatos

    def enviarMensagem(self, contatos: set[str], msg: str) -> set[str]:
        """
        Método responsável por enviar a mensagem template para o set de contatos fornecidos.

        Cada contato será vasculhado até uma distância de rolagem predefinida.
        - Caso seja encontrado, a mensagem é enviada.
        - Caso contrário, o nome do contato é adicionado a um set de erros

        :param contatos: A lista de contatos que devem receber a mensagem
        :param msg: O template de mensagem que será enviado
        :return: um set contendo os possíveis contatos para os quais não foi possível enviar a mensagem
        """
        # TODO: ideia -> template strings

        self.statusString = Status.ENVIANDO_MENSAGENS

        painel = self.wait.until(ec.visibility_of_element_located((By.ID, "pane-side")))

        erros = set()
        for contato in contatos:
            print(f'Clicando em {contato}...')
            scroll = 0
            retries = 5
            visible = False

            while not visible:
                if retries == 0:
                    print(f'{contato} não encontrado')
                    erros.add(contato)
                    break
                else:
                    try:
                        clickable = self.driver.find_element(By.XPATH, f'//span[contains(@title, "{contato}")]')
                        clickable.click()
                        visible = True
                        print(f'{contato} encontrado')
                        
                        # pesquisar contato e escrever mensagem usam as mesmas classes, por isso retornar lista
                        input = self.driver.find_elements(
                            By.CSS_SELECTOR, 'p.selectable-text.copyable-text.x15bjb6t.x1n2onr6'
                            )[1]
                        input.send_keys(msg)
                        # input.send_keys(Keys.ENTER)
                    except:
                        print('Rolando...')
                        self.driver.execute_script(f'arguments[0].scrollTop = {scroll}', painel)
                        retries -= 1
                        scroll += 600
                    finally:
                        sleep(2)

        self.statusString = Status.IDLE

        return erros


    def getScraperStatus(self) -> int:
        """
        **DOCUMENTACAO E IMPLEMENTAÇÃO EM ANDAMENTO\n**
        Retorna o estado atual do Scraper, definido entre um dos estados possiveis em Status.py

        :return: o código de estado do Scraper
        """

        return self.statusString
