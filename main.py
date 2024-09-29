'''
Prepared by: Ítalo Osorio
Date of creation: 06/06/2024
Last modification: 09/28/2024

Purpose: Refactor the video cutter script “Slicer Inator.py” in classes and methods.
PS: My first “POO” test in Python :D!
'''

# Libraries:
import os # To clear the console.
from time import sleep # To add cooldowns before clearing the console.

# Local Classes:

# Parameters:
INPUT_PATH = r'C:\Users\Dheam\Videos\Prueba'
CLIPS_LIMIT = 10
DURATION = 45
VIDEO_FORMATS = ('.mp4', '.avi', '.mov', '.mkv', '.flv')

def clear(cooldown=0):
    '''Clean the console with optional cooldown to the previous action.'''
    sleep(cooldown)
    os.system('cls' if os.name == 'nt' else 'clear')
clear()


def select(input_text):
    '''Validate the users selection and use it globally.'''
    while True:
        try:
            user_select = input(input_text)
            return user_select
        except ValueError:
            print('Error! You must enter a valid value. Please try again.')


def main():
    '''Main function.'''
    print('Welcome to the Slicer Inator!')


