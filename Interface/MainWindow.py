'''Module for the main window of the application. 
This module is responsible to create the main window of the application.'''

# Libraries:
from PyQt5.QtCore import Qt # To set the alignment of the labels.
from PyQt5.QtGui import QIcon # To set the icon.
from PyQt5.QtCore import QSize # To set the size of the icon.
from PyQt5.QtCore import pyqtSignal # To create signals.
from PyQt5.QtWidgets import QFileDialog

# Local Classes:
from Interface.Window import Window # Import Window local class.


class MainWindow(Window):

    theme_applied_signal = pyqtSignal(str)
    open_directory_signal = pyqtSignal(str)
    select_directory_signal = pyqtSignal(str)

    def __init__(self, data_json):
        super().__init__(data_json)
        self.__data_json = data_json
        self._setup_ui()

    def _setup_ui(self):
        super().window_settings((550, 350), 'SlicerInator')

        main_layout = super().main_layout_settings()
        secondary_layouts = super().create_secondary_layout(main_layout, 3)
        self.labels = []
        self.buttons = []

        lbl_title = super().label_settings((200, 60), 'SlicerInator', 'SlicerInator', font_size=20)
        secondary_layouts[0].addWidget(lbl_title, 0, 0, alignment=Qt.AlignCenter)

        btn_theme = super().button_settings((50, 50), '', 'Toggle the theme', font_size=0)
        secondary_layouts[0].addWidget(btn_theme, 0, 0, alignment=Qt.AlignRight)
        btn_theme.setIcon(QIcon('Interface/Images/theme.png'))
        btn_theme.setIconSize(QSize(42, 42))
        btn_theme.setCheckable(True)
        btn_theme.clicked.connect(self.toggle_theme)

        btn_close = super().button_settings((50, 50), '', 'Press to close the application.', font_size=0)
        secondary_layouts[0].addWidget(btn_close, 0, 0, alignment=Qt.AlignLeft)
        btn_close.setIcon(QIcon('Interface/Images/close.png'))
        btn_close.setIconSize(QSize(42, 42))
        btn_close.clicked.connect(lambda: self.close())

        lbl_input = super().label_settings((350, 50), (rf'Input │ Default'), '', font_size=10)
        secondary_layouts[1].addWidget(lbl_input, 0, 0, alignment=Qt.AlignCenter)

        lbl_output = super().label_settings((350, 50), (rf'Output │ Default'), '', font_size=10)
        secondary_layouts[1].addWidget(lbl_output, 1, 0, alignment=Qt.AlignCenter)

        btn_input = super().button_settings((50, 50), '', 'Press to open the input path.', font_size=0)
        secondary_layouts[1].addWidget(btn_input, 0, 0, alignment=Qt.AlignLeft)
        btn_input.setIcon(QIcon('Interface/Images/folder.png'))
        btn_input.setIconSize(QSize(52, 52))
        btn_input.clicked.connect(lambda: self.open_directory_signal.emit('input_path'))

        btn_output = super().button_settings((50, 50), '', 'Press to open the output path.', font_size=0)
        secondary_layouts[1].addWidget(btn_output, 1, 0, alignment=Qt.AlignLeft)
        btn_output.setIcon(QIcon('Interface/Images/folder.png'))
        btn_output.setIconSize(QSize(52, 52))
        btn_output.clicked.connect(lambda: self.open_directory_signal.emit('output_path'))

        btn_search_input = super().button_settings((50, 50), '...', 'Press to select the input path.', font_size=14)
        secondary_layouts[1].addWidget(btn_search_input, 0, 0, alignment=Qt.AlignRight)
        btn_search_input.clicked.connect(lambda: self.select_directory_signal.emit('input_path'))

        btn_search_output = super().button_settings((50, 50), '...', 'Press to select the output path.', font_size=14)
        secondary_layouts[1].addWidget(btn_search_output, 1, 0, alignment=Qt.AlignRight)
        btn_search_output.clicked.connect(lambda: self.select_directory_signal.emit('output_path'))

        btn_slice = super().button_settings((160, 50), 'SLICE NOW', 'Press to open the Render Window.', font_size=14)
        secondary_layouts[2].addWidget(btn_slice, 0, 0, alignment=Qt.AlignCenter)
        btn_slice.clicked.connect(self.close)
        btn_slice.clicked.connect(lambda: self.controller.get_render_window().open()) 

        self.labels.extend([lbl_input, lbl_output, lbl_title])
        self.buttons.extend([btn_theme, btn_close, btn_input, btn_output, btn_search_input, btn_search_output, btn_slice])

    def open(self):
        self.load_theme(self.__data_json.get('theme'))
        self.show()

    def toggle_theme(self):
        if self.__data_json.get('theme') == 'dark':
            self.__data_json['theme'] = 'light'
        else:
            self.__data_json['theme'] = 'dark'

        self.theme_applied_signal.emit(self.__data_json['theme'])

    def select_directory(self, directory:str):
        new_path = QFileDialog.getExistingDirectory(self, 'Select the directory of the clips', directory)
        if new_path:
            print(f"New path selected {new_path}")
            return new_path