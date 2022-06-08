import json
import os
import time

from src.application.app import App
from src.application.utils import *
from src.application.constants import *
from multitasking import task as multi
from shutil import copy as copy


class JsonApp(App):
    json_file_dev_path: str = resource_path('data/output.json')
    csv_file_dev_path: str = resource_path('data/output.csv')

    def __init__(self):
        self.m_file = BaseFileIO()
        self.m_entry = JsonIO()
        self.m_output = JsonToCsvIO()
        self.m_input_dir = DirectoryIO('manipulator_json/input_folder')
        self.m_used_dir = DirectoryIO('manipulator_json/used_folder')

        self.m_entry.set_file(JsonApp.json_file_dev_path)
        self.m_output.set_file(JsonApp.csv_file_dev_path)

        self.running = True

        home = ScreenUtil('Home',
                          input_label=[LabelCustom('Input text file.', height=25), 0.5, 0.25],
                          file_button=[FileButtonCustom(self.input_validated, self.input_invalidated), 0.5, 0.5],
                          result_label=[LabelCustom(''), 0.5, 0.75],
                          json_screen=[ButtonCustom(self.set_export, w=5, content='[Export]'), 0.75, 0.9],
                          csv_screen=[ButtonCustom(self.set_config, w=5, content='[Config]'), 0.25, 0.9])

        export = ScreenUtil('Export',
                            file_button=[ButtonCustom(self.update_csv, w=10, content='Update CSV file'), 0.5, 0.5],
                            result_label=[LabelCustom(), 0.5, 0.75],
                            home_screen=[ButtonCustom(self.set_home, w=5, content='[Home]'), 0.5, 0.9])

        config = ScreenUtil('Config',
                            reset_button=[ButtonCustom(self.reset_json, w=10, content='Reset Json file'), 0.5, 0.5],
                            auto_button=[CheckbuttonCustom('Auto mode'), 0.5, 0.7],
                            home_screen=[ButtonCustom(self.set_home, w=5, content='[Home]'), 0.5, 0.9])

        self.automated_process()

        super().__init__(title='Crevolution Json Manipulation',
                         dimensions=(400, 400),
                         logo='resources/logo_json.png',
                         screens=[home(), config(), export()])

        self.running = False

    def input_validated(self, file_path):
        self.m_file.set_file(file_path)
        self.m_file.set_data_txt()
        self.m_entry.add_entries(self.m_file.data)
        self.m_screen('Home').widgets['result_label'].set_value('Success.')

    def input_invalidated(self):
        self.m_screen('Home').widgets['result_label'].set_value('Error.')

    def set_export(self):
        self.m_screen('Export').set_screen()

    def set_config(self):
        self.m_screen('Config').set_screen()

    def set_home(self):
        self.m_screen('Home').set_screen()

    def update_csv(self):
        self.m_output.write_2da(self.m_entry.get_entries())

    def reset_json(self):
        self.m_entry.clear_entries()
        pass

    @multi
    def automated_process(self):
        print("???")
        while self.running:
            time.sleep(1)
            if not self.running: break
            if all([self.m_screen('Config').widgets['auto_button'].get_value() == 1, self.m_input_dir.files_exist()]):
                for file in self.m_input_dir.get_files_of_type('txt'):
                    self.input_validated(self.m_input_dir.get_file_path(file))
                    self.update_csv()
                    self.m_input_dir.move_file(file, self.m_used_dir)


class JsonIO(BaseFileIO):

    def __init__(self):
        super().__init__()

    def add_entries(self, txt_input):

        with open(self.file_path, 'r', encoding="utf-8", errors="replace") as self.file:
            self.data = json.load(self.file)

        for n, txt_input in enumerate(txt_input):
            entry = {}
            for index, key in enumerate(FIELD_KEYS):
                entry[key] = txt_input[index]
            self.data.append(entry)

        self.file = open(self.file_path, 'w', encoding="utf-8", errors="replace")
        self.file.write(json.dumps(self.data, sort_keys=False, indent=4))
        self.file.close()

    def clear_entries(self):
        with open(self.file_path, 'w', encoding="utf-8", errors="replace") as self.file:
            self.file.write(json.dumps([], sort_keys=False, indent=4))

    def get_entries(self):
        try:
            with open(self.file_path, 'r') as self.file:
                self.data = json.load(self.file)
                print("DATA:", self.data)
        except FileNotFoundError:
            print("NOT FOUND?")
        print(self.data)
        return self.data


class JsonToCsvIO(CsvFileIO):

    def __init__(self):
        super().__init__()

    def write_2da(self, data):
        print("DATA 2:", data)
        with open(self.file_path, 'w') as self.file:
            row: dict
            for row in data:
                self.file.write(','.join(list(map(str, list(row.values())[:-1]))) + ','
                                + list(row.values())[-1].replace(',', '，') + '\n')


class DirectoryIO(BaseDirectoryIO):

    def __init__(self, *args):
        super().__init__(*args)

    def files_exist(self) -> bool:
        return True if len(os.listdir(self.dir_path)) >= 1 else False

    def get_file_path(self, file):
        return os.path.join(self.dir_path, file)

    def get_files_of_type(self, extension) -> list[str]:
        files = []
        for file in os.listdir(self.dir_path):
            if file.lower().endswith('.' + extension):
                files.append(file)
        print('FILES FOUND: ', files)
        return files

    def move_file(self, file, output_dir):
        """

        :type file: str
        :type output_dir: DirectoryIO
        """
        copy(self.get_file_path(file), output_dir())
        self.delete_file(file)

    def delete_file(self, file):
        try:
            os.remove(self.get_file_path(file))
        except FileNotFoundError:
            pass

    def delete_all_files(self):
        for file in os.listdir(self.dir_path):
            os.remove(self.get_file_path(file))


def execute():
    JsonApp()
