from PyQt5.QtCore import QThread # To create threads.
from PyQt5.QtCore import pyqtSignal # Emit signals to update the progress bar.
from time import sleep # To add cooldowns in the progress bar.

class ProgressThread(QThread):
    signal_progress = pyqtSignal(int)
    
    def __init__(self, progress_bar):
        super().__init__()
        self.progress_bar = progress_bar

    def run(self):
        while True:
            current_value = self.progress_bar.value()
            if current_value < 99:
                self.signal_progress.emit(current_value + 1)
                sleep(0.5)