# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIntValidator # To validate the input.


# Local Classes:
from Interface.Window import Window # Import Window local class.

class SettingsWindow(Window):
    def __init__(self, file_manager, slicer):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer

    def set_controller(self, controller):
        self.controller = controller

    def open(self):
        super().window_parameters("Settings", 'lightgrey', 300, 150)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)      

        # Title Label:
        # lbl_title = QLabel('Settings', self)
        # lbl_title.setStyleSheet("font-weight: bold; font-size: 30px;")
        # lbl_title.setGeometry(100, 0, 150, 70)

        btn_back = self.button_config('↩️', 'lightblue', 'Arial', 20, tooltip_text='Back to the render window')
        btn_back.setGeometry(120, 110, 60, 35)
        btn_back.clicked.connect(self.close)
        btn_back.clicked.connect(self.controller.execute_render_window)

        # Duration Label:
        lbl_duration = QLabel('Duration:', self)
        lbl_duration.setStyleSheet("font-weight: bold; font-size: 20px;")
        lbl_duration.setGeometry(50, 0, 100, 70)

        # Duration Input:
        self.txt_duration = QLineEdit(self)
        self.txt_duration.setValidator(QIntValidator())
        self.txt_duration.setGeometry(150, 20, 50, 30)
        self.txt_duration.setStyleSheet("background-color: white; color: black; border: 1px solid black; border-radius: 5px;")
        self.txt_duration.setPlaceholderText(str(self.slicer.get_duration()))
        self.txt_duration.setToolTip(f'Duration: {self.slicer.get_duration()}')

        # Set Duration Button:
        self.btn_set_duration = self.button_config('Set', 'lightblue', 'Arial', 10, tooltip_text='Set the duration')
        self.btn_set_duration.setGeometry(210, 20, 50, 30)
        self.btn_set_duration.setEnabled(False)
        self.btn_set_duration.clicked.connect(lambda: self.slicer.set_duration(int(self.txt_duration.text())))
        self.btn_set_duration.clicked.connect(lambda: self.show_message('Duration', 'Duration set successfully!'))
        self.btn_set_duration.clicked.connect(lambda: self.txt_duration.setPlaceholderText(str(self.slicer.get_duration())))
        self.btn_set_duration.clicked.connect(lambda: self.txt_duration.setToolTip(f'Duration: {self.slicer.get_duration()}'))

        self.txt_duration.textChanged.connect(self.check_input)

        self.show()

    def check_input(self, input):
        '''Check if the input is valid.'''
        if input.isdigit():
            self.btn_set_duration.setEnabled(True)
        else:
            self.btn_set_duration.setEnabled(False)
