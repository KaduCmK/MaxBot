import threading

from Scraper import Scraper
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.clock import CyClockBase, time, mainthread
from kivy.properties import StringProperty


class MaxBot(App):
    """
    **Classe Principal\n**

    Instancia a árvore de widgets do aplicativo
    """
    
    def build(self):
        """
        Construtor da árvore de widgets do aplicativo

        :return: raíz da árvore de widgets
        """
        self.second_thread()
        
        screen = BoxLayout(orientation='vertical', padding=10, spacing=10)

        upper = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        upper.add_widget(TextBox())
        upper.add_widget(TagMenu())

        screen.add_widget(upper)
        screen.add_widget(ProgressInfo())

        # window = AnchorLayout(anchor_x='center', anchor_y='center')
        # window = ModalView(background='background_image.png')
        window = ModalView()
        window.add_widget(screen)

        return window
    
    def second_thread(self):
        threading.Thread(target=self.call_scraper).start()

    def call_scraper(self):
        CyClockBase.schedule_once(self.start_scraper, 0)

    def start_scraper(self):
        self.sc = Scraper()


class TextBox(BoxLayout):
    """
    Classe criadora do campo de mensagem
    """

    # variével q guarda a mensagem atual
    message = StringProperty("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam a aliquam odio. Quisque ultrices purus ipsum, id dignissim quam feugiat in. Pellentesque id purus non urna volutpat vehicula. Integer turpis odio, viverra at massa vel, feugiat fermentum velit. Duis quis lacus scelerisque, dictum nibh vitae, facilisis lorem. Nulla vestibulum tincidunt ante vel tincidunt. Suspendisse at iaculis est. \n\nSed vitae quam fringilla, auctor tellus vel, volutpat mi. Sed rhoncus mi et ex tincidunt sagittis. In id est nec leo auctor ullamcorper quis a tortor. Nam tristique, nunc at pretium ultrices, lorem nisl cursus velit, eu consequat diam nulla id enim. Aliquam consectetur feugiat tellus, quis vehicula orci ultricies id. Proin nec leo at velit consectetur bibendum. Maecenas in nibh sodales, elementum eros vel, facilisis augue. Integer gravida libero nec leo cursus fermentum. Phasellus volutpat ullamcorper convallis. In euismod risus faucibus mollis accumsan. Donec sed orci ut nisl ullamcorper convallis. Vestibulum bibendum condimentum elit ac aliquam.")
    
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
        size = (instance.size[0]-10, instance.size[1])
        self.rectangle.size = instance.size
        self.rectangle.pos = instance.pos
        self.text_display.text_size = size

    def call_editor(self, instance):
        edit_text(self)

    def update(self, input_text):
        self.message = input_text
        self.text_display.text = self.message


class TagMenu(StackLayout):
    """
    Classe criadora do menu de etiquetas
    """

    def __init__(self, **kwargs):
        super(TagMenu, self).__init__(orientation='tb-lr', size_hint=(0.3,1))
        self.build()

    def build(self):
        '''
        Construtor da classe TagMenu
        '''

        updater = Button(
            text='Atualizar etiquetas',
            size_hint=(1,None),
            size=(200,44),
            pos_hint={'top': 1, 'center_x': .5}
        )

        menu = Spinner(
            text="Etiquetas",
            values=self.tags(),
            size_hint=(1,None),
            size=(200, 44),
            pos_hint={'top': .9}
        )
        menu._on_dropdown_select=self.show # testando resgate da opção selecionada no menu

        self.add_widget(updater)
        self.add_widget(menu)

    def tags(self):
        values = ("Tag 1", "Tag 2", "Tag 3", "Tag 4", "Tag 5")
        return values
    
    def show(self, instance, value):
        # print(text)
        pass


class ProgressInfo(BoxLayout):
    """
    Classe criadora da área de progresso e botão de enviar
    """

    max = 100
    current = 0
    current_status = StringProperty("Carregando")

    def __init__(self, **kwargs):
        super(ProgressInfo, self).__init__(orientation='vertical', padding=10, spacing=10, size_hint=(1,0.4), **kwargs)
        self.build()

    def build(self):
        '''
        Construtor da classe ProgressInfo
        '''

        status = Label(
            text=self.current_status,
            font_size=20,
            size_hint=(1, None),
            halign='center',
            pos_hint={'bottom': 0.1}
        )

        progress = ProgressBar(
            value_normalized=0.65
        )

        enviar = Button(
            text="Enviar",
            size_hint=(None,None),
            size=(100,44),
            pos_hint={'center_x': .5}
        )

        self.add_widget(status)
        self.add_widget(progress)
        self.add_widget(enviar)


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
