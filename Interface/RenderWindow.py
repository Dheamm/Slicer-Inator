'''Module responsible to show the render window.'''

# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.
from PyQt5.QtWidgets import QProgressBar # To create progress bars.

# Local Classes:
from Interface.MainWindow import MainWindow # Import MainWindow local class.

class RenderWindow(MainWindow):
    def __init__(self, file_manager, slicer):
        super().__init__(file_manager, slicer)

    def render_window(self):
        super().window_parameters("Render", 500, 250, 'lightblue')
        
        # Title Label:
        lbl_title = QLabel('Render', self)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        lbl_title.setGeometry(200, 20, 100, 70)

        # Progress Bar:
        self.pb_progress = QProgressBar(self)
        self.pb_progress.setGeometry(100, 100, 300, 50)
        self.pb_progress.setValue(0)

        self.show()