'''Module for the main window of the application. 
This module is responsible to create the main window of the application and start the render thread.'''

# Libraries:
from PyQt5.QtWidgets import QMainWindow # To create the main window.
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.

class MainWindow(QMainWindow):
    def __init__(self, file_manager, slicer):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer

    def window_parameters(self, title, color, width=500, height=250):
        '''Set the window parameters.'''
        self.setWindowTitle(title) # Set the window title
        self.setFixedSize(width, height) # Set fixed size
        self.setStyleSheet(f"background-color: {color};")

    def main_window(self, new_window):
        self.window_parameters("Slicer Inator", 'lightgrey', 500, 250)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)      

        # Title Label:
        lbl_title = QLabel("Slicer Inator", self) # Create a label
        lbl_title.setStyleSheet("font-weight: bold; font-size: 30px;") # Set the label style
        lbl_title.setGeometry(160, 20, 200, 70)

        # Start Button:
        btn_start = QPushButton("Start", self)
        btn_start.setStyleSheet("background-color: lightblue; font-weight: bold; font-size: 16px;")
        btn_start.setGeometry(155, 100, 200, 50)
        btn_start.clicked.connect(self.hide) # Hide last window.
        btn_start.clicked.connect(new_window) # Start the new window.
        # btn_start.clicked.connect(self.start_render_thread)

        # Exit Button:
        btn_exit = QPushButton("Exit", self)
        btn_exit.setStyleSheet("background-color: lightcoral; font-weight: bold; font-size: 16px;")
        btn_exit.setGeometry(230, 160, 50, 30)
        btn_exit.clicked.connect(self.close)

        self.show() # Show the window