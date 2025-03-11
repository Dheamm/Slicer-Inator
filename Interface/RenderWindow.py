'''Module responsible to show the render window.'''

# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QProgressBar # To create progress bars.
from PyQt5.QtCore import QThread # To create threads.

# Local Classes:
from Logic.FileManager import FileManager # Import FileManager local class.
from Logic.Slicer import Slicer # Import Slicer local class.
from Interface.Window import Window # Import Window local class.
from Threads.RenderThread import RenderThread # Import RenderThread local class.
from Threads.ProgressThread import ProgressThread # Import ProgressThread local class.

class RenderWindow(Window):
    def __init__(self):
        super().__init__()
        self.file_manager = FileManager()
        self.slicer = Slicer()
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
        self.pb_progress.setStyleSheet("border: 2px solid #2196F3; border-radius: 5px; background-color: #E0E0E0;")

        # Buttons:
        self.btn_start = self.button_config('▶', 'green', 'Arial', 30, tooltip_text='Start')
        self.btn_start.setGeometry(105, 75, 35, 35)
        self.btn_start.clicked.connect(self.start_rendering)

        btn_stop = self.button_config('⬛', 'lightcoral', 'Arial', 15, tooltip_text='Stop', style='padding-top: 0px; padding-bottom: 2px; padding-left: 0.4px;')
        btn_stop.setGeometry(145, 75, 35, 35)
        btn_stop.clicked.connect(self.stop_rendering)

        btn_back = self.button_config('↩️', 'lightblue', 'Arial', 20, tooltip_text='Back to the main window')
        btn_back.setGeometry(430, 205, 60, 35)
        btn_back.clicked.connect(self.close)
        btn_back.clicked.connect(self.stop_rendering)
        btn_back.clicked.connect(self.controller.execute_main_window)

        self.btn_settings = self.button_config('⚙️', 'lightblue', 'Arial', 14, tooltip_text='Settings', style='padding-top: 0px; padding-bottom: 4px;')
        self.btn_settings.setGeometry(430, 165, 60, 35)
        self.btn_settings.clicked.connect(self.close)
        self.btn_settings.clicked.connect(self.controller.execute_settings_window)

        self.btn_toggle_delete = self.button_config('Delete: OFF', 'lightcoral', 'Arial', 12, tooltip_text='Delete original video')
        self.btn_toggle_delete.setGeometry(265, 75, 130, 35)
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

        # Instances of the threads
        self.render_thread = RenderThread(self.file_manager, self.slicer, self.pb_progress, self.btn_toggle_delete, self.btn_start)
        self.progress_thread = ProgressThread(self.pb_progress)

        # Connect the signals
        self.render_thread.signal_render.connect(self.update_progress)
        self.progress_thread.signal_progress.connect(self.update_progress)
        self.render_thread.signal_status.connect(self.handle_render_error)
        self.render_thread.signal_processed.connect(self.update_info)
        
        # Start the threads
        self.render_thread.start()
        self.progress_thread.start()

    def handle_render_error(self):
        print("Error! Stopping ProgressThread.")
        self.stop_rendering()

    def stop_rendering(self):
        if self.render_thread and self.progress_thread is not None:
            self.render_thread.terminate()
            self.progress_thread.terminate()

        self.btn_toggle_delete.setEnabled(True)
        self.btn_start.setEnabled(True)
        self.btn_settings.setEnabled(True)
        self.lbl_processed.hide()
        self.lbl_name.hide()
        self.lbl_status.hide()
        self.lbl_time.hide()

        self.update_progress(-1)

        self.file_manager.close_ffmpeg_process()
        QThread.msleep(100) # Wait for the process to close.
        self.file_manager.delete_temp_files()

    def update_progress(self, value):
        self.pb_progress.setValue(value)
        self.pb_progress.update()

    def update_info(self, info_type, text):
        '''Update the information of the render window.'''
        if info_type == 'processed':
            self.lbl_processed.setText(text)
            self.lbl_processed.show()

        elif info_type == 'name':
            self.lbl_name.setText(text)
            self.lbl_name.setToolTip(text)
            self.lbl_name.show()

        elif info_type == 'render' or info_type == 'cut':
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

