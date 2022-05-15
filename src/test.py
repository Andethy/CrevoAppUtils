from application.app import App
from application.utils import *


class TestApp(App):

    def __init__(self):
        screen_a = ScreenUtil('Home',
                              input_label=[LabelCustom("This is home.\nInput a text File.", height=25), 0.5, 0.25],
                              file_button=[FileButtonCustom(self.home_validated, self.home_invalidated), 0.5, 0.5],
                              error_label=[LabelCustom(''), 0.5, 0.75])
        screen_b = ScreenUtil('Config',
                              test_label=[LabelCustom("This is config.\nInput a csv file.", height=25), 0.5, 0.25],
                              file_button=[FileButtonCustom(self.config_validated, data_type='csv'), 0.5, 0.5],
                              error_label=[LabelCustom(''), 0.5, 0.75])

        self.m_file = BaseFileIO()

        super().__init__(title='Test App',
                         dimensions=(400, 500),
                         screens=[screen_a(), screen_b()])

    def home_validated(self, file_path):
        self.m_screen('Config').set_screen()
        self.m_file.set_file(file_path)
        self.m_file.set_data_txt()
        print(self.m_file.get_data())

    def home_invalidated(self):
        self.m_screen('Home').widgets['error_label'].set_value('Error - wrong file type!')

    def config_validated(self, file_path):
        self.m_screen('Home').set_screen()

    def config_invalidated(self):
        self.m_screen('Home').widgets['error_label'].set_value('Error - wrong file type!')


if __name__ == '__main__':
    TestApp()
