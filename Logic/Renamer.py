'''This module is responsible for renaming the clips.'''

# Libraries:
from os.path import getmtime # To get the time stamp of the file.
from os import rename # To rename the file.
from datetime import datetime # To format the date.

class Renamer():
    '''Rename the files.'''
    def __init__(self, input_name):
        self.__input_name = input_name

    def get_input_name(self):
        '''Get the file name.'''
        return self.__input_name

    def set_input_name(self, new_name):
        '''Set the file name.'''
        self.__file_name = new_name

    def __date_pattern(self, file_path):
        '''Get the date pattern of the file.'''
        time_stamp = getmtime(file_path) # Get the 'unix' time stamp of the file.
        date = datetime.fromtimestamp(time_stamp) # Convert the time stamp to a date.
        date_format = date.strftime('%Y.%m.%d %H.%M') # Format the date.

        return date_format
    
    def __name_format(self):
        '''Get the name format.'''

    def rename_file(self):
        '''Rename the file.'''
        pass