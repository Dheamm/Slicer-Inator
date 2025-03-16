from proglog import ProgressBarLogger

class BarLogger(ProgressBarLogger):

    def __init__(self, signal_progress_logger, signal_status_logger):
        super().__init__()
        self.signal_progress_logger = signal_progress_logger
        self.signal_status_logger = signal_status_logger

    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        percentage = int((value / self.bars[bar]['total']) * 100)
        self.signal_progress_logger.emit(percentage) # Send the percentage to the progress bar.
        self.signal_status_logger.emit(int(value), int(self.bars[bar]['total']))
        # print(f'{percentage} %')
        # print(f'{value} / {self.bars[bar]["total"]}\n')