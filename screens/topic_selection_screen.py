from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import os

class TopicSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_topics()

    def load_topics(self):
        documents_folder = '/Users/nikita/Documents/mycppapp/assets/documents'
        if not os.path.exists(documents_folder):
            print("Documents folder not found:", documents_folder)
            return

        files = os.listdir(documents_folder)
        docx_files = [f for f in files if f.endswith('.docx')]

        try:
            docx_files.sort(key=lambda x: os.path.getctime(os.path.join(documents_folder, x)))  # Сортировка по возрастанию даты создания
        except FileNotFoundError as e:
            print(f"Error sorting files: {e}")

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for file_name in docx_files:
            try:
                button = Button(text=file_name[:-5], size_hint_y=None, height='40dp')  # Масштабируем высоту кнопок
                button.bind(on_release=lambda instance, file_name=file_name: self.show_topic_content(file_name))
                layout.add_widget(button)
            except Exception as e:
                print(f"Error creating button for file {file_name}: {e}")

        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100))  # Уменьшаем высоту на 100 для размещения кнопки "назад"
        scrollview.add_widget(layout)
        self.add_widget(scrollview)

        # Создаем кнопку "назад"
        back_button = Button(text="Назад", size_hint=(1, None), height='40dp')  # Масштабируем высоту кнопки
        back_button.bind(on_release=self.go_back)  # Привязываем метод go_back к нажатию кнопки "назад"
        self.add_widget(back_button)

    def show_topic_content(self, file_name):
        content_file = os.path.join('/Users/nikita/Documents/mycppapp/assets/documents', file_name)
        try:
            with open(content_file) as f:
                content = f.read()
                file_screen = FileContentScreen(name=file_name[:-5], content=content, file_name=file_name[:-5])  # Создаем экран с содержимым файла
                self.manager.add_widget(file_screen)  # Добавляем экран в ScreenManager
                self.manager.current = file_name[:-5]  # Переходим на новый экран
        except FileNotFoundError:
            print(f"Content file not found: {content_file}")

    def go_back(self, instance):
        self.manager.current = 'home'

class FileContentScreen(Screen):
    def __init__(self, content, file_name, **kwargs):
        super().__init__(**kwargs)
        text_input = TextInput(text=content, readonly=True, size_hint=(1, None), height=Window.height, multiline=True)  # Используем масштабируемый размер и прокрутку в начало
        text_input.scroll_y = 1  # Устанавливаем прокрутку в начало
        self.add_widget(text_input)

        # Добавляем кнопку "назад"
        back_button = Button(text="Назад", size_hint=(1, None), size=(Window.width, Window.height * 0.05))  # Масштабируем размер кнопки
        back_button.bind(on_release=self.go_back)  # Привязываем метод go_back к нажатию кнопки "назад"
        self.add_widget(back_button)

    def go_back(self, instance):
        self.manager.current = 'topic_selection'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TopicSelectionScreen(name='topic_selection'))
        return sm

if __name__ == '__main__':
    MyApp().run()
