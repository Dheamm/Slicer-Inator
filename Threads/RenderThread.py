'''Module responsible to create the render procces thread.'''

# Libraries:
from PyQt5.QtCore import QThread # To create threads.
from PyQt5.QtCore import pyqtSignal # Emit signals to update the progress bar.
from time import time # To measure the time of the render process.
from os.path import join # To join the paths.

# Local Classes:
from Logic.Renamer import Renamer # Import Renamer local class.
from Logic.Reporter import Reporter # Import Reporter local class.
from Logic.BarLogger import BarLogger # Import BarLogger local class.

class RenderThread(QThread):
    signal_status = pyqtSignal(bool)
    signal_processed = pyqtSignal(str, object)
    signal_progress_logger = pyqtSignal(int)
    signal_status_logger = pyqtSignal(int, int)
    signal_color_bar = pyqtSignal(str)

    signal_name_message = pyqtSignal(str)
    signal_status_message = pyqtSignal(str)
    signal_timer_start = pyqtSignal()
    signal_timer_stop = pyqtSignal()
    signal_archive_count_message = pyqtSignal(int, int)

    def __init__(self, file_manager, slicer, data_json):
        super().__init__()
        self.file_manager = file_manager
        self.slicer = slicer
        self.data_json = data_json

    def show_status(self, status:str):
        '''Show the status info and send to the render window.'''
        self.signal_status_message.emit(status)
        print(status)

    def run(self):
        '''Run the render process.'''
        try:
            progress_logger = BarLogger(self.signal_progress_logger, self.signal_status_logger)
            self.slicer.set_logger(progress_logger)

            path = self.file_manager.get_input_path()
            valid_files = self.file_manager.get_method('valid_files_list')
            if self.file_manager.get_output_path() is None:
                self.file_manager.create_output_path()
            output_path = self.file_manager.get_output_path()
            reporter = Reporter(output_path)
            reporter.file_creation()
            clips_list = []
            errors = 0

            for index, file in enumerate(valid_files):
                index += 1
                if self.data_json.get_json("clip_limit") >= index:

                    renamer = Renamer(file, index)
                    total_disk, used_disk, free_disk = self.file_manager.get_method('disk_space')

                    # -- FLOW -- #

                    self.signal_name_message.emit(file)
                    if index == 1:
                        print(f'{0}/{len(valid_files)} clips processed.')
                    print(f'Name: {file}')
                    self.signal_archive_count_message.emit(index, len(valid_files))

                    try:
                        self.signal_timer_start.emit()
                        timer_static_start = time()
                        self.show_status(f'Clip {index} timer started.')

                        # LOAD
                        load_clip = self.slicer.load_clip(path, file)
                        self.show_status(f'The clip {index} has been loaded.')

                        # SLICE
                        slice_clip = self.slicer.slice_clip(load_clip)
                        self.show_status(f'The clip {index} has been sliced.')

                        # OVERLAY TEXT
                        overlay_text = slice_clip
                        if self.data_json.get_json("overlay")!= "off":
                            overlay_text = self.slicer.overlay_text(slice_clip, renamer.file_name(path, file))
                            self.show_status(f'Overlay text has been added in the clip {index}.')

                        # TRANSITIONS
                        if self.data_json.get_json("transitions") != 0:
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

                        if self.data_json.get_json("render_type") == "Separated":
                            # RENDER
                            self.slicer.render_clip(clips_list[index-1-errors], renamer.file_name(path, file), output_path)
                            self.show_status(f'Clip {index} has been rendered.')
                        
                        self.signal_timer_stop.emit()
                        timer_static_end = time()
                        self.show_status(f'Clip {index} timer ended.')

                        total_static_time = int(timer_static_end - timer_static_start)

                        print(f'Time: {total_static_time} seconds.\n')


                        # Update report file.
                        reporter.file_update(clip_number=index, original_name=file, delete_original=self.data_json.get_json("delete_original"),
                        renamed=renamer.file_name(path, file), game=renamer.game_pattern(), date=renamer.date_pattern(path, file), 
                        time=total_static_time, total_disk=total_disk, used_disk=used_disk, free_disk=free_disk)
                        self.show_status(f'Report file has been updated.')

                    except OSError as error:
                        self.show_status(f'Error! In the flow process.')
                        # print(f'Error: {error}')

                        reporter.file_update(clip_number=index, original_name=file, delete_original=False,
                        renamed='Corrupt', game=None, date=None, time=None, total_disk=None, used_disk=None, free_disk=None)
                        self.show_status(f'The report for the corrupt file has been updated.')

                        errors += 1
                        continue

                    if self.data_json.get_json("delete_original") == "on" and self.data_json.get_json("render_type") == "Separated":
                        self.file_manager.delete_original_files(file)
                        self.show_status(f'Original file {file} has been deleted.')

                    print(f'{index}/{len(valid_files)} clips processed.')
                    QThread.msleep(1000)

                else:
                    self.show_status(f'Clips limit reached ({self.data_json.get_json("clip_limit")}).')

            try:
                if self.data_json.get_json("render_type") == "Compact":
                # CONCATENATE
                    concatenate_clips = self.slicer.concatenate_clips(clips_list)
                    self.show_status(f'Clip {index} has been concatenated.')

                # RENDER
                    self.slicer.render_clip(concatenate_clips, (f'{renamer.game_pattern()} - TotalClips({len(clips_list)})'), output_path)
                    self.show_status(f'Clip {index} has been rendered.')

                if self.data_json.get_json("delete_original") == "on" and self.data_json.get_json("render_type") == "Compact":
                    for file in valid_files:
                        try:
                            self.file_manager.delete_original_files(file)
                            self.show_status(f'Original file {file} has been deleted.')
                        except OSError as error:
                            self.show_status(f'Error! Deleting file: {file}')
                            continue

            except OSError as error:
                self.show_status(f'Error! In the render process.')
                print(f'Error: {error}')

            # self.btn_go.setEnabled(True)
            # self.btn_toggle_delete.setEnabled(True)

        except TypeError as error:
            self.show_status(f'Error! The directory is empty or has not valid videos.')
            print(f'Error: {error}')
            self.signal_status.emit(False)