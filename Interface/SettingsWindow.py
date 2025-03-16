# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtWidgets import QWidget # To create widgets.
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIntValidator # To validate the input.
from PyQt5.QtWidgets import QLineEdit # To create inputs.


# Local Classes:
from Logic.FileManager import FileManager # Import FileManager local class.
from Logic.Slicer import Slicer # Import Slicer local class.
from Interface.SettingsController import SettingsController # Import SettingsController local class.
from Interface.Window import Window # Import Window local class.

class SettingsWindow(Window):
    def __init__(self):
        super().__init__()
        self.file_manager = FileManager()
        self.slicer = Slicer()
        self.settings_controller = SettingsController()

    def set_controller(self, controller):
        self.controller = controller

    def open(self):
        super().window_parameters("Settings", 'lightgrey', 600, 500)
        lbl_style = "font-weight: bold; font-size: 20px;"

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # BACK:
        btn_back = self.button_config('↩️', 'lightblue', 'Arial', 20, tooltip_text='Back to the render window')
        btn_back.setGeometry(520, 460, 60, 35)
        btn_back.clicked.connect(self.close)
        btn_back.clicked.connect(lambda: self.controller.get_render_window().setDisabled(False))

        # DURATION:
        lbl_duration = super().label_config((10, 0, 100, 70), 'Duration:', tooltip='Set the duration', style=lbl_style)
        self.txt_duration = super().input_config((160, 20, 50, 30), 'int', 
        placeholder=str(self.slicer.get_duration()), 
        tooltip=f'Duration: {(self.slicer.get_duration())}')

        self.btn_set_duration = self.button_config('Set', 'lightblue', 'Arial', 10, tooltip_text='Set the duration')
        self.btn_set_duration.setGeometry(220, 20, 50, 30)
        self.btn_set_duration.setEnabled(False)
        self.btn_set_duration.clicked.connect(lambda: self.slicer.set_duration(int(self.txt_duration.text())))
        self.btn_set_duration.clicked.connect(lambda: self.show_message('Duration', 'Duration set successfully!'))
        self.btn_set_duration.clicked.connect(lambda: self.txt_duration.setPlaceholderText(str(self.slicer.get_duration())))
        self.btn_set_duration.clicked.connect(lambda: self.txt_duration.setToolTip(f'Duration: {self.slicer.get_duration()}'))
        self.txt_duration.textChanged.connect(lambda text: self.btn_set_duration.setEnabled(bool(text)))

        # CLIP LIMIT:
        lbl_clips_limit = super().label_config((300, 0, 120, 70), 'Clips limit:', tooltip='Set the clips limit', style=lbl_style)
        self.txt_clips_limit = super().input_config((420, 20, 50, 30), 'int',
        placeholder=str(self.settings_controller.get_clips_limit()),
        tooltip=f'Clips limit: {self.settings_controller.get_clips_limit()}')

        self.btn_set_clips_limit = self.button_config('Set', 'lightblue', 'Arial', 10, tooltip_text='Set the clips limit')
        self.btn_set_clips_limit.setGeometry(480, 20, 50, 30)
        self.btn_set_clips_limit.setEnabled(False)
        self.btn_set_clips_limit.clicked.connect(lambda: self.settings_controller.set_clips_limit(int(self.txt_clips_limit.text())))
        self.btn_set_clips_limit.clicked.connect(lambda: self.show_message('Clips limit', 'Clips limit set successfully!'))
        self.btn_set_clips_limit.clicked.connect(lambda: self.txt_clips_limit.setPlaceholderText(str(self.settings_controller.get_clips_limit())))
        self.btn_set_clips_limit.clicked.connect(lambda: self.txt_clips_limit.setToolTip(f'Clips limit: {self.settings_controller.get_clips_limit()}'))
        self.txt_clips_limit.textChanged.connect(lambda text: self.btn_set_clips_limit.setEnabled(bool(text)))
        

        # VIDEO TEXT POSITION:
        lbl_position = QLabel('Text position:', self)
        lbl_position.setStyleSheet("font-weight: bold; font-size: 20px;")
        lbl_position.setGeometry(10, 50, 140, 70)

        self.cb_text_position = super().combobox_config((160, 70, 120, 30), 'Set the position of video text', 
        items = ["left-bottom", "left-center", "left-top", "center-bottom", "center-center", "center-top", "right-bottom", "right-center", "right-top", 'none'])
        self.cb_text_position.currentTextChanged.connect(self.on_combobox_changed)

        # TRANSITIONS:
        lbl_transitions = super().label_config((10, 100, 180, 70), 'Transitions:', tooltip='Show transitions', style=lbl_style)
        self.chk_transitions = super().checkbox_config((200, 120, 30, 30), tooltip='Show transitions')
        self.chk_transitions.setChecked(self.settings_controller.get_show_transition())
        self.chk_transitions.stateChanged.connect(lambda: self.settings_controller.set_show_transition(self.chk_transitions.isChecked()))

        # SHOW VIDEO TEXT:
        lbl_show_overlay = super().label_config((10, 150, 180, 70), 'Overlay:', tooltip='Show overlay', style=lbl_style)
        self.chk_show_overlay = super().checkbox_config((200, 170, 40, 40), tooltip='Show overlay')
        self.chk_show_overlay.setChecked(self.settings_controller.get_show_overlay())
        self.chk_show_overlay.stateChanged.connect(lambda: self.settings_controller.set_show_overlay(self.chk_show_overlay.isChecked()))

        # PER-CLIP:
        lbl_render_per_clip = super().label_config((10, 200, 180, 70), 'Per-clip:', tooltip='Render per-clip', style=lbl_style)
        self.chk_render_per_clip = super().checkbox_config((200, 220, 40, 40), tooltip='Render per-clip')
        self.chk_render_per_clip.setChecked(self.settings_controller.get_render_per_clip())
        self.chk_render_per_clip.stateChanged.connect(lambda: self.settings_controller.set_render_per_clip(self.chk_render_per_clip.isChecked()))

        self.show()

    def on_combobox_changed(self):
        '''Method to execute when the combobox is changed.'''
        selected_text = self.cb_text_position.currentText()
        self.slicer.set_text_position(selected_text)
        print(f'current = {self.cb_text_position.currentText()}')
        print(f'get = {self.slicer.get_text_position()}')