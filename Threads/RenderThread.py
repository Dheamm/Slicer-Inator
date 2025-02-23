'''Module responsible to create the render procces thread.'''

# Libraries:
from PyQt5.QtCore import QThread # To create threads.
from PyQt5.QtCore import pyqtSignal # Emit signals to update the progress bar.
from time import time # To measure the time of the render process.
from os.path import join # To join the paths.

# Local Classes:
from Logic.Renamer import Renamer # Import Renamer local class.
from Logic.Reporter import Reporter # Import Reporter local class.


class RenderThread(QThread):
    signal_render = pyqtSignal(int)
    signal_status = pyqtSignal(bool)
    signal_processed = pyqtSignal(str, object)

    def __init__(self, file_manager, slicer, progress_bar, btn_toggle_delete, btn_go, execute_flag=True):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer
        self.progress_bar = progress_bar
        self.btn_toggle_delete = btn_toggle_delete
        self.btn_go = btn_go

    def run(self):
        try:
            reporter = Reporter(self.file_manager.get_output_path())
            reporter.file_creation()
            
            valid_files = self.file_manager.get_method('valid_files_list')
            for index, file in enumerate(valid_files):
                index += 1
                renamer = Renamer(file, index)
                total_files = len(valid_files)
                
                self.signal_render.emit(0)
                self.signal_render.emit(1)
                self.signal_processed.emit('processed', f'''{index}/{total_files} clips processed.''')
                self.signal_processed.emit('name', f'''Name: {file}''')

                print(f'{index}/{total_files} clips processed.')
                print(f'- CLIP {index}:')
                print(f'Name: {file}')

                try:
                    cut = self.slicer.cut(self.file_manager.get_input_path(), file)

                    self.signal_processed.emit('cut', f'''The clip {index} has been cut!''')
                    print(f'The clip {index} has been cut!')

                    self.signal_render.emit(self.progress_bar.value() + 15)

                    start = time()
                    file_path = join(self.file_manager.get_input_path() + '\\' + file) 
                    new_name = renamer.rename_file(file_path)
                    self.slicer.render(cut, (new_name), '.mp4', self.file_manager.get_output_path())
                    end = time()
                    total_time = int(end - start)
                    self.signal_processed.emit('render', f'''The clip {index} has been rendered!''')
                    self.signal_processed.emit('time', f'''Time: {total_time} seconds.''')
                    print(f'Time: {total_time} seconds.\n')

                    total, used, free = self.file_manager.get_method('disk_space')

                    # Update the report file.
                    reporter.file_update(clip_number=index, original_name=file, delete_original=self.btn_toggle_delete.isChecked(),
                    renamed=new_name, game=renamer.game_pattern(), date=renamer.date_pattern(file_path), 
                    time=total_time, total_disk=total, used_disk=used, free_disk=free)



                except OSError as error:
                    print(f'Error! The clip {index} could not be rendered.')
                    print(f'Error: {error}')
                    reporter.file_update(file, 'Corrupt', 'Corrupt', 'Corrupt', index, 0)
                    self.signal_render.emit(100)
                    continue

                self.signal_render.emit(100)
                if self.btn_toggle_delete.isChecked():
                    self.file_manager.delete_original_files(file)

                self.signal_processed.emit('hide', None)
                QThread.msleep(1000)

        except TypeError as error:
            print('Error! The directory is empty or has not valid videos.')
            print(f'Error: {error}')
            self.signal_status.emit(False)

        self.btn_go.setEnabled(True)
        self.btn_toggle_delete.setEnabled(True)



