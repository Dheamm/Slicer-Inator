'''Module responsible to cut and render the video clips.'''

# Libraries:
from os.path import join # To join paths.
from moviepy.editor import VideoFileClip # To manipulate and render the clips.

# Local Classes:
from Logic.FileManager import FileManager #Import FileManager local class.

class Slicer(FileManager):
    '''Cut and render the video clips.'''
    def __init__(self, input_path, output_path, duration):
        super().__init__(input_path, output_path)
        self.__duration = duration

    def get_duration(self):
        '''Get the duration of the clip.'''
        return self.__duration

    def set_duration(self, new_duration):
        '''Set the duration of the clip.'''
        self.__duration = new_duration

    def __cut(self, valid_file, duration):
        '''Cut the clip.'''
        original_clip = VideoFileClip(join(super().get_input_path(), valid_file)) # The clip is loaded.

        # The clip is cut (the final seconds are kept):
        total_duration = original_clip.duration # Total duration of the clip.
        start_time = max(0, total_duration - (duration)) # Get the start time of the clip.
        slice_clip = original_clip.subclip(start_time, total_duration) # From start time to final.
        return slice_clip

    def __render(self, slice_clip, name, video_format):
        '''Render the clip.'''
        output = join(super().get_output_path(), name + video_format) # Built in the name and path.
        slice_clip.write_videofile(output, # Rendering the video.
                                    codec="libx264",
                                    fps=60,
                                    threads=4,
                                    audio_codec="aac",
                                    ffmpeg_params=["-vcodec", "h264_nvenc"],
                                    bitrate="16000k")

    def get_method(self, method_type):
        '''Get the value of the methods.'''
        if method_type == 'cut':
            return self.__cut(super().get_method('valid_file'), self.get_duration())

        elif method_type == 'render':
            return self.__render(self.get_method('cut'), 'test', '.mp4')