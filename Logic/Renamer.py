'''This module is responsible for renaming the clips.'''

# Libraries:
from os.path import getmtime # To get the time stamp of the file.
from datetime import datetime # To format the date.

# Local Classes:
from Logic.FileManager import FileManager # Import FileManager local class.


class Renamer(FileManager):
    '''Rename the files.'''
    def __init__(self, file_name, input_path):
        super().__init__(input_path)
        self.__file_name = file_name

    def get_file_name(self):
        '''Get the file name.'''
        return self.__file_name

    def set_file_name(self, new_name):
        '''Set the file name.'''
        self.__file_name = new_name

    def __date_pattern(self, file_path):
        '''Get the date pattern of the file.'''
        time_stamp = getmtime(file_path) # Get the 'unix' time stamp of the file.
        date = datetime.fromtimestamp(time_stamp) # Convert the time stamp to a date.
        date_format = date.strftime('%Y.%m.%d %H.%M') # Format the date.

        return date_format

    def get_value(self, value_type):
        '''Get the value of the methods.'''
        if value_type == 'date':
            return self.__date_pattern(super().get_input_path())
        
