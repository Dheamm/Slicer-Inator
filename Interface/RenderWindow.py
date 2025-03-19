'''Module responsible to show the render window.'''

# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QProgressBar # To create progress bars.
from PyQt5.QtCore import QThread # To create threads.

# Local Classes:
from Logic.FileManager import FileManager # Import FileManager local class.
from Logic.Slicer import Slicer # Import Slicer local class.
from Interface.SettingsController import SettingsController # Import SettingsController local class.
from Interface.Window import Window # Import Window local class.
from Threads.RenderThread import RenderThread # Import RenderThread local class.
from Logic.BarLogger import BarLogger # Import BarLogger local class.

class RenderWindow(Window):
    def __init__(self):
        super().__init__()
        self.file_manager = FileManager()
        self.slicer = Slicer()
        self.settings_controller = SettingsController()
        self.render_thread = None
        self.progress_thread = None

    def set_controller(self, controller):
        self.controller = controller

    def open(self):
        super().window_parameters('Render', 'lightgrey', 500, 250)

        # Title Label:
        # lbl_title = QLabel('Render', self)
        # lbl_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        # lbl_title.setGeometry(200, 20, 100, 70)

        # Progress Bar:
        self.pb_progress = QProgressBar(self)
        self.pb_progress.setGeometry(100, 20, 300, 50)
        self.pb_progress.setRange(0, 100)
        # self.pb_progress.setStyleSheet("border: 2px solid black; border-radius: 5px; background-color: #E0E0E0;")
        self.pb_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid black;
                border-radius: 5px;
                background-color: #E0E0E0;
                text-align: center;
                font-weight: bold;
                font-size: 16px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)

        self.lbl_status_logger = super().label_config((402, 60, 100, 10), '0 / 0', tooltip='Status', style='font-weight: bold; font-size: 10px;')
        self.lbl_status_logger.hide()

        # Buttons:
        self.btn_start = self.button_config((105, 75, 35, 35), '▶', '#90CFA0', 'Arial', 30, tooltip_text='Start', style='border-radius: 17.5px; border: 2px solid #388E3C;')
        self.btn_start.clicked.connect(self.start_rendering)

        btn_stop = self.button_config((145, 75, 35, 35), '⬛', 'lightcoral', 'Arial', 15, tooltip_text='Stop', style='padding-top: 0px; padding-bottom: 2px; padding-left: 0.4px;')
        btn_stop.clicked.connect(self.stop_rendering)

        btn_back = self.button_config((430, 205, 60, 35), '↩️', '#ADD8E6', 'Arial', 20, tooltip_text='Back to the main window')
        btn_back.clicked.connect(self.close)
        btn_back.clicked.connect(self.stop_rendering)
        btn_back.clicked.connect(lambda: self.controller.get_main_window().open())

        self.btn_settings = self.button_config((430, 165, 60, 35), '⚙️', 'lightblue', 'Arial', 14, tooltip_text='Settings', style='padding-top: 0px; padding-bottom: 4px;')
        self.btn_settings.clicked.connect(lambda: self.setDisabled(True))
        self.btn_settings.clicked.connect(lambda: self.controller.get_settings_window().open())

        self.btn_toggle_delete = self.button_config((265, 75, 130, 35), 'Delete: OFF', 'lightcoral', 'Arial', 12, tooltip_text='Delete original video')
        self.btn_toggle_delete.setCheckable(True)
        self.btn_toggle_delete.clicked.connect(self.change_toggle_delete)

        self.lbl_processed = QLabel(f'{0}/{0} clips processed.', self)
        self.lbl_processed.setStyleSheet("font-size: 20px;")
        self.lbl_processed.setGeometry(50, 120, 200, 30)
        self.lbl_processed.hide()

        self.lbl_name = QLabel(f'Name: {None}', self)
        self.lbl_name.setStyleSheet("font-size: 20px;")
        self.lbl_name.setGeometry(50, 150, 350, 30)
        self.lbl_name.hide()

        self.lbl_status = QLabel(f'The clip {0} has been rendered!', self)
        self.lbl_status.setStyleSheet("font-size: 20px;")
        self.lbl_status.setGeometry(50, 180, 350, 30)
        self.lbl_status.hide()

        self.lbl_time = QLabel(f'Time: {0} seconds.', self)
        self.lbl_time.setStyleSheet("font-size: 20px;")
        self.lbl_time.setGeometry(50, 210, 200, 30)
        self.lbl_time.hide()

        self.show()

    def change_toggle_delete(self):
        if self.btn_toggle_delete.isChecked():
            self.btn_toggle_delete.setText('Delete: ON')
        else:
            self.btn_toggle_delete.setText('Delete: OFF')

    def start_rendering(self):
        self.btn_toggle_delete.setEnabled(False)
        self.btn_start.setEnabled(False)
        self.btn_settings.setEnabled(False)
        self.lbl_status_logger.show()

        # Instances of the threads
        self.render_thread = RenderThread(self.file_manager, self.slicer, self.settings_controller, self.btn_toggle_delete, self.btn_start)

        # Connect the signals
        self.render_thread.signal_progress_logger.connect(self.update_progress) # Percentage of the progress bar.
        self.render_thread.signal_status_logger.connect(self.update_status_logger) # Status logger of the progress bar.
        self.render_thread.signal_status.connect(self.handle_render_error)
        self.render_thread.signal_processed.connect(self.update_info)
        
        # Start the threads
        self.render_thread.start()

    def handle_render_error(self):
        print("Error! Stopping ProgressThread.")
        self.stop_rendering()

    def stop_rendering(self):
        if self.render_thread is not None:
            self.render_thread.terminate()

        self.btn_toggle_delete.setEnabled(True)
        self.btn_start.setEnabled(True)
        self.btn_settings.setEnabled(True)
        self.lbl_processed.hide()
        self.lbl_name.hide()
        self.lbl_status.hide()
        self.lbl_time.hide()
        self.lbl_status_logger.hide()

        self.update_progress(-1)

        self.file_manager.close_ffmpeg_process()
        QThread.msleep(100) # Wait for the process to close.
        self.file_manager.delete_temp_files()

    def update_progress(self, value):
        self.pb_progress.setValue(value)
        self.pb_progress.update()

    def update_status_logger(self, curren_value, total_value):
        self.lbl_status_logger.setText(f'{curren_value} / {total_value}')

    def update_info(self, info_type, text):
        '''Update the information of the render window.'''
        if info_type == 'processed':
            self.lbl_processed.setText(text)
            self.lbl_processed.show()

        elif info_type == 'name':
            self.lbl_name.setText(text)
            self.lbl_name.setToolTip(text)
            self.lbl_name.show()

        elif info_type == 'status':
            self.lbl_status.setText(text)
            self.lbl_status.setToolTip(text)
            self.lbl_status.show()

        elif info_type == 'time':
            self.lbl_time.setText(text)
            self.lbl_time.show()

        elif info_type == 'hide':
            self.lbl_name.hide()
            self.lbl_status.hide()
            self.lbl_time.hide()
