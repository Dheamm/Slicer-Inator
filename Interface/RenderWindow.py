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

    def set_controller(self, controller):
        self.controller = controller

    def open(self):
        super().window_parameters('Render', 'lightblue', 500, 250)

        # Title Label:
        lbl_title = QLabel('Render', self)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        lbl_title.setGeometry(200, 20, 100, 70)

        # Progress Bar:
        self.pb_progress = QProgressBar(self)
        self.pb_progress.setGeometry(100, 100, 300, 50)
        self.pb_progress.setRange(0, 100)

        # Buttons:
        btn_go = self.button_config('▶', 'green', 'Arial', 30, tooltip_text='Go')
        btn_go.setGeometry(100, 160, 30, 30)

        btn_stop = self.button_config('■', 'lightcoral', 'Arial', 30, tooltip_text='Stop')
        btn_stop.setGeometry(155, 160, 30, 30)

        btn_exit = self.button_config('Exit', 'lightcoral', 'Arial', 12, tooltip_text='Exit')
        btn_exit.setGeometry(210, 160, 50, 30)
        btn_exit.clicked.connect(self.close)
        btn_exit.clicked.connect(self.controller.execute_main_window)


        # self.start_rendering()

        self.show()

    def start_rendering(self):
        # Instances of the threads
        self.render_thread = RenderThread(self.file_manager, self.slicer, self.pb_progress)
        self.progress_thread = ProgressThread(self.pb_progress)

        # Connect the signals
        self.render_thread.signal_render.connect(self.update_progress)
        self.progress_thread.signal_progress.connect(self.update_progress)
        
        # Start the threads
        self.render_thread.start()
        self.progress_thread.start()

    def update_progress(self, value):
        self.pb_progress.setValue(value)