# Local Classes:
from Interface.MainWindow import MainWindow # Import MainWindow local class.
from Interface.RenderWindow import RenderWindow # Import RenderWindow local class.
from Interface.SettingsWindow import SettingsWindow # Import SettingsWindow local class.

class WindowsController():
    def __init__(self):
        self.main_window = MainWindow()
        self.render_window = RenderWindow()
        self.settings_window = SettingsWindow()

        self.main_window.set_controller(self)
        self.render_window.set_controller(self)
        self.settings_window.set_controller(self)

    def execute_main_window(self):
        self.main_window.open()

    def execute_render_window(self):
        self.render_window.open()

    def execute_settings_window(self):
        self.settings_window.open()