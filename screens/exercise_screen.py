import json
import subprocess
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

class ExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_task_index = None
        self.tasks = load_tasks('/Users/nikita/Documents/mycppapp/assets/tasks.json')  
        self.current_task_index = self.get_next_task_index()  

        layout = BoxLayout(orientation='vertical')

        self.task_label = Label(text='', size_hint=(1, None), height=dp(100), font_size=dp(14))
        self.input_text = TextInput(text='', size_hint=(1, 1), font_size=dp(14))

        layout.add_widget(self.task_label)
        layout.add_widget(self.input_text)

        button_layout = BoxLayout(size_hint=(1, None), height=dp(40))

        back_button = Button(text='Главное меню', size_hint=(1/3, 1), height='40dp')
        back_button.bind(on_press=self.go_to_home)
        
        send_button = Button(text='Отправить код для проверки', size_hint=(1/3, 1), height='40dp')
        send_button.bind(on_press=self.send_code)
        
        next_button = Button(text='Следующее задание', size_hint=(1/3, 1), height='40dp')
        next_button.bind(on_press=self.next_task)

        button_layout.add_widget(back_button)
        button_layout.add_widget(send_button)
        button_layout.add_widget(next_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)
        self.display_task()

    def display_task(self):
        if self.current_task_index is not None:
            task = self.tasks[self.current_task_index]
            if task.get('status') == 'не выполнено':
                task_text = f"Задание {task['id']}: {task['title']}\n\n{task['description']}"

                self.task_label.text = task_text
                self.task_label.text_size = (self.width - 20, None)  
                self.task_label.size_hint_y = None
                self.task_label.height = self.task_label.texture_size[1] + 40  

                self.input_text.text = ''
            else:
                unfinished_tasks = [t for t in self.tasks if t.get('status') == 'не выполнено']
                if not unfinished_tasks:
                    self.task_label.text = "Все задания выполнены!"
                    self.input_text.text = ''
                else:
                    next_index = (self.current_task_index + 1) % len(self.tasks)
                    while self.tasks[next_index].get('status') != 'не выполнено':
                        next_index = (next_index + 1) % len(self.tasks)
                    self.current_task_index = next_index
                    self.display_task()

    def next_task(self, instance):
        if self.current_task_index is not None:
            next_index = self.get_next_task_index()
            if next_index is not None:
                self.current_task_index = next_index
                self.display_task()

    def get_next_task_index(self):
        next_index = 0
        if self.current_task_index is not None:
            next_index = self.current_task_index + 1
            if next_index >= len(self.tasks):
                next_index = 0
            while next_index != self.current_task_index:
                if not self.tasks[next_index].get('выполнено', False):
                    return next_index
                next_index = (next_index + 1) % len(self.tasks)
        return next_index

    def go_to_home(self, instance):
        self.manager.current = 'home'
    
    def send_code(self, instance):
        cpp_code = self.input_text.text

        with open("temp_code.cpp", "w") as file:
            file.write(cpp_code)

        compilation_result = subprocess.run(["g++", "temp_code.cpp", "-o", "executable"], capture_output=True)

        if compilation_result.returncode == 0:
            with open("tasks.json", "r") as file:
                tasks_data = json.load(file)

            for task in tasks_data["tasks"]:
                if task["status"] == "не выполнено":
                    input_data = task.get("input", "")
                    
                    execution_result = subprocess.run(["./executable"], input=input_data.encode(), capture_output=True)

                    if execution_result.stdout.decode("utf-8") == task["expected_output"]:
                        task["status"] = "выполнено"
                        with open("tasks.json", "w") as file:
                            json.dump(tasks_data, file)
                            
                        self.task_label.text = "Задание выполнено!"
                        self.input_text.text = ''
                        return  

            self.task_label.text = "Все задания выполнены!"
            self.input_text.text = ''
        else:
            self.task_label.text = "Ошибка компиляции. Проверьте ваш код на C++."

def load_tasks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file).get('tasks', [])
