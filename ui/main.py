from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty


class MaxBot(App):
    def build(self):
        screen = BoxLayout(orientation='vertical', padding=10, spacing=10)

        upper = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        upper.add_widget(TextBox().build())
        upper.add_widget(TagMenu().build())

        screen.add_widget(upper)
        screen.add_widget(ProgressInfo().build())

        window = AnchorLayout(anchor_x='center', anchor_y='center')
        window.add_widget(screen)

        return window


class TextBox():
    message = "The ScrollView manages the position of its children similarly to a RelativeLayout but does not use the size_hint. You must carefully specify the size of your content to get the desired scroll/pan effect.\n By default, the size_hint is (1, 1), so the content size will fit your ScrollView exactly (you will have nothing to scroll). You must deactivate at least one of the size_hint instructions (x or y) of the child to enable scrolling. Setting size_hint_min to not be None will also enable scrolling for that dimension when the ScrollView is smaller than the minimum size.\nTo scroll a GridLayout on it’s Y-axis/vertically, set the child’s width to that of the ScrollView (size_hint_x=1), and set the size_hint_y property to None:"

    def build(self):
        box = BoxLayout(orientation='vertical', spacing=10)
        scroll_box = ScrollView(
            size_hint=(1,1),
            size=box.size
        )

        text_display = Label(
            text=self.message,
            size_hint=(1,None),
            text_size=(600,None)
        )

        button = Button(
            text="Editar mensagem",
            size_hint=(None,None),
            width=150,
            height=44,
            pos_hint={'center_x': 0.5},
            on_release=edit_text
        )
        
        scroll_box.add_widget(text_display)

        box.add_widget(scroll_box)
        box.add_widget(button)

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
            halign='center',
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


def edit_text(instance):
    content = BoxLayout(
        orientation='vertical', 
        padding=10, 
        spacing=10, 
        size_hint=(1,1)
    )
    
    buttons = BoxLayout(
        orientation='horizontal', 
        size_hint=(1,0.2)
    )

    cancel = Button(
        text='Cancelar', 
        size_hint=(1,None), 
        height=50
    )

    update = Button(
        text='Salvar', 
        size_hint=(1,None), 
        height=50
    )

    box = ScrollView(size_hint=(1,1))
    box.add_widget(TextInput(background_color=(0.5,0.5,0.5,1)))

    buttons.add_widget(cancel)
    buttons.add_widget(update)

    content.add_widget(box)
    content.add_widget(buttons)

    editor = Popup(
        title='Editor',
        content=content,
        size_hint=(None,None),
        size=(300,400),
        auto_dismiss=False
    )
    
    cancel.bind(on_press=editor.dismiss)

    editor.open()


if __name__ == "__main__":
    MaxBot().run()
