'''Module responsible for generating the report of the processes performed.'''

# Local Classes:
from Logic.FileManager import FileManager # Import FileManager local class.

class Reporter(FileManager):
    '''Report or summary of the processes performed.'''
    def __init__(self, input_path, video_formats):
        super().__init__(input_path, video_formats)

    def __file_creation(self):
        '''Create the summary file.'''
        file = open(fr'{super().get_output_path}\report.csv', 'a', encoding='utf-8') # The file is created.
        file.write('original name,deleted,renamed,game,date,nº,slicer procces,time\n'.upper()) # The columns of the file are created.
        file.close()

    def get_report(self, value_type):
        '''Get a report'''
        if value_type == 'create_csv':
            return self.__file_creation()
