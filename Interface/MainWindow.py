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
        lbl_title.setStyleSheet("font-weight: bold; font-size: 40px;") # Set the label style
        lbl_title.setGeometry(130, 30, 300, 70)

        # Path Label:
        self.lbl_path = QLabel(f"Ruta: {self.file_manager.get_input_path()}", self)
        self.lbl_path.setStyleSheet("font-weight: bold; font-size: 15px;")
        self.lbl_path.setGeometry(100, 200, 400, 70)

        # Change Path Button:
        btn_change_path = super().button_config("Change Path", "lightblue", "Arial", 8, tooltip_text="Change the path of the clips")
        btn_change_path.setGeometry(0, 0, 100, 30)
        btn_change_path.clicked.connect(self.change_path)

        # Open Path Button:
        btn_open_input_path = super().button_config("Input Path", "lightblue", "Arial", 8, tooltip_text="Open the input path")
        btn_open_input_path.setGeometry(100, 0, 100, 30)
        btn_open_input_path.clicked.connect(lambda: self.file_manager.open_directory(self.file_manager.get_input_path()))

        # Open Output Path Button:
        btn_open_output_path = super().button_config("Output Path", "lightblue", "Arial", 8, tooltip_text="Open the output path")
        btn_open_output_path.setGeometry(200, 0, 100, 30)
        btn_open_output_path.clicked.connect(lambda: self.file_manager.open_directory(self.file_manager.get_output_path()))

        # Slice Button:
        btn_slice = super().button_config("Slice", "lightblue", "Arial", 16, tooltip_text="Go to the render window")
        btn_slice.setGeometry(155, 100, 200, 50)
        btn_slice.clicked.connect(self.close) # Hide last window.
        btn_slice.clicked.connect(self.controller.execute_render_window) # Start the new window.
        # btn_slice.clicked.connect(self.start_render_thread)

        # Exit Button:
        btn_exit = super().button_config("Exit", "lightcoral", "Arial", 12, tooltip_text="Exit the application")
        btn_exit.setGeometry(230, 160, 50, 30)
        btn_exit.clicked.connect(self.close)

        self.show() # Show the window

    def change_path(self):
        '''Change the path of the clips.'''
        new_path = QFileDialog.getExistingDirectory(self, 'Select the directory of the clips', self.file_manager.get_input_path())
        if new_path:
            self.file_manager.set_input_path(new_path)
            self.lbl_path.setText(f"Ruta: {self.file_manager.get_input_path()}")
