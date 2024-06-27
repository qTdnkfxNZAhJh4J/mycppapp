import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class StatisticsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        label = Label(text='Статистика по пройденным тестам', halign='left')
        layout.add_widget(label)
        
        quiz_stats = self.get_quiz_statistics('/Users/nikita/Documents/mycppapp/assets/quiz')
        for filename, points_scored in quiz_stats.items():
            test_name = os.path.splitext(filename)[0] 
            label = Label(text=f'{test_name}: {points_scored} баллов из 30', halign='left')
            layout.add_widget(label)
        
        layout.add_widget(Label())
        label = Label(text='Статусы заданий:', halign='left')
        layout.add_widget(label)
        
        tasks_info = self.get_tasks_info('/Users/nikita/Documents/mycppapp/assets/tasks.json')
        for task_id, task_title, task_status in tasks_info:
            label = Label(text=f'Задание {task_id}: {task_title} - {task_status}', halign='left')
            layout.add_widget(label)
        
        back_button = Button(text='Назад', size_hint_y=None, height='40dp')
        back_button.bind(on_press=self.go_to_home)
        layout.add_widget(back_button)
        
        self.add_widget(layout)

    def go_to_home(self, instance):
        self.manager.current = 'home'
    
    def get_quiz_statistics(self, directory):
        quiz_stats = {}
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                with open(os.path.join(directory, filename), 'r') as file:
                    data = json.load(file)
                    quiz_stats[filename] = data.get('points_scored', 0)
        return quiz_stats
    
    def get_tasks_info(self, filepath):
        tasks_info = []
        with open(filepath, 'r') as file:
            data = json.load(file)
            tasks = data.get('tasks', [])
            for task in tasks:
                task_id = task.get('id', '')
                task_title = task.get('title', '')
                task_status = task.get('status', '')
                tasks_info.append((task_id, task_title, task_status))
        return tasks_info
