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
from psutil import process_iter # To get the process list.
from psutil import Process # To get the process.
from pathlib import Path # To get the home and video directory.



class FileManager():
    '''Get the list of files and handle them.'''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,
                video_formats:tuple = ('.mp4', '.avi', '.mov', '.mkv', '.flv'),
                output_path=None,
                directory_output_name='Sliced'):
        self.__input_path = str(self.base_directory())
        self.__video_formats = video_formats
        self.__output_path = output_path
        self.__directory_output_name = directory_output_name

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
        return self.__output_path

    def set_output_path(self, new_path):
        '''Set the output path.'''
        self.__output_path = new_path

    def get_directory_output_name(self):
        '''Get the name of the output directory.'''
        return self.__directory_output_name
    
    def set_directory_output_name(self, new_name):
        '''Set the name of the output directory.'''
        self.__directory_output_name = new_name

    def search_directory(self, input_path:str, directory:str):
        '''Search the directory.'''
        path = Path(join(input_path, directory))
        return path.exists()

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

    def create_output_path(self):
        '''Create the output path.'''
        output_path = join(self.get_input_path(), self.get_directory_output_name()) # Join the paths.
        makedirs(output_path, exist_ok=True) # Create the directory if it doesn't exist.

        self.set_output_path(output_path) # Set the output path.

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
        try:
            temps_files = glob(join(self.get_output_path(), pattern))

            # Delete the temporary files.
            for file in temps_files:
                remove(file)
        except ValueError as e:
            print(f"Temp Files have not been deleted!\nError: {e}")
    
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

    def close_ffmpeg_process(self):
        '''Close the `ffmpeg` process.'''
        for process in process_iter(attrs=['pid', 'name']):
            if "ffmpeg" in process.info['name'].lower():  #Search 'ffmpeg' in the process name
                print(f"Stopping the process: {process.info}")
                Process(process.info['pid']).terminate()  # Stop the process.

    # def close_vlc_process(self):
    #     '''Close the `vlc` process.'''
    #     for process in process_iter(attrs=['pid', 'name']):
    #         if "vlc" in process.info['name'].lower():

    
    def home_dir(self):
        # Get the home directory.
        return Path.home()

    def dir_exists(self, directory:str):
        '''Check if the directory exists.'''
        return (self.home_dir()/directory).exists()

    def base_directory(self, directory:str='Videos'):
        '''Get the base or main directory.'''
        if not self.dir_exists(directory):
            return self.home_dir()
        else:
            return self.home_dir()/directory
        
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