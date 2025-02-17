'''Module for the main window of the application. 
This module is responsible to create the main window of the application and start the render thread.'''

# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.
from PyQt5.QtWidgets import QFileDialog

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

        # Path Label:
        self.lbl_path = QLabel(f"Ruta: {self.file_manager.get_input_path()}", self)
        self.lbl_path.setStyleSheet("font-weight: bold; font-size: 15px;")
        self.lbl_path.setGeometry(100, 200, 400, 70)

        # Change Path Button:
        btn_change_path = QPushButton("Change Path", self)
        btn_change_path.setStyleSheet("background-color: lightblue; font-weight: bold; font-size: 12px;")
        btn_change_path.setGeometry(0, 0, 100, 30)
        btn_change_path.clicked.connect(self.change_path)


        # Start Button:
        btn_start = QPushButton("Start", self)
        btn_start.setStyleSheet("text-align: center; lightblue; background-color: lightblue; font-weight: bold; font-size: 16px;")
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

    def change_path(self):
        '''Change the path of the clips.'''
        new_path = QFileDialog.getExistingDirectory(self, 'Select the directory of the clips')
        if new_path:
            self.file_manager.set_input_path(new_path)
            self.lbl_path.setText(f"Ruta: {self.file_manager.get_input_path()}")