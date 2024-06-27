from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_string('''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'

        Image:
            source: '/Users/nikita/Documents/mycppapp/assets/cpp.png'  # Путь к вашему изображению
            size_hint_y: 0.7  # Размер изображения занимает 80% высоты экрана

        Button:
            text: 'Изучить тему'
            size_hint_y: 0.1  # Кнопка занимает 10% высоты экрана
            on_release: root.manager.current = 'topic_selection'  

        Button:
            text: 'Пройти тест'
            size_hint_y: 0.1  # Кнопка занимает 10% высоты экрана
            on_release: root.manager.current = 'test'  
        
        Button:
            text: 'Практические задания'
            size_hint_y: 0.1  # Кнопка занимает 10% высоты экрана
            on_release: root.manager.current = 'exercise'  
                                
        Button:
            text: 'Просмотреть статистику'
            size_hint_y: 0.1  # Кнопка занимает 10% высоты экрана
            on_release: root.manager.current = 'statistics'  
''')

class HomeScreen(Screen):
    pass
