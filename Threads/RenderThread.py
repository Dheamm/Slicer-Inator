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

    def __init__(self, file_manager, slicer, settings_controller, progress_bar, btn_toggle_delete, btn_go):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer
        self.settings_controller = settings_controller
        self.progress_bar = progress_bar
        self.btn_toggle_delete = btn_toggle_delete
        self.btn_go = btn_go

    def show_status(self, status:str):
        '''Show the status info and send to the render window.'''
        self.signal_processed.emit('status', status)
        print(status)

    def run(self):
        '''Run the render process.'''
        try:
            path = self.file_manager.get_input_path()
            valid_files = self.file_manager.get_method('valid_files_list')
            self.file_manager.create_output_path()
            output_path = self.file_manager.get_output_path()
            reporter = Reporter(output_path)
            reporter.file_creation()
            clips_list = []
            errors = 0

            for index, file in enumerate(valid_files):
                index += 1
                renamer = Renamer(file, index)
                total_disk, used_disk, free_disk = self.file_manager.get_method('disk_space')

                # -- FLOW -- #
                self.signal_render.emit(0)
                self.signal_render.emit(1)
                self.signal_processed.emit('name', f'Name: {file}')
                if index == 1:
                    self.signal_processed.emit('processed', f'{0}/{len(valid_files)} clips processed.')
                    print(f'{0}/{len(valid_files)} clips processed.')
                print(f'Name: {file}')

                try:
                    timer_start = time()
                    self.show_status(f'Clip {index} timer started.')

                    # LOAD
                    load_clip = self.slicer.load_clip(path, file)
                    self.show_status(f'The clip {index} has been loaded.')

                    # SLICE
                    slice_clip = self.slicer.slice_clip(load_clip)
                    self.show_status(f'The clip {index} has been sliced.')

                    # OVERLAY TEXT
                    overlay_text = slice_clip
                    if self.settings_controller.get_show_overlay():
                        overlay_text = self.slicer.overlay_text(slice_clip, renamer.file_name(path, file))
                        self.show_status(f'Overlay text has been added in the clip {index}.')

                    # TRANSITIONS
                    if self.settings_controller.get_show_transition():
                        if index == 1: # First clip.
                            transition = self.slicer.transition_fade_out(overlay_text)
                            self.show_status(f'Fading-out transition added in the clip {index}.')

                            clips_list.append(transition)

                        elif index == (len(valid_files)): # Last clip.
                            transition = self.slicer.transition_fade_in(overlay_text)
                            self.show_status(f'Fading-in transition added in the clip {index}.')

                            clips_list.append(transition)

                        else: # Middle clips.
                            transition_fade_out = self.slicer.transition_fade_out(overlay_text)
                            self.show_status(f'Fading-out transition added in the clip {index}.')

                            transition = self.slicer.transition_fade_in(transition_fade_out)
                            self.show_status(f'Fading-in transition added in the clip {index}.')

                            clips_list.append(transition)
                    else:
                        clips_list.append(overlay_text)

                    if self.settings_controller.get_render_per_clip():
                        # RENDER
                        self.slicer.render_clip(clips_list[index-1-errors], renamer.file_name(path, file), output_path)
                        self.show_status(f'Clip {index} has been rendered.')

                    timer_end = time()
                    self.show_status(f'Clip {index} timer ended.')

                    total_time = int(timer_end - timer_start)
                    print(f'Time: {total_time} seconds.\n')
                    self.signal_processed.emit('time', f'Time: {total_time} seconds.')

                    # Update report file.
                    reporter.file_update(clip_number=index, original_name=file, delete_original=self.btn_toggle_delete.isChecked(),
                    renamed=renamer.file_name(path, file), game=renamer.game_pattern(), date=renamer.date_pattern(path, file), 
                    time=total_time, total_disk=total_disk, used_disk=used_disk, free_disk=free_disk)
                    self.show_status(f'Report file has been updated.')

                except OSError as error:
                    self.show_status(f'Error! In the flow process.')
                    # print(f'Error: {error}')

                    reporter.file_update(clip_number=index, original_name=file, delete_original=False,
                    renamed='Corrupt', game=None, date=None, time=None, total_disk=None, used_disk=None, free_disk=None)
                    self.show_status(f'The report for the corrupt file has been updated.')

                    errors += 1
                    continue

                if self.btn_toggle_delete.isChecked():
                    self.file_manager.delete_original_files(file)
                    self.show_status(f'Original file {file} has been deleted.')

                self.signal_render.emit(100)
                self.signal_processed.emit('processed', f'{index}/{len(valid_files)} clips processed.')
                print(f'{index}/{len(valid_files)} clips processed.')
                self.signal_processed.emit('hide', None)
                QThread.msleep(1000)

            try:
                if not self.settings_controller.get_render_per_clip():
                # CONCATENATE
                    concatenate_clips = self.slicer.concatenate_clips(clips_list)
                    self.show_status(f'Clip {index} has been concatenated.')

                # RENDER
                    self.slicer.render_clip(concatenate_clips, (f'{renamer.game_pattern()} - TotalClips({len(clips_list)})'), output_path)
                    self.show_status(f'Clip {index} has been rendered.')

            except OSError as error:
                self.show_status(f'Error! In the render process.')
                print(f'Error: {error}')

            self.btn_go.setEnabled(True)
            self.btn_toggle_delete.setEnabled(True)

        except TypeError as error:
            self.show_status(f'Error! The directory is empty or has not valid videos.')
            print(f'Error: {error}')
            self.signal_status.emit(False)