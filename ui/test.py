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
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty


class MaxBot(App):
    def build(self):
        screen = BoxLayout(orientation='vertical', padding=10, spacing=10)

        upper = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        upper.add_widget(TextBox())
        upper.add_widget(TagMenu())

        screen.add_widget(upper)
        screen.add_widget(ProgressInfo())

        window = AnchorLayout(anchor_x='center', anchor_y='center')
        window.add_widget(screen)

        return window


class TextBox(BoxLayout):
    message = StringProperty("The ScrollView manages the position of its children similarly to a RelativeLayout but does not use the size_hint. You must carefully specify the size of your content to get the desired scroll/pan effect.\n By default, the size_hint is (1, 1), so the content size will fit your ScrollView exactly (you will have nothing to scroll). You must deactivate at least one of the size_hint instructions (x or y) of the child to enable scrolling. Setting size_hint_min to not be None will also enable scrolling for that dimension when the ScrollView is smaller than the minimum size.\nTo scroll a GridLayout on it’s Y-axis/vertically, set the child’s width to that of the ScrollView (size_hint_x=1), and set the size_hint_y property to None:")

    def __init__(self, **kwargs):
        super(TextBox, self).__init__(orientation='vertical', spacing=10, **kwargs)
        self.build()

    def build(self):
        scroll_box = ScrollView(size_hint=(1, 1))
        self.text_display = Label(
            text=self.message, 
            size_hint=(1, None), 
            text_size=(600, None),
            color=(0,0,0,1), 
            valign='top'
        )
        self.text_display.bind(texture_size=self.update_height)

        with self.text_display.canvas.before:
            Color(1, 1, 1, 1)  # Set the color to white
            self.rect = Rectangle(size=self.text_display.size, pos=self.text_display.pos)
            self.text_display.bind(size=self.update_rect, pos=self.update_rect)

        button = Button(text="Editar mensagem", size_hint=(None, None), width=150, height=44, pos_hint={'center_x': 0.5})
        button.bind(on_release=self.call_editor)

        scroll_box.add_widget(self.text_display)
        self.add_widget(scroll_box)
        self.add_widget(button)

    def update_height(self, instance, value):
        instance.height = instance.texture_size[1]
        self.update_rect(instance, value)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def call_editor(self, instance):
        edit_text(self)

    def update(self, input_text):
        self.message = input_text
        self.text_display.text = self.message


class TagMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(TagMenu, self).__init__(orientation='vertical', **kwargs)
        self.build()

    def build(self):
        menu = Spinner(
            text="Etiquetas",
            values=self.tags(),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_y': .9}
        )
        self.add_widget(menu)

    def tags(self):
        values = ("Tag 1", "Tag 2", "Tag 3", "Tag 4")
        return values


class ProgressInfo(BoxLayout):
    max = 100
    current = 0
    current_status = StringProperty("Loading")

    def __init__(self, **kwargs):
        super(ProgressInfo, self).__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.build()

    def build(self):
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

        self.add_widget(status)
        self.add_widget(progress)
        self.add_widget(enviar)


def edit_text(parent):
    content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))
    buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

    cancel = Button(text='Cancelar', size_hint=(1, None), height=50)
    update = Button(text='Salvar', size_hint=(1, None), height=50)

    box = TextInput(background_color=(0.5, 0.5, 0.5, 1))

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
