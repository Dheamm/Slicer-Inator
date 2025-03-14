'''Module responsible for generating the report of the processes performed.'''

# Libraries:
from os import path # To verify if the file exists.

class Reporter():
    '''Report or summary of the processes performed.'''
    def __init__(self, output_path, file_name='report.csv'):
        self.__output_path = output_path
        self.__file_name = file_name

    def get_file_name(self):
        '''Get the file name.'''
        return self.__file_name
    
    def set_file_name(self, new_name):
        '''Set the file name.'''
        self.__file_name = new_name

    def get_output_path(self):
        '''Get the output path.'''
        return self.__output_path
    
    def set_output_path(self, new_path):
        '''Set the output path.'''
        self.__output_path = new_path

    def file_creation(self):
        '''Create the summary file.'''
        if not path.exists(fr'{self.get_output_path()}\{self.get_file_name()}'): # Verify if the file exists.
            file = open(fr'{self.get_output_path()}\{self.get_file_name()}', 'a', encoding='utf-8') # The file is created.
            file.write('num, original name,delete original,renamed,game,date,render time (sec),total disk(GB),used(GB),free(GB)\n'.upper()) # The columns of the file are created.
            #deleted original,slicer procces
            file.close()

    def file_update(self, clip_number, original_name, delete_original, renamed, game, date, time, total_disk, used_disk, free_disk):
        '''Update the summary file.'''
        file = open(fr'{self.get_output_path()}\{self.get_file_name()}', 'a', encoding='utf-8') # The file is opened.
        file.write(f'{clip_number},{original_name},{delete_original},{renamed}.mp4,{game},{date},{time},{total_disk},{used_disk},{free_disk}\n')
