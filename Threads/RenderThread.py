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

    def __init__(self, file_manager, slicer, progress_bar, btn_toggle_delete, btn_go):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer
        self.progress_bar = progress_bar
        self.btn_toggle_delete = btn_toggle_delete
        self.btn_go = btn_go

    def run(self):
        '''Run the render process.'''
        try:
            path = self.file_manager.get_input_path()
            print(f'Path: {path}')
            valid_files = self.file_manager.get_method('valid_files_list')
            self.file_manager.create_output_path()
            output_path = self.file_manager.get_output_path()
            reporter = Reporter(output_path)
            clips_list = []

            for index, file in enumerate(valid_files):
                index += 1
                renamer = Renamer(file, index)
                total_disk, used_disk, free_disk = self.file_manager.get_method('disk_space')

                # -- FLOW -- #
                self.signal_render.emit(0)
                self.signal_render.emit(1)
                self.signal_processed.emit('processed', f'{index-1}/{len(valid_files)} clips processed.')
                self.signal_processed.emit('name', f'Name: {file}')

                print(f'{index-1}/{len(valid_files)} clips processed.')
                print(f'Name: {file}')

                try:
                    timer_start = time()
                    print(f'Clip {index} timer started.\n')

                    load_clip = self.slicer.load_clip(path, file)
                    print(f'The clip {index} has been loaded.\n')

                    slice_clip = self.slicer.slice_clip(load_clip)
                    print(f'The clip {index} has been sliced.\n')

                    overlay_text = self.slicer.overlay_text(slice_clip, renamer.file_name(path, file))
                    print(f'Overlay text has been added in the clip {index}.\n')

                    if index == 1: # First clip.
                        transition_fade_out = self.slicer.transition_fade_out(overlay_text)
                        print(f'Fading-out transition added in the clip {index}.\n')

                        clips_list.append(transition_fade_out)

                    elif index == (len(valid_files)): # Last clip.
                        transition_fade_in = self.slicer.transition_fade_in(overlay_text)
                        print(f'Fading-in transition added in the clip {index}.\n')

                        clips_list.append(transition_fade_in)

                    else: # Middle clips.
                        transition_fade_out = self.slicer.transition_fade_out(overlay_text)
                        print(f'Fading-out transition added in the clip {index}.\n')

                        transition_fade_in = self.slicer.transition_fade_in(transition_fade_out)
                        print(f'Fading-in transition added in the clip {index}.\n')

                        clips_list.append(transition_fade_in)

                    timer_end = time()
                    print(f'Clip {index} timer ended.\n')

                    total_time = int(timer_end - timer_start)
                    print(f'Time: {total_time} seconds.\n')

                    # Update report file.
                    reporter.file_update(clip_number=index, original_name=file, delete_original=self.btn_toggle_delete.isChecked(),
                    renamed=renamer.file_name(path, file), game=renamer.game_pattern(), date=renamer.date_pattern(path, file), 
                    time=total_time, total_disk=total_disk, used_disk=used_disk, free_disk=free_disk)
                    print(f'Report file has been updated.\n')

                except OSError as error:
                    print(f'Error! In the flow process.')
                    print(f'Error: {error}')

                    reporter.file_update(clip_number=index, original_name=file, delete_original=False,
                    renamed='Corrupt', game=None, date=None, time=None, total_disk=None, used_disk=None, free_disk=None)
                    print(f'Report corrupt file has been updated corrupt.\n')

                    continue

                try:
                    concatenate_clips = self.slicer.concatenate_clips(clips_list)
                    print(f'Clip {index} has been concatenated.\n')

                    self.slicer.render_clip(concatenate_clips, renamer.game_pattern(), output_path)
                    print(f'Clip {index} has been rendered.\n')

                except OSError as error:
                    print('Error! In the render process.')
                    print(f'Error: {error}')
                    continue

                if self.btn_toggle_delete.isChecked():
                    self.file_manager.delete_original_files(file)
                    print(f'Original file {file} has been deleted.\n')

                self.signal_render.emit(100)
                self.signal_processed.emit('hide', None)
                QThread.msleep(1000)

            self.btn_go.setEnabled(True)
            self.btn_toggle_delete.setEnabled(True)

        except TypeError as error:
            print('Error! The directory is empty or has not valid videos.')
            print(f'Error: {error}')
            self.signal_status.emit(False)

    # def run(self):
    #     try:
    #         reporter = Reporter(self.self.file_manager.get_output_path())
    #         reporter.file_creation()
            
    #         valid_files = self.self.file_manager.get_method('valid_files_list')
    #         for index, file in enumerate(valid_files):
    #             index += 1
    #             renamer = Renamer(file, index)
    #             total_files = len(valid_files)
                
    #             self.signal_render.emit(0)
    #             self.signal_render.emit(1)
    #             self.signal_processed.emit('processed', f'''{index-1}/{total_files} clips processed.''')
    #             self.signal_processed.emit('name', f'''Name: {file}''')

    #             print(f'{index-1}/{total_files} clips processed.')
    #             print(f'- CLIP {index}:')
    #             print(f'Name: {file}')

    #             try:
    #                 video_cut = self.self.slicer.cut(self.self.file_manager.get_input_path(), file)
    #                 self.signal_processed.emit('cut', f'''The clip {index} has been cut!''')
    #                 print(f'The clip {index} has been cut!')

    #                 self.signal_render.emit(self.progress_bar.value() + 15)

    #                 start = time()
    #                 file_path = join(self.self.file_manager.get_input_path() + '\\' + file) 
    #                 new_name = renamer.rename_file(file_path)
    #                 video_text = self.self.slicer.add_text(video_cut, new_name, 25, 'white')
    #                 self.self.slicer.render(video_text, (new_name), '.mp4', self.self.file_manager.get_output_path())
    #                 end = time()
    #                 total_time = int(end - start)
    #                 self.signal_processed.emit('render', f'''The clip {index} has been rendered!''')
    #                 self.signal_processed.emit('time', f'''Time: {total_time} seconds.''')
    #                 print(f'Time: {total_time} seconds.\n')

    #                 total, used, free = self.self.file_manager.get_method('disk_space')

    #                 # Update the report file.
    #                 reporter.file_update(clip_number=index, original_name=file, delete_original=self.btn_toggle_delete.isChecked(),
    #                 renamed=new_name, game=renamer.game_pattern(), date=renamer.date_pattern(file_path), 
    #                 time=total_time, total_disk=total, used_disk=used, free_disk=free)

    #                 if self.btn_toggle_delete.isChecked():
    #                     self.self.file_manager.delete_original_files(file)

    #             except OSError as error:
    #                 print(f'Error! The clip {index} could not be rendered.')
    #                 print(f'Error: {error}')
    #                 reporter.file_update(clip_number=index, original_name=file, delete_original=False,
    #                 renamed='Corrupt', game=None, date=None, time=None, total_disk=None, used_disk=None, free_disk=None)
    #                 continue

    #             self.signal_render.emit(100)

    #             self.signal_processed.emit('hide', None)
    #             QThread.msleep(1000)

    #     except TypeError as error:
    #         print('Error! The directory is empty or has not valid videos.')
    #         print(f'Error: {error}')
    #         self.signal_status.emit(False)

    #     self.btn_go.setEnabled(True)
    #     self.btn_toggle_delete.setEnabled(True)
