'''This module is responsible for renaming the clips.'''

# Libraries:
from os.path import getmtime # To get the time stamp of the file.
from datetime import datetime # To format the date.
from os.path import join # To join the paths.

class Renamer():
    '''Rename the files.'''
    def __init__(self, input_name, clip_index):
        self.__input_name = input_name
        self.__clip_index = clip_index

    def get_input_name(self):
        '''Get the file name.'''
        return self.__input_name

    def set_input_name(self, new_name):
        '''Set the file name.'''
        self.__file_name = new_name

    def get_clip_index(self):
        '''Get the index of the clip.'''
        return self.__clip_index
    
    def set_clip_index(self, new_index):
        '''Set the index of the clip.'''
        self.__clip_index = new_index

    def date_pattern(self, input_path, file):
        '''Get the date pattern of the file.'''
        time_stamp = getmtime(join(input_path + '\\' + file)) # Get the 'unix' time stamp of the file.
        date = datetime.fromtimestamp(time_stamp) # Convert the time stamp to a date.
        date_format = date.strftime('%d.%m.%Y %H.%M') # Format the date.

        return date_format
    
    def game_pattern(self):
        '''Get the game of the file name.'''
        return self.get_input_name().split(' - ')[0]
    
    def file_name(self, input_path, file):
        '''Rename the file.'''
        game = self.game_pattern()
        date = self.date_pattern(input_path, file)
        index = self.get_clip_index()
        return (f'{game} - {date} - Clip_{index}') # Rename the file.
    
    def __str__(self):
        pass
