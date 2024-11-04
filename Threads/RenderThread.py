'''Module responsible to create the render procces thread.'''

# Libraries:
from PyQt5.QtCore import QThread # To create threads.

# Local Classes:
from time import time # To measure the time of the render process. 

class RenderThread(QThread):
    def __init__(self, slicer, file_manager):
        super().__init__()
        self.slicer = slicer
        self.file_manager = file_manager

    def run(self):
        try:
            for index, file in enumerate(self.file_manager.get_method('valid_files_list')):
                index += 1
                print(f'- CLIP {index}:')
                print(f'Name: {file}')

                # Proceso de cortar y renderizar
                cut = self.slicer.cut(self.file_manager.get_input_path(), file)
                print(f'The clip {index} has been cut!')

                start = time()  # Inicio del temporizador
                self.slicer.render(cut, (f'Sliced_{index}'), '.mp4', self.file_manager.get_output_path())
                end = time()  # Fin del temporizador
                print(f'Time: {int(end - start)} seconds.\n')

        except TypeError:
            print('Error! The directory is empty or has not valid videos.')
        except OSError:
            print('Error! The clip could not be rendered.')