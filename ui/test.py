import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window


class MyApp(App):
    def build(self):
        self.progress_value = 0

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Message input
        self.message_input = TextInput(hint_text="Enter your message here", size_hint_y=None, height=40)
        layout.add_widget(self.message_input)

        # Option chooser
        self.option_spinner = Spinner(
            text='Choose an option',
            values=('Option 1', 'Option 2', 'Option 3'),
            size_hint=(None, None),
            size=(200, 44)
        )
        layout.add_widget(self.option_spinner)

        # Button to update text box
        update_button = Button(text='Update Text Box')
        update_button.bind(on_press=self.update_text_box)
        layout.add_widget(update_button)

        # Scrollable text box
        self.scrollable_text_box = ScrollView(size_hint=(1, None), size=(Window.width, 150))
        self.text_label = Label(text='', size_hint_y=None, markup=True)
        self.text_label.bind(texture_size=self.update_text_label_height)
        self.scrollable_text_box.add_widget(self.text_label)
        layout.add_widget(self.scrollable_text_box)

        # Progress bar
        self.progress_bar = ProgressBar(max=100, value=self.progress_value)
        layout.add_widget(self.progress_bar)

        # Button to start progress
        start_button = Button(text='Start Progress')
        start_button.bind(on_press=self.start_progress)
        layout.add_widget(start_button)

        return layout

    def update_text_label_height(self, instance, value):
        instance.height = value[1]

    def update_text_box(self, instance):
        # Update the text in the scrollable text box with the message input
        self.text_label.text += self.message_input.text + '\n'

    def start_progress(self, instance):
        # Schedule the progress increment every 0.1 seconds
        Clock.schedule_interval(self.increment_progress, 0.1)

    def increment_progress(self, dt):
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress_bar.value = self.progress_value
        else:
            # Stop incrementing once the progress reaches 100
            Clock.unschedule(self.increment_progress)


MyApp().run()
