'''Module responsible to create the render procces thread.'''

# Libraries:
from PyQt5.QtCore import QThread # To create threads.
from PyQt5.QtCore import pyqtSignal # Emit signals to update the progress bar.
from time import time # To measure the time of the render process.
from time import sleep # To add cooldowns in the progress bar.
from os.path import join # To join the paths.

# Local Classes:
from Logic.Renamer import Renamer # Import Renamer local class.


class RenderThread(QThread):
    signal_render = pyqtSignal(int)

    def __init__(self, file_manager, slicer, progress_bar, execute_flag=True):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer
        self.progress_bar = progress_bar

    def run(self):
        try:
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
                self.slicer.render(cut, (renamer.rename_file(file_path)), '.mp4', self.file_manager.get_output_path())
                end = time()
                print(f'Time: {int(end - start)} seconds.\n')

                self.signal_render.emit(100)
                sleep(2)

        except TypeError:
            print('Error! The directory is empty or has not valid videos.')
        except OSError:
            print('Error! The clip could not be rendered.')

