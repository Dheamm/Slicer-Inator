'''Obtain the list of files and the valid ones'''

# Libraries:
from os import listdir # To read the files from a path.
from os import makedirs # To make directories.
from os.path import join # To join paths.
from os import remove # To delete files.
from os.path import splitdrive # To get the drive letter.
from shutil import disk_usage # To get the disk space.
from os import startfile # To open the directory.
from glob import glob # To get the list of files with a pattern.


class FileManager():
    '''Get the list of files and handle them.'''
    def __init__(self, input_path, video_formats, output_path=None):
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
        return self.__create_output_path(self.get_input_path())

    def set_output_path(self, new_path):
        '''Set the output path.'''
        self.__output_path = new_path

    def __files_list(self, path):
        '''A list of files in the selected path.'''
        return listdir(path) # Get the list of files in the path.

    def __valid_files_list(self, file_list, video_formats):
        '''A list of all the valid files.'''
        valid_files = []
        for file in file_list:
            for one_format in video_formats:
                if file.endswith(one_format): # Verify is the file has a valid format.
                    valid_files.append(file) # Add the file to the valid_file list.
        if not valid_files:
            print('Error! There are no valid files in the selected path.')
            return None
        else:
            return valid_files

    def __create_output_path(self, input_path, directory_name='Sliced'):
        '''Create the output path.'''
        self.__output_path = join(input_path, directory_name) # Join the paths.
        makedirs(self.__output_path, exist_ok=True) # Create the directory if it doesn't exist.
        return self.__output_path
    
    def delete_original_files(self, file):
        '''Delete the original files.'''
        file_path = join(self.get_input_path(), file)
        remove(file_path)

    def get_drive(self, input_path):
        '''Return the drive letter of the specified path.'''
        try:
            drive, _ = splitdrive(input_path)
        except ValueError:
            drive = None
        
        return drive
    
    def delete_temp_files(self, pattern='*TEMP_AUDIO_*'):
        '''Delete the temporary directory.'''
        temps_files = glob(join(self.get_output_path(), pattern))

        # Delete the temporary files.
        for file in temps_files:
            remove(file)
    
    def __disk_space(self, drive):
        """Show the total, used and free disk space in GB."""
        try:
            total, used, free = disk_usage(f"{drive}/")
        
            return (
                round(total / (1024**3), 1),
                round(used / (1024**3), 1),
                round(free / (1024**3), 1)
                    )
        except FileNotFoundError:
            return "Unknown Drive", 0, 0
        
    def open_directory(self, directory):
        '''Open a directory.'''
        startfile(directory)

    def get_method(self, method_type):
        '''Get the value of the methods.'''
        if method_type == 'list':
            return self.__files_list(self.get_input_path())

        elif method_type == 'valid_files_list':
            return self.__valid_files_list(self.get_method('list'), self.get_video_formats())
        
        elif method_type == 'disk_space':
            return self.__disk_space(self.get_drive(self.get_input_path()))

        else:
            print('Error! The method is not valid.')
