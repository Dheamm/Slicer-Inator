'''Module for the main window of the application. 
This module is responsible to create the render window of the application and start the render thread.'''

# Libraries:
from PyQt5.QtCore import Qt # To set the alignment of the labels.
from PyQt5.QtGui import QIcon # To set the icon.
from PyQt5.QtCore import QSize # To set the size of the icon.
from PyQt5.QtCore import pyqtSignal # To create signals.
from PyQt5.QtCore import QTime 
from PyQt5.QtCore import QTimer # To create a timer.

# Local Classes:
from Interface.Window import Window # Import Window local class

class RenderWindow(Window):

    start_rendering_signal = pyqtSignal(bool)
    stop_rendering_signal = pyqtSignal(bool)

    def __init__(self, data_json):
        super().__init__(data_json)
        self.__data_json = data_json
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_message)
        self.seconds_timer = 0

        self._setup_ui()

    def _setup_ui(self):
        super().window_settings((550, 450), 'SlicerInator - Render')
        self.setWindowIcon(QIcon('Interface/Images/play.png'))

        # Layouts:
        main_layout = super().main_layout_settings()
        secondary_layouts = super().create_secondary_layout(main_layout, 4)

        self.btn_back = super().button_settings((50, 50), '', 'Press to go back to the main window.', font_size=0)
        secondary_layouts[0].addWidget(self.btn_back, 0, 0, alignment=Qt.AlignCenter)
        self.btn_back.setIcon(QIcon('Interface/Images/back.png'))
        self.btn_back.setIconSize(QSize(42, 42))
        self.btn_back.clicked.connect(lambda: self.close())
        self.btn_back.clicked.connect(lambda: self.controller.get_main_window().open())

        lbl_title = super().label_settings((350, 65), 'SlicerInator - Render', 'SlicerInator - Render', font_size=20)
        secondary_layouts[0].addWidget(lbl_title, 0,  1, alignment=Qt.AlignCenter)

        self.btn_settings = super().button_settings((50, 50), '', 'Open the settings window.', font_size=0)
        secondary_layouts[0].addWidget(self.btn_settings, 0, 2, alignment=Qt.AlignCenter)
        self.btn_settings.setIcon(QIcon('Interface/Images/settings.png'))
        self.btn_settings.setIconSize(QSize(42, 42))
        self.btn_settings.clicked.connect(lambda: self.setEnabled(False))
        self.btn_settings.clicked.connect(lambda: self.controller.get_settings_window().open())

        self.progress_bar = super().progress_bar_settings((400, 60), 'Render Progress')
        secondary_layouts[1].addWidget(self.progress_bar, 0,  0, alignment=Qt.AlignCenter)

        self.lbl_status_logger = super().label_settings((200, 50), '0 / 0', 'Status Logger', font_size=12)
        secondary_layouts[1].addWidget(self.lbl_status_logger, 1, 0, alignment=Qt.AlignCenter)
        self.lbl_status_logger.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.lbl_time = super().label_settings((200, 50), 'Time : 00:00:00', 'Time Elapsed', font_size=12)
        secondary_layouts[2].addWidget(self.lbl_time, 0, 0, alignment=Qt.AlignLeft)
        self.lbl_time.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.lbl_archive_count = super().label_settings((200, 50), 'Archives 0 / 0', 'Archive Count', font_size=12)
        secondary_layouts[2].addWidget(self.lbl_archive_count, 0, 0, alignment=Qt.AlignRight)
        self.lbl_archive_count.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.lbl_status_message = super().label_settings((470, 50), 'Status: None', 'Status Message', font_size=12)
        secondary_layouts[2].addWidget(self.lbl_status_message, 1, 0, alignment=Qt.AlignCenter)
        self.lbl_status_message.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.btn_start = super().button_settings((160, 50), 'Start', 'Press to start to render.', font_size=14)
        secondary_layouts[3].addWidget(self.btn_start, 0, 0, alignment=Qt.AlignCenter)
        self.btn_start.setIcon(QIcon('Interface/Images/play.png'))
        self.btn_start.setIconSize(QSize(42, 42))
        self.btn_start.clicked.connect(self.start_pressed)


        self.btn_stop = super().button_settings((160, 50), 'Stop', 'Press to stop the render.', font_size=14)
        secondary_layouts[3].addWidget(self.btn_stop, 0, 1, alignment=Qt.AlignCenter)
        self.btn_stop.setIcon(QIcon('Interface/Images/stop.png'))
        self.btn_stop.setIconSize(QSize(42, 42))
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_pressed)


    def open(self):
        self.load_theme(self.__data_json.get('theme'))
        self.show()

    def start_pressed(self):
        self.btn_start.setEnabled(False)
        self.btn_settings.setEnabled(False)
        self.btn_back.setEnabled(False)
        self.btn_stop.setEnabled(True)

        self.progress_bar.setTextVisible(True)

        self.start_rendering_signal.emit(True)

    def stop_pressed(self):
        self.btn_start.setEnabled(True)
        self.btn_settings.setEnabled(True)
        self.btn_back.setEnabled(True)

        self.progress_bar.setTextVisible(False)
        self.update_progress_bar(0)

        self.update_status_logger(0,0)
        self.lbl_time.setText("00:00:00")
        self.update_archive_count(0,0)
        self.update_status_message("Status: None")

        self.stop_rendering_signal.emit(True)

    def update_progress_bar(self, value: int):
        """Update the progress bar with the given value."""
        self.progress_bar.setValue(value)
        self.progress_bar.update()

    def update_status_logger(self, curren_value: int, total_value: int):
        self.lbl_status_logger.setText(f'{curren_value} / {total_value}')
        self.lbl_status_logger.update()
    
    def timer_start(self):
        """Start the timer."""
        self.seconds_timer = 0
        self.timer.start(1000)

    def timer_stop(self):
        """Stop the timer and reset the seconds."""
        self.timer.stop()

    # def timer_switch(self, state: bool):
    #     """Switch the timer state."""
    #     if state:
    #         self.timer.start(1000)  # Start the timer with a 1 second interval
    #     else:
    #         self.timer.stop()
    #         self.lbl_time.setText('Time : 00:00:00')
    #         self.seconds_timer = 0

    def update_time_message(self):
        """Update the time label with the given seconds."""
        self.seconds_timer += 1
        tiempo = QTime(0, 0).addSecs(self.seconds_timer)
        self.lbl_time.setText(f'Time : {tiempo.toString("hh:mm:ss")}')
        self.lbl_time.update()

    def update_archive_count(self, current: int, total: int):
        """Update the archive count label with the current and total values."""
        self.lbl_archive_count.setText(f'Archives {current} / {total}')
        self.lbl_archive_count.update()

    def update_status_message(self, message: str):
        """Update the status message label."""
        self.lbl_status_message.setText(message)
        self.lbl_status_message.update()