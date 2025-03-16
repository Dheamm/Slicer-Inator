'''Module responsible to cut and render the video clips.'''

# Libraries:
from os.path import join # To join paths.

from moviepy.editor import VideoFileClip # To manipulate and render the clips.
from moviepy.editor import TextClip
from moviepy.editor import CompositeVideoClip
from moviepy.config import change_settings
from moviepy.editor import concatenate_videoclips
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

class Slicer():
    '''Cut and render the video clips.'''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, 
                logger = None,
                duration:int = 45, 
                text_position:tuple = ("left", "bottom"),
                transition_duration:float = 0.5):
        self.__logger = logger
        self.__duration = duration
        self.__text_position = text_position
        self.__transition_duration = transition_duration
        self.__run_transitions = True
        self.__show_video_text = True

    def get_logger(self):
        '''Get the logger.'''
        return self.__logger
    
    def set_logger(self, new_logger):
        '''Set the logger.'''
        self.__logger = new_logger

    def get_duration(self):
        '''Get the duration of the clip.'''
        return self.__duration

    def set_duration(self, new_duration):
        '''Set the duration of the clip.'''
        self.__duration = new_duration

    def get_text_position(self):
        '''Get the position of the text.'''
        return self.__text_position
    
    def set_text_position(self, new_position:str):
        '''Set the position of the text.'''
        if not new_position == 'none':
            self.__text_position = tuple(new_position.split('-')) # Convert the string to tuple.
        if new_position == 'none':
            self.__text_position = None

    def get_transition_duration(self):
        '''Get the duration of the transition.'''
        return self.__transition_duration
    
    def set_transition_duration(self, new_duration:float):
        '''Set the duration of the transition
        (fade out and fade in).'''
        self.__transition_duration = new_duration

    def load_clip(self, input_path, valid_file):
        '''Load the clip.'''
        return VideoFileClip(join(input_path, valid_file))

    def slice_clip(self, clip):
        '''Cut or 'slice' the clip.'''
        # The clip is cut (the final seconds are kept):
        start_time = max(0, clip.duration - (self.get_duration())) # Get the start time of the clip.
        slice_clip = clip.subclip(start_time, clip.duration) # From start time to final.

        return slice_clip

    def overlay_text(self, clip, input_text:str, font_size:int=25, color_text:str='white'):
        '''Add text to the clip.'''
        text = TextClip(input_text, fontsize=font_size, color=color_text, font='Arial-Bold')
        if self.get_text_position() is not None:
            text = text.set_position(self.get_text_position()).set_duration(clip.duration)
        else:
            text = text.set_duration(clip.duration-clip.duration)

        return CompositeVideoClip([clip, text])

    def transition_fade_out(self, slice_clip):
        '''Fade out the clip.'''
        return slice_clip.fadeout(self.get_transition_duration())
    
    def transition_fade_in(self, slice_clip):
        '''Fade in the clip.'''
        return slice_clip.fadein(self.get_transition_duration())

    def concatenate_clips(self, clips_list:list):
        '''Concatenate the clips.'''
        return concatenate_videoclips(clips_list, method="compose")
    
    def render_clip(self, clip, name, output_path, video_format='.mp4'):
        '''Render the clip.'''
        output = join(output_path, name + video_format) # Built in the name and path.
        temp_audio = join(output_path, 'TEMP_AUDIO_' + name + video_format) # Temporary audio file.
        clip.write_videofile(output, # Rendering the video.
                                    codec="libx264",
                                    fps=60,
                                    threads=4,
                                    audio_codec="aac",
                                    ffmpeg_params=["-vcodec", "h264_nvenc"],
                                    bitrate="16000k",
                                    logger=self.get_logger(), # None or 'bar' to display a progress bar.
                                    temp_audiofile=temp_audio, # The audio file is temporary.
                                    remove_temp=True # Remove the temporary file.
                                    )
        
        clip.close() # Close the clip.

