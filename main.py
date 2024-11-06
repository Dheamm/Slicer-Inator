'''
Prepared by: Ítalo Osorio
Date of creation: 06/06/2024
Last modification: 04/11/2024

Purpose: Refactor the video cutter script “Slicer Inator.py” in classes and methods.
PS: My first “POO” test in Python :D!
'''

# Libraries:
import os # To clear the console.
from time import sleep # To add cooldowns before clearing the console.
from sys import exit # To close the application.
from PyQt5.QtWidgets import QApplication # To create the interface application.

# Local Classes:
from Logic.FileManager import FileManager # Import FileManager local class.
from Logic.Slicer import Slicer # Import Slicer local class.
from Interface.WindowsController import WindowsController # Import WindowsController local class.

# Parameters:
INPUT_PATH = r'C:\Users\Dheam\Videos\Prueba'
CLIPS_LIMIT = 10
DURATION = 45
VIDEO_FORMATS = ('.mp4', '.avi', '.mov', '.mkv', '.flv')

def clear(cooldown=0):
    '''Clean the console with optional cooldown to the previous action.'''
    sleep(cooldown)
    os.system('cls' if os.name == 'nt' else 'clear')


def select(input_text):
    '''Validate the users selection and use it globally.'''
    while True:
        try:
            user_select = input(input_text)
            return user_select
        except ValueError:
            print('Error! You must enter a valid value. Please try again.')


def start_application():
    # Logic:
    file_manager = FileManager(INPUT_PATH, VIDEO_FORMATS) # Instance of FileManager
    slicer = Slicer(DURATION, CLIPS_LIMIT) # Instance of Slicer

    # Interface:
    app = QApplication([]) # Create the application to show the interface.
    interface = WindowsController(file_manager, slicer) # Instance of MainWindow

    interface.execute_main_window() # Show the window with a parameter of RenderWindow.
    exit(app.exec_()) # Execute the event loop.

start_application()