# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIntValidator # To validate the input.
from PyQt5.QtWidgets import QLineEdit # To create inputs.


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
        super().window_parameters("Settings", 'lightgrey', 300, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)      

        # Title Label:
        # lbl_title = QLabel('Settings', self)
        # lbl_title.setStyleSheet("font-weight: bold; font-size: 30px;")
        # lbl_title.setGeometry(100, 0, 150, 70)

        btn_back = self.button_config('↩️', 'lightblue', 'Arial', 20, tooltip_text='Back to the render window')
        btn_back.setGeometry(120, 160, 60, 35)
        btn_back.clicked.connect(self.close)
        btn_back.clicked.connect(self.controller.execute_render_window)

        # Duration Label:
        lbl_duration = QLabel('Duration:', self)
        lbl_duration.setStyleSheet("font-weight: bold; font-size: 20px;")
        lbl_duration.setGeometry(10, 0, 100, 70)

        # Duration Input:
        self.txt_duration = super().input_config((160, 20, 50, 30), 'int', 
        placeholder=str(self.slicer.get_duration()), 
        tooltip=f'Duration: {(self.slicer.get_duration())}')

        lbl_position = QLabel('Text position:', self)
        lbl_position.setStyleSheet("font-weight: bold; font-size: 20px;")
        lbl_position.setGeometry(10, 50, 140, 70)

        # Position ComboBox:
        self.cb_text_position = super().combobox_config((160, 70, 120, 30), 'Set the position of video text', 
        items = ["left-bottom", "left-center", "left-top", "center-bottom", "center-center", "center-top", "right-bottom", "right-center", "right-top", 'none'])
        self.cb_text_position.currentTextChanged.connect(self.on_combobox_changed)

        # Set Duration Button:
        self.btn_set_duration = self.button_config('Set', 'lightblue', 'Arial', 10, tooltip_text='Set the duration')
        self.btn_set_duration.setGeometry(220, 20, 50, 30)
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

    def on_combobox_changed(self):
        '''Method to execute when the combobox is changed.'''
        selected_text = self.cb_text_position.currentText()
        self.slicer.set_text_position(selected_text)
        print(f'current = {self.cb_text_position.currentText()}')
        print(f'get = {self.slicer.get_text_position()}')