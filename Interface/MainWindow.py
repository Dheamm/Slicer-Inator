'''Module for the main window of the application. 
This module is responsible to create the main window of the application and start the render thread.'''

# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.

# Local Classes:
from Interface.Window import Window # Import Window local class.

class MainWindow(Window):
    def __init__(self, file_manager, slicer):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer

    def set_controller(self, controller):
        self.controller = controller

    def open(self):
        super().window_parameters("Slicer Inator", 'lightgrey', 500, 250)

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
        btn_start.clicked.connect(self.close) # Hide last window.
        btn_start.clicked.connect(self.controller.execute_render_window) # Start the new window.
        # btn_start.clicked.connect(self.start_render_thread)

        # Exit Button:
        btn_exit = QPushButton("Exit", self)
        btn_exit.setStyleSheet("background-color: lightcoral; font-weight: bold; font-size: 16px;")
        btn_exit.setGeometry(230, 160, 50, 30)
        btn_exit.clicked.connect(self.close)

        self.show() # Show the window