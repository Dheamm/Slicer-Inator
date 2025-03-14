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

    def get_main_window(self):
        return self.main_window

    def get_render_window(self):
        return self.render_window

    def get_settings_window(self):
        return self.settings_window