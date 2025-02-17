'''Module responsible to create the render procces thread.'''

# Libraries:
from PyQt5.QtCore import QThread # To create threads.
from PyQt5.QtCore import pyqtSignal # Emit signals to update the progress bar.
from time import time # To measure the time of the render process.
from time import sleep # To add cooldowns in the progress bar.
from os.path import join # To join the paths.

# Local Classes:
from Logic.Renamer import Renamer # Import Renamer local class.
from Logic.Reporter import Reporter # Import Reporter local class.


class RenderThread(QThread):
    signal_render = pyqtSignal(int)

    def __init__(self, file_manager, slicer, progress_bar, execute_flag=True):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer
        self.progress_bar = progress_bar

    def run(self):
        try:
            reporter = Reporter(self.file_manager.get_output_path())
            reporter.file_creation()
            for index, file in enumerate(self.file_manager.get_method('valid_files_list')):
                index += 1
                renamer = Renamer(file, index)

                self.signal_render.emit(0)
                self.signal_render.emit(1)

                print(f'- CLIP {index}:')
                print(f'Name: {file}')
                # Proceso de cortar y renderizar
                cut = self.slicer.cut(self.file_manager.get_input_path(), file)
                print(f'The clip {index} has been cut!')
                self.signal_render.emit(self.progress_bar.value() + 15)

                start = time()
                file_path = join(self.file_manager.get_input_path() + '\\' + file) 
                new_name = renamer.rename_file(file_path)
                self.slicer.render(cut, (new_name), '.mp4', self.file_manager.get_output_path())
                end = time()
                total_time = int(end - start)
                print(f'Time: {total_time} seconds.\n')

                reporter.file_update(file, new_name, renamer.game_pattern(), renamer.date_pattern(file_path), index, total_time)

                self.signal_render.emit(100)
                sleep(2)

        except TypeError as error:
            print('Error! The directory is empty or has not valid videos.')
            print(f'Error: {error}')
        except OSError as error:
            print('Error! The clip could not be rendered.')
            print(f'Error: {error}')


