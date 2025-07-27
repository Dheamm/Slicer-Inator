# Local Classes:
from Interface.MainWindow import MainWindow # Import MainWindow local class.
from Interface.RenderWindow import RenderWindow # Import RenderWindow local class.
from Interface.SettingsWindow import SettingsWindow # Import SettingsWindow local class.
from Threads.RenderThread import RenderThread # Import RenderThread local class.
from Logic.FileManager import FileManager # Import FileManager local class.
from Logic.Slicer import Slicer # Import Slicer local class.
from PyQt5.QtCore import QThread # To create threads.

from Logic.JsonCreator import JsonCreator # Import JsonCreator local class.

class Controller():
    def __init__(self):
        self.json_creator = JsonCreator()
        self.data_json = self.json_creator.get_full_json()


        self.file_manager = FileManager()
        self.slicer = Slicer(self.data_json['duration'],
                            self.data_json['transitions'])
        self.render_thread = RenderThread(self.file_manager, self.slicer, self.json_creator)

        self.main_window = MainWindow(self.data_json)
        self.main_window.labels[0].setText(f'Input │ {self.file_manager.get_input_path()}')
        if self.file_manager.get_output_path():
            self.main_window.labels[1].setText(f'Output │ {self.file_manager.get_output_path()}')
            self.main_window.buttons[3].setEnabled(True)
        else:
            self.main_window.labels[1].setText(f'Output │ No Selected (Default)')
            self.main_window.buttons[3].setEnabled(False) # Disable the button if the output path is not set.

        self.render_window = RenderWindow(self.data_json)
        self.settings_window = SettingsWindow(self.data_json)

        self.main_window.set_controller(self)
        self.render_window.set_controller(self)
        self.settings_window.set_controller(self)

        self.main_window.theme_applied_signal.connect(self.handle_applied_theme)
        self.main_window.open_directory_signal.connect(self.handle_open_directory)
        self.main_window.select_directory_signal.connect(self.handle_select_directory)

        self.render_window.start_rendering_signal.connect(self.handle_start_rendering)
        self.render_window.stop_rendering_signal.connect(self.handle_stop_rendering)

        self.settings_window.settings_applied.connect(self.handle_applied_settings)


    def get_main_window(self):
        return self.main_window

    def get_render_window(self):
        return self.render_window

    def get_settings_window(self):
        return self.settings_window

    def handle_applied_settings(self, updated_data: dict):
        print("The following settings were applied:", updated_data)

        # Aquí podrías actualizar la lógica, por ejemplo:
        for key, value in updated_data.items():
            if value.isdigit():
                value = int(value)
            self.json_creator.set_json(key, value)

    def handle_applied_theme(self, theme: str):
        print(f"Theme applied: {theme}")
        self.json_creator.set_json('theme', theme)
        self.main_window.load_theme(theme)
        self.render_window.load_theme(theme)
        self.settings_window.load_theme(theme)

    def handle_open_directory(self, directory_type: str):
        if directory_type == 'input_path':
            self.file_manager.open_directory(self.file_manager.get_input_path())
        elif directory_type == 'output_path':
            print(self.file_manager.get_output_path())
            self.file_manager.open_directory(self.file_manager.get_output_path())

    def handle_select_directory(self, directory_type: str):
        if directory_type == 'input_path':
            path = self.main_window.select_directory(self.file_manager.get_input_path())
            if path:
                self.file_manager.set_input_path(path)
                self.main_window.labels[0].setText(f'Input │ {path}')
        elif directory_type == 'output_path':
            path = self.main_window.select_directory(self.file_manager.get_input_path())
            if path:
                self.file_manager.set_output_path(path)
                print(self.file_manager.get_output_path())
                self.main_window.labels[1].setText(f'Output │ {path}')
                self.main_window.buttons[3].setEnabled(True)

    def handle_start_rendering(self):
        self.render_thread.signal_progress_logger.connect(self.render_window.update_progress_bar) # Percentage of the progress bar.
        self.render_thread.signal_status_logger.connect(self.render_window.update_status_logger) # Status logger of the progress bar.
        self.render_thread.signal_archive_count_message.connect(self.render_window.update_archive_count)
        self.render_thread.signal_status_message.connect(self.render_window.update_status_message)
        self.render_thread.signal_name_message.connect(self.render_window.update_name_message)
        self.render_thread.signal_timer_start.connect(self.render_window.timer_start)
        self.render_thread.signal_timer_stop.connect(self.render_window.timer_stop)
        # self.render_thread.signal_status.connect(self.handle_render_error)
        # self.render_thread.signal_processed.connect(self.update_info)

        self.render_thread.start() # Start the render thread.

    def handle_stop_rendering(self):
        if self.render_thread is not None:
            self.render_thread.terminate()

        self.file_manager.close_ffmpeg_process()
        QThread.msleep(100) # Wait for the process to close.
        self.file_manager.delete_temp_files()