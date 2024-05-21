from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import chromedriver_autoinstaller
import pathlib
import base64


class Scraper:
    """
    Classe principal. Contém as configurações do Chromedriver e os métodos de acesso
    e controle do Whatsapp Web
    """
    
    def __init__(self) -> None:
        """
        Construtor que inicializa o chromedriver e seta o driver para o Whatsapp Web
        """
        
        chromedriver_autoinstaller.install()

        options = Options()
        options.add_argument('--headful')
        options.add_argument(f'user-data-dir={pathlib.Path().absolute()}\\userdata')
        options.add_experimental_option('detach', True)

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get('https://web.whatsapp.com')
        
        
    def authenticateWithQRCode(self):
        """
        método responsável por gerenciar a autenticação via QRCode

        O método entrará em um loop que constantemente vai checar pela presença e pela
        atualização do QRCode de autenticação do Whatsapp. Sempre que o QR for criado ou
        atualizado, ele será escrito em um arquivo 'canvas.png' na raíz do projeto.
        Após a autenticação, a função retorna com um código de retorno\n
        Retorno:
            Int: o código de retorno.
            0 significa sucesso na autenticação, enquanto
            -1 significa um erro
        """
        
        c_base64 = None     # inicializa um base64 vazio
                    
        while True:
            print('\nchecando QRCode...')
            
            login = self.wait.until(ec.any_of(
                ec.visibility_of_element_located((By.TAG_NAME, 'canvas')),
                ec.visibility_of_element_located((By.CLASS_NAME, '_aly_'))
            ))
            
            if login.tag_name == 'canvas':
                new_c_base64 = self.driver.execute_script('return arguments[0].toDataURL("image.png").substring(21);', login)
                
                if new_c_base64 != c_base64:
                    print('QRCodes diferentes, atualizando...')
                    
                    c_base64 = new_c_base64
                    c_png = base64.b64decode(c_base64)
                    
                    with open(r'canvas.png', 'wb') as f:
                        f.write(c_png)
                else:
                    print('QRCodes ainda sao iguais')
            elif login.tag_name == 'div':
                print('Logado com sucesso')
                return
                
            sleep(3)
            
            
    def coletarEtiquetas(self) -> set:
        """** MÉTODO EM DESENVOLVIMENTO **
        Irá coletar as etiquetas do usuário e retornar em um set

        Returns:
            set: set contendo strings das etiquetas do usuário
        """

        botao = self.wait.until(ec.visibility_of_element_located(
            (By.XPATH, '//button[contains(@aria-label, "Menu de filtros de conversas")]')))
        botao.click()

        etiqueta = self.wait.until(ec.visibility_of_element_located((By.XPATH, f'//span[text()="{etiqueta}"]')))
        return etiqueta
    
    
    def coletarContatos(self, qtdContatos: int) -> set:
        """
        **DOCUMENTACAO EM ANDAMENTO**\n
        A função irá coletar e formar um set com n contatos, sendo n >= qtdContatos

        Args:
            qtdContatos (Int): quantidade minima de contatos a ser coletada
        
        Returns:
            contatos (set): uma coleção com nomes únicos de contatos
        """
        
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
