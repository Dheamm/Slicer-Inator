'''Module responsible to show the render window.'''

# Libraries:
from PyQt5.QtWidgets import QMainWindow # To create the main window.
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.
from PyQt5.QtWidgets import QProgressBar # To create progress bars.
from PyQt5.QtCore import pyqtSignal
from time import sleep # To add cooldowns in the progress bar.

# Local Classes:
from Interface.MainWindow import MainWindow # Import MainWindow local class.
from Threads.RenderThread import RenderThread # Import RenderThread local class.
from Threads.ProgressThread import ProgressThread # Import ProgressThread local class.s

class RenderWindow(MainWindow):
    def __init__(self, file_manager, slicer):
        super().__init__(file_manager, slicer)

    def render_window(self):
        super().window_parameters('Render', 'lightblue', 500, 250)

        # Title Label:
        lbl_title = QLabel('Render', self)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        lbl_title.setGeometry(200, 20, 100, 70)

        # Progress Bar:
        self.pb_progress = QProgressBar(self)
        self.pb_progress.setGeometry(100, 100, 300, 50)
        self.pb_progress.setRange(0, 100)

        self.start_rendering()

        self.show()

    def start_rendering(self):
        # Instances of the threads
        self.render_thread = RenderThread(self.file_manager, self.slicer, self.pb_progress)
        self.progress_thread = ProgressThread(self.pb_progress)

        # Connect the signals
        self.render_thread.signal_render.connect(self.update_progress)
        self.progress_thread.signal_progress.connect(self.update_progress)
        
        # Start the threads
        self.render_thread.start()
        self.progress_thread.start()

    def update_progress(self, value):
        self.pb_progress.setValue(value)