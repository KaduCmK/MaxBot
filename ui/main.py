from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.anchorlayout import AnchorLayout


class MaxBot(App):
    def build(self):
        screen = BoxLayout(orientation='vertical')

        upper = BoxLayout(orientation='horizontal')
        upper.add_widget(TextBox().build())
        upper.add_widget(TagMenu().build())

        screen.add_widget(upper)
        screen.add_widget(ProgressInfo().build())

        window = AnchorLayout(anchor_x='center', anchor_y='center')
        window.add_widget(screen)

        return window


class MainScreen(Widget):
    def build(self):
        coisa = TextBox().build()
        return coisa


class TextBox():
    def build(self):
        box = TextInput()
        return box


class TagMenu():
    def build(self):
        menu = Spinner(
            text="Etiquetas",
            values=self.tags(),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_y': .9}
        )
        return menu

    def tags(self):
        values = ("Tag 1", "Tag 2", "Tag 3", "Tag 4")
        return values


class ProgressInfo():
    max: int
    current: int
    current_status = "Loading"

    def build(self):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        status = Label(
            text=self.current_status,
            font_size=20,
            size_hint=(1, None),
            halign='center'
        )

        progress = ProgressBar(
            value_normalized=0.65
        )

        enviar = Button(text="Enviar")

        box.add_widget(status)
        box.add_widget(progress)
        box.add_widget(enviar)

        return box

    # def current_status(self):
    #     return "Loading"

    # def current_progress(self):
    #     return


if __name__ == "__main__":
    MaxBot().run()
