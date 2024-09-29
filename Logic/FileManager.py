'''Obtain the list of files and the valid ones'''

# Libraries:
from os import listdir # To read the files from a path.
from os import makedirs # To make directories.
from os.path import join # To join paths.

class FileManager():
    '''Get the list of files and handle them.'''
    def __init__(self, input_path, video_formats=('.mp4'), output_path=None):
        self.__input_path = input_path
        self.__video_formats = video_formats
        self.__output_path = output_path

    def get_input_path(self):
        '''Get the path of the clips.'''
        return self.__input_path

    def set_input_path(self, new_path):
        '''Set the path of the clips.'''
        self.__input_path = new_path

    def get_video_formats(self):
        '''Get the video formats.'''
        return self.__video_formats

    def set_video_formats(self, new_formats):
        '''Set the video formats.'''
        self.__video_formats = new_formats

    def get_output_path(self):
        '''Get the output path.'''
        return self.__create_output_path()
    
    def set_output_path(self, new_path):
        '''Set the output path.'''
        self.__output_path = new_path

    def __file_list(self):
        '''Get a list of clips in the selected path.'''
        return listdir(self.__input_path)

    def __valid_files(self):
        '''Get the valid files.'''
        valid_files = []
        for file in self.__file_list(): # Get a name of one file.
            for one_format in self.__video_formats:
                if file.endswith(one_format): # Verify is the file has a valid format.
                    valid_files.append(file) # Add the file to the valid_files list.
        return valid_files

    def __create_output_path(self):
        '''Create the output path.'''
        self.__output_path = join(self.get_input_path, 'Recortado') # Join the paths.
        makedirs(self.__output_path, exist_ok=True) # Create the directory if it doesn't exist.
        return self.__output_path

    def get_values(self, value_type):
        '''Get the value of the methods.'''
        if value_type == 'list':
            print('\nFile list: ')
            for i in self.__file_list():
                print (f'- {i}')
            print('')

        elif value_type == 'valid_files':
            return self.__valid_files()
