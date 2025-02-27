'''Module responsible to cut and render the video clips.'''

# Libraries:
from os.path import join # To join paths.

from moviepy.editor import VideoFileClip # To manipulate and render the clips.
from moviepy.editor import TextClip
from moviepy.editor import CompositeVideoClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

class Slicer():
    '''Cut and render the video clips.'''
    def __init__(self, duration, limit):
        self.__duration = duration
        self.__limit = limit
        self.__text_position = ("left", "bottom")

    def get_duration(self):
        '''Get the duration of the clip.'''
        return self.__duration

    def set_duration(self, new_duration):
        '''Set the duration of the clip.'''
        self.__duration = new_duration

    def get_limit(self):
        '''Get the limit of the clips.'''
        return self.__limit
    
    def set_limit(self, new_limit):
        '''Set the limit of the clips.'''
        self.__limit = new_limit

    def get_text_position(self):
        '''Get the position of the text.'''
        return self.__text_position
    
    def set_text_position(self, new_position:str):
        '''Set the position of the text.'''
        if not new_position == 'none':
            self.__text_position = tuple(new_position.split('-')) # Convert the string to tuple.
        if new_position == 'none':
            self.__text_position = None

    def cut(self, input_path, valid_file):
        '''Cut the clip.'''
        original_clip = VideoFileClip(join(input_path, valid_file)) # The clip is loaded.

        # The clip is cut (the final seconds are kept):
        total_duration = original_clip.duration # Total duration of the clip.
        start_time = max(0, total_duration - (self.get_duration())) # Get the start time of the clip.
        slice_clip = original_clip.subclip(start_time, total_duration) # From start time to final.
        return slice_clip

    def render(self, slice_clip, name, video_format, output_path):
        '''Render the clip.'''
        output = join(output_path, name + video_format) # Built in the name and path.
        temp_audio = join(output_path, 'TEMP_AUDIO_' + name + video_format) # Temporary audio file.
        slice_clip.write_videofile(output, # Rendering the video.
                                    codec="libx264",
                                    fps=60,
                                    threads=4,
                                    audio_codec="aac",
                                    ffmpeg_params=["-vcodec", "h264_nvenc"],
                                    bitrate="16000k",
                                    logger='bar', # None or 'bar' to display a progress bar.
                                    temp_audiofile=temp_audio, # The audio file is temporary.
                                    remove_temp=True # Remove the temporary file.
                                    )
        
        slice_clip.close() # Close the clip.

    def add_text(self, slice_clip, input_text:str, font_size:int, color:str):
        '''Add text to the clip.'''
        text = TextClip(input_text, fontsize=font_size, color=color, font="Arial-Bold")
        if self.get_text_position() is not None:
            text = text.set_position(self.get_text_position()).set_duration(slice_clip.duration)
        else:
            text = text.set_duration(slice_clip.duration-slice_clip.duration)
        video_final = CompositeVideoClip([slice_clip, text])

        return video_final

