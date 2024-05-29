from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
# from kivy.uix.image import Image
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty


"""
Criar classes para cada objeto, label, widget...
Deixar configurações de design para o arquivo KV
"""


# class QRcode(ModalView):
#     def


class Authentication_Screen(Widget):        
    # verifica autenticação
    # leitura do QR-code
    # inicializa as outras telas

    def build(self):
        if self.check_authenticated():
            # avisa que já está autenticado e carrega página principal
            # animação de inicio
            return Main_Screen().build()

        else:
            # chama classe que apresenta QRcode e monitora autenticação
            pass

        return Main_Screen().build()
    
    def check_authenticated(self):
        return True
    

class Main_Screen(Widget):
    # lista de etiquetas
    # caixa de mensagem
    # barra de progresso
    # botão de interação

    def build(self):
        boxes = BoxLayout(orientation='vertical')
        upper = BoxLayout(orientation='horizontal')
        lower = BoxLayout(orientation='vertical')
        
        upper.add_widget(Label(text="caixa de texto"))
        upper.add_widget(Label(text="etiquetas e menu"))
        lower.add_widget(Label(text="texto de progresso"))
        lower.add_widget(Label(text="barra de progresso"))
        lower.add_widget(Label(text="botoes"))
        
        boxes.add_widget(upper)
        boxes.add_widget(lower)
        return boxes


class MaxBot(App):
    image = StringProperty()

    def build(self):
        self.image = "background_image.png"
        parent = ModalView(background_color=(0.7,0.9,0.7,1))
        parent.add_widget(Main_Screen().build())
        return parent


if __name__ == "__main__":
    MaxBot().run()