'''Module responsible to show the render window.'''

# Libraries:
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtWidgets import QProgressBar # To create progress bars.

# Local Classes:
from Interface.Window import Window # Import Window local class.
from Threads.RenderThread import RenderThread # Import RenderThread local class.
from Threads.ProgressThread import ProgressThread # Import ProgressThread local class.

class RenderWindow(Window):
    def __init__(self, file_manager, slicer):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer
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

        btn_back = self.button_config('Back', 'lightblue', 'Arial', 12, tooltip_text='Back to the main window')
        btn_back.setGeometry(430, 205, 60, 35)
        btn_back.clicked.connect(self.close)
        btn_back.clicked.connect(self.stop_rendering)
        btn_back.clicked.connect(self.controller.execute_main_window)

        self.btn_toggle_delete = self.button_config('Delete: OFF', 'lightcoral', 'Arial', 12, tooltip_text='Delete original video')
        self.btn_toggle_delete.setGeometry(265, 75, 130, 35)
        self.btn_toggle_delete.setCheckable(True)
        self.btn_toggle_delete.clicked.connect(self.change_toggle_delete)


        self.show()

    def change_toggle_delete(self):
        if self.btn_toggle_delete.isChecked():
            self.btn_toggle_delete.setText('Delete: ON')
        else:
            self.btn_toggle_delete.setText('Delete: OFF')

    def info(self):
        pass

    def start_rendering(self):
        self.btn_toggle_delete.setEnabled(False)
        self.btn_start.setEnabled(False)

        # Instances of the threads
        self.render_thread = RenderThread(self.file_manager, self.slicer, self.pb_progress, self.btn_toggle_delete, self.btn_start)
        self.progress_thread = ProgressThread(self.pb_progress)

        # Connect the signals
        self.render_thread.signal_render.connect(self.update_progress)
        self.progress_thread.signal_progress.connect(self.update_progress)
        self.render_thread.signal_status.connect(self.handle_render_error)
        
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

            self.update_progress(0)

    def update_progress(self, value):
        self.pb_progress.setValue(value)
        self.pb_progress.update()

