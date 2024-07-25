import threading
from kivy.clock import Clock

from Status import Status as sts
from Scraper import Scraper
from kivy.app import App
from kivy.clock import mainthread
from kivy.loader import Loader
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from functools import partial

class MaxBot(App):
    """
    **Classe Principal\n**

    Instancia a árvore de widgets do aplicativo
    """
    selected = "Nenhuma"
    tags = set()
    contacts = set[str]

    def __init__(self, **kwargs):
        self.backend = Backend(self)
        super().__init__(**kwargs)
    
    def build(self):
        """
        Construtor da árvore de widgets do aplicativo

        :return: raíz da árvore de widgets
        """

        self.textbox = TextBox()
        self.progress = ProgressInfo(self)

        screen = BoxLayout(orientation='vertical', padding=10, spacing=10)

        upper = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        upper.add_widget(self.textbox)
        upper.add_widget(TagMenu(self))

        screen.add_widget(upper)
        screen.add_widget(self.progress)

        # window = AnchorLayout(anchor_x='center', anchor_y='center')
        # window = ModalView(background='background_image.png')
        window = ModalView()
        window.add_widget(screen)

        return window
    

class TextBox(BoxLayout):
    """
    Classe criadora do campo de mensagem
    """

    # variével q guarda a mensagem atual
    message = "Mensagem... "
    
    def __init__(self, **kwargs):
        super(TextBox, self).__init__(orientation='vertical', spacing=10, **kwargs)
        self.build()

    def build(self):
        '''
        Construtor da classe TextBox
        '''

        scroll_box = ScrollView(size_hint=(1, 1))
        scroll_box.bind(size=self.update_rect, pos=self.update_rect)

        with scroll_box.canvas.before:
            Color(1,1,1,1)
            self.rectangle = Rectangle(size=scroll_box.size, pos=scroll_box.pos)

        self.text_display = Label(
            text=self.message, 
            size_hint=(1, None),
            color=(0,0,0,1),
            valign='top'
        )
        self.text_display.bind(texture_size=self.update_height)

        button = Button(
            text="Editar mensagem", 
            size_hint=(None, None), 
            width=200, 
            height=44, 
            pos_hint={'center_x': 0.5}
        )
        button.bind(on_release=self.call_editor)

        scroll_box.add_widget(self.text_display)
        self.add_widget(scroll_box)
        self.add_widget(button)

    def update_height(self, instance, value):
        instance.height = instance.texture_size[1]

    def update_rect(self, instance: ScrollView, value):
        self.rectangle.size = instance.size
        self.rectangle.pos = instance.pos
        self.text_display.text_size = (instance.size[0] - 10, None)

    def call_editor(self, instance):
        edit_text(self)

    def update(self, input_text):
        self.message = input_text
        self.text_display.text = self.message


class TagMenu(StackLayout):
    """
    Classe criadora do menu de etiquetas
    """
    root: MaxBot

    def __init__(self, root, **kwargs):
        super(TagMenu, self).__init__(orientation='tb-lr', size_hint=(0.3,1))
        self.root = root
        self.build()

    def build(self):
        '''
        Construtor da classe TagMenu
        '''

        self.updater = Button(
            text='Atualizar etiquetas',
            size_hint=(1,None),
            size=(200,44),
            pos_hint={'top': 1, 'center_x': .5}
        )
        self.updater.bind(on_release=partial(self.backendGetTags, self.updateTags))

        self.menu = Spinner(
            text="Etiquetas",
            values=set([""]),
            size_hint=(1,None),
            size=(200, 44),
            pos_hint={'top': .9}
        )
        self.menu.bind(text=self.select)

        self.add_widget(self.updater)
        self.add_widget(self.menu)

    def backendGetTags(self, callback, *args):
        threading.Thread(target=self.root.backend.get_tags, args=(callback,)).start()

    @mainthread
    def updateTags(self, tags: set[str]):
        self.menu.values = tags
        
    def select(self, instance, value):
        self.root.selected=value
        print(self.root.selected)


class ProgressInfo(BoxLayout):
    """
    Classe criadora da área de progresso e botão de enviar
    """

    max = 1
    current = 0
    current_status = StringProperty("Iniciando")
    root: App

    def __init__(self, root, **kwargs):
        super(ProgressInfo, self).__init__(orientation='vertical', padding=10, spacing=10, size_hint=(1,0.4), **kwargs)
        self.root = root
        self.build()

    def build(self):
        '''
        Construtor da classe ProgressInfo
        '''

        self.status = Label(
            text=self.current_status,
            font_size=30,
            size_hint=(1, None),
            halign='center',
            pos_hint={'bottom': 0.1}
        )

        progress = ProgressBar(
            max=self.max,
            value=self.current
        )

        enviar = Button(
            text="Enviar",
            size_hint=(None,None),
            size=(100,44),
            pos_hint={'center_x': .5}
        )
        enviar.bind(on_release=partial(self.sendMessenge, self.updateStatus))

        self.add_widget(self.status)
        self.add_widget(progress)
        self.add_widget(enviar)


    def cont(self, callback, *args):
        self.updater = Clock.schedule_interval(self.updateStatusBar, 0.5)
        self.status.text="Coletando"
        threading.Thread(target=self.root.backend.get_contacts, args=(callback,)).start()

    def sendMessenge(self, callback, *args):
        threading.Thread(target=self.root.backend.filter_tag, args=(callback, )).start()

    def updateStatus(self, text):
        self.status.text = text

    def updateStatusBar(self, dt):
        if self.current == self.max:
            self.updater.cancel()


