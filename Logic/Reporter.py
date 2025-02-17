'''Module responsible for generating the report of the processes performed.'''

class Reporter():
    '''Report or summary of the processes performed.'''
    def __init__(self, output_path):
        self.__output_path = output_path

    def get_output_path(self):
        '''Get the output path.'''
        return self.__output_path
    
    def set_output_path(self, new_path):
        '''Set the output path.'''
        self.__output_path = new_path

    def file_creation(self):
        '''Create the summary file.'''
        file = open(fr'{self.get_output_path()}\report.csv', 'a', encoding='utf-8') # The file is created.
        file.write('original name,renamed,game,date,num,render time (sec)\n'.upper()) # The columns of the file are created.
        #deleted original,slicer procces
        file.close()

    def file_update(self, original_name, renamed, game, date, clip_number, time):
        '''Update the summary file.'''
        file = open(fr'{self.get_output_path()}\report.csv', 'a', encoding='utf-8') # The file is opened.
        file.write(f'{original_name},{renamed}.mp4,{game},{date},{clip_number},{time}\n')
