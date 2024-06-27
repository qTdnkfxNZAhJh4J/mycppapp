import os
import glob
import json
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

class TestScreen(Screen):
    def on_pre_enter(self):
        self.load_topics()

    def load_topics(self):
        docs_folder = '/Users/nikita/Documents/mycppapp/assets/quiz'
        json_files = glob.glob(os.path.join(docs_folder, '*.json'))
        json_files.sort(key=lambda x: os.path.getctime(x))
        topics = [os.path.splitext(os.path.basename(file))[0] for file in json_files]
        self.add_buttons(topics)

    def add_buttons(self, topics):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for topic in topics:
            button = Button(text=topic, size_hint_y=None, height='40dp')
            button.bind(on_release=lambda instance, topic=topic: self.show_topic_content(topic))
            layout.add_widget(button)

        scrollview = ScrollView(size_hint=(1, 0.9))
        scrollview.add_widget(layout)
        
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(scrollview)

        back_button = Button(text="Назад", size_hint=(1, 0.1), height='40dp')
        back_button.bind(on_release=self.go_back)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def show_topic_content(self, topic):
        json_file = f'/Users/nikita/Documents/mycppapp/assets/quiz/{topic}.json'
        with open(json_file, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
            quiz = quiz_data.get("quiz")
            if quiz is not None:
                questions = quiz.get("questions")
                if questions is not None:
                    self.display_questions(questions)
                else:
                    print("Key 'questions' not found in JSON data.")
            else:
                print("Key 'quiz' not found in JSON data.")

    def display_questions(self, questions):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        self.current_quiz_questions = questions

        for question in questions:
            question_text = question["question"]
            question_label = Label(text=question_text, size_hint_y=None, halign='left', valign='middle', text_size=(Window.width - 40, None))
            question_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
            layout.add_widget(question_label)

            options = question["options"]
            question["option_buttons"] = []
            for option in options:
                option_button = Button(text=option, size_hint_y=None, height='40dp')
                option_button.bind(on_release=self.on_option_button_pressed)
                question["option_buttons"].append(option_button)
                layout.add_widget(option_button)

        if 'questions_screen' not in self.manager.screen_names:
            questions_screen = Screen(name='questions_screen')
            self.manager.add_widget(questions_screen)
        else:
            questions_screen = self.manager.get_screen('questions_screen')
            questions_screen.clear_widgets()

        scrollview = ScrollView(size_hint=(1, 0.9))
        scrollview.add_widget(layout)
        
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(scrollview)

        float_layout = BoxLayout(size_hint=(1, 0.1), orientation='horizontal')
        finish_button = Button(text="Завершить тест", size_hint=(0.5, 1))
        finish_button.bind(on_release=self.finish_test)
        float_layout.add_widget(finish_button)

        back_button = Button(text="Назад", size_hint=(0.5, 1))
        back_button.bind(on_release=self.go_back)
        float_layout.add_widget(back_button)

        main_layout.add_widget(float_layout)

        questions_screen.add_widget(main_layout)

        self.manager.current = 'questions_screen'

    def on_option_button_pressed(self, instance):
        for question in self.current_quiz_questions:
            if instance in question["option_buttons"]:
                for option_button in question["option_buttons"]:
                    option_button.background_color = (1, 1, 1, 1)
                instance.background_color = (0, 1, 0, 1)
                question["selected_option"] = instance.text

    def finish_test(self, instance):
        total_points = 0
        for question in self.current_quiz_questions:
            correct_answer = question.get("correct_answer")
            selected_option = question.get("selected_option")
            if correct_answer is not None and selected_option is not None:
                if correct_answer == selected_option:
                    total_points += question.get("points", 0)
        print("Total points:", total_points)
        self.manager.current = 'home'

    def go_back(self, instance):
        self.manager.current = 'home'