class Backend():
    root: MaxBot
    status: int

    def __init__(self, root):
        self.root = root
        self.status = 0
        threading.Thread(target=self.call_scraper).start()

    def authenticate(self):
        if self.sc.statusString == 0:
            print('Coisaaaaaaaaaaaaaaaaaaa!')
            AuthenticationScreen(self.sc)

    def call_scraper(self):
        self.sc = Scraper(self.status)
        # AuthenticationScreen(self.sc, self)
        testing(self.sc, self)
        self.sc.authenticateWithQRCode(self.status)

    def filter_tag(self, callback):
        callback("Filtrando Etiqueta")
        tag = self.root.selected
        
        if self.sc.selecionarEtiqueta(tag):
            callback("Etiquetas Selecionadas")
            self.get_contacts(callback)
            self.send_messenge(callback)

        else:
            callback("Falha ao Selecionar Etiquetas")

    def get_contacts(self, callback):
        callback("Coletando Contatos")
        contacts = self.sc.coletarContatos(1)
        number_contacts = len(contacts)
        callback(f"{number_contacts} contatos encontrados")
        self.root.contacts = contacts
    
    def get_tags(self, callback):
        callback(self.sc.coletarEtiquetas())

    def send_messenge(self, callback):
        callback("Enviando Mensagens")
        self.sc.enviarMensagem(self.root.contacts, self.root.textbox.message) 


class AuthenticationScreen():
    @mainthread
    def __init__(self, scraper: Scraper, parent):
        self.scraper = scraper
        self.build(parent)
   
    def build(self, parent: Backend):
        self.qrcode = Image(source='res/canvas.png')
        self.message = Label(text="Coisa", size_hint=(1,None), height=50)

        def check_authenticated(instance):
            if self.scraper.statusString == 0:
                self.authenticator.dismiss()

            else:
                self.message.text = "Não Autenticado"

        def test(instance):
            print("O status é ", parent.status)
            if parent.status == 0:
                self.authenticator.dismiss()

            else:
                self.message.text = "Não autenticado!"

        def update_image(self, parent):
            parent.message.text = "Clicou!"

        self.button = Button(text='Close', size_hint=(1,None), height=50)
        # button.bind(on_release=test)
        self.button.bind(on_release=self.update_image)

        self.content = BoxLayout(orientation='vertical')
        self.content.add_widget(self.qrcode)
        self.content.add_widget(self.message)
        self.content.add_widget(self.button)

        self.authenticator = Popup(title='Authenticator', content=self.content, size_hint=(None,None), size=(400,500), auto_dismiss=False)
        self.authenticator.open()
        

@mainthread
def testing(scraper: Scraper, parent):
    qrcode = Image(source='res/canvas.png', pos_hint={'center': 0.5})
    message = Label(text='', size_hint=(1,None), height=50)

    def check_authenticated(instance):
        if scraper.statusString == sts.IDLE:
            # rectangle_update.cancel()
            authenticator.dismiss()

        else:
            message.text = str(scraper.statusString)

    def update_image(instance):
        if scraper.statusString == sts.IDLE:
            image_update.cancel()

        else:
            qrcode.reload()
                
    def update_rectangle(instance, value):
        rectangle.size = qrcode.size
        rectangle.pos = qrcode.pos


    def update_message(instance):
        if scraper.statusString == sts.IDLE:
            message_update.cancel()
            message.text = "Autenticado"

        else:
            message.text = str(scraper.statusString)


    button = Button(text='Close', size_hint=(1,None), height=50)
    button.bind(on_release=check_authenticated)
    qrcode.bind(pos=update_rectangle)
    qrcode.bind(size=update_rectangle)

    content = BoxLayout(orientation='vertical')
    content.add_widget(qrcode)
    content.add_widget(message)
    content.add_widget(button)
    
    with qrcode.canvas.before:
        Color(1,1,1,1)
        rectangle = Rectangle()

    authenticator = Popup(title='Authenticator', content=content, size_hint=(None,None), size=(400,500), auto_dismiss=False)
    authenticator.open()

    # rectangle_update = Clock.schedule_interval(update_rectangle, 0.1)
    image_update = Clock.schedule_interval(update_image, 2)
    message_update = Clock.schedule_interval(update_message, 0.5)


def edit_text(parent):
    """
    Funçao que instancia e abre um Popup com editor da mensagem do aplicativo
    """

    content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))
    buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

    cancel = Button(text='Cancelar', size_hint=(1, None), height=50)
    update = Button(text='Salvar', size_hint=(1, None), height=50)

    box = TextInput(
        text=parent.message,
        background_color=(0.5, 0.5, 0.5, 1)
    )

    buttons.add_widget(cancel)
    buttons.add_widget(update)

    content.add_widget(box)
    content.add_widget(buttons)

    editor = Popup(title='Editor', content=content, size_hint=(None, None), size=(300, 400), auto_dismiss=False)

    def save(self):
        parent.update(box.text)
        editor.dismiss()

    cancel.bind(on_press=editor.dismiss)
    update.bind(on_press=save)

    editor.open()


if __name__ == "__main__":
    MaxBot().run()
