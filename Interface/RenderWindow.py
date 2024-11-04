from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget
from Interface.MainWindow import MainWindow

class RenderWindow(MainWindow):
    def __init__(self):
        super().__init__()

    def render_window(self):
        super().window_parameters("Render", 500, 250, 'lightblue')
        self.show()