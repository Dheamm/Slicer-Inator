# Local Classes:
from Interface.MainWindow import MainWindow # Import MainWindow local class.
from Interface.RenderWindow import RenderWindow # Import RenderWindow local class.

class WindowsController():
    def __init__(self, file_manager, slicer):
        self.file_manager = file_manager
        self.slicer = slicer
        self.main_window = MainWindow(self.file_manager, self.slicer)
        self.render_window = RenderWindow(self.file_manager, self.slicer)

        self.main_window.set_controller(self)
        self.render_window.set_controller(self)

    def execute_main_window(self):
        self.main_window.open()

    def execute_render_window(self):
        self.render_window.open()