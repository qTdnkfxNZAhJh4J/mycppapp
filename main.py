from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screens.home_screen import HomeScreen
from screens.exercise_screen import ExerciseScreen
from screens.test_screen import TestScreen
from screens.statistics_screen import StatisticsScreen
from screens.topic_selection_screen import TopicSelectionScreen

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ExerciseScreen(name='exercise'))
        sm.add_widget(TestScreen(name='test'))
        sm.add_widget(StatisticsScreen(name='statistics'))
        topic_selection_screen = TopicSelectionScreen(name='topic_selection')
        sm.add_widget(topic_selection_screen)
        
        return sm

if __name__ == '__main__':
    MyApp().run()