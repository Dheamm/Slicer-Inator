'''Module responsible to cut and render the video clips.'''

# Libraries:
from os.path import join # To join paths.
from moviepy.editor import VideoFileClip # To manipulate and render the clips.

class Slicer():
    '''Cut and render the video clips.'''
    def __init__(self, duration, limit):
        self.__duration = duration
        self.__limit = limit

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
        slice_clip.write_videofile(output, # Rendering the video.
                                    codec="libx264",
                                    fps=60,
                                    threads=4,
                                    audio_codec="aac",
                                    ffmpeg_params=["-vcodec", "h264_nvenc"],
                                    bitrate="16000k",
                                    logger=None, # or 'bar' to display a progress bar.
                                    remove_temp=True # Remove the temporary file.
                                    )
        
        slice_clip.close() # Close the clip.