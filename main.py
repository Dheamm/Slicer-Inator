'''
Prepared by: Ítalo Osorio
Date of creation: 06/06/2024
Last modification: 04/11/2024

Purpose: Refactor the video cutter script “Slicer Inator.py” in classes and methods.
PS: My first “POO” test in Python :D!
'''

# Libraries:
import threading # To use threads.
from sys import stdout # To overwrite a line in console.
import os # To clear the console.
from time import sleep # To add cooldowns before clearing the console.
from time import time # To measure the time of the process.
from PyQt5.QtWidgets import QApplication # To create the interface application.
from sys import exit # To close the application.

# Local Classes:
from Logic.FileManager import FileManager # Import FileManager local class.
from Logic.Slicer import Slicer # Import Slicer local class.
from Interface.MainWindow import MainWindow # Import MainWindow local class.
from Interface.RenderWindow import RenderWindow # Import RenderWindow local class.

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
    print('This program will cut and render video clips.\n')

    # Instances:
    file_manager = FileManager(INPUT_PATH, VIDEO_FORMATS) # Create the FileManager object.
    slicer = Slicer(DURATION, CLIPS_LIMIT) # Create the Slicer object.

    try:
        # Render the clip:
        for index, file in enumerate(file_manager.get_method('valid_files_list')):
            index += 1

            # Event to control the animation:
            animation_event = threading.Event()

            def loading_animation():
                states = [
                    'Rendering',
                    'Rendering.', 
                    'Rendering..', 
                    'Rendering...'
                ]
                while not animation_event.is_set(): 
                    for state in states:
                        stdout.write('\r' + ' ' * 30 + '\r') # Clear the line.
                        stdout.write(f"{state}") # Show the state.
                        stdout.flush()  # Clean the buffer.
                        sleep(0.5) # Cooldown.
                        if animation_event.is_set():  
                            stdout.write('\r' + ' ' * 30 + '\r') # Clear the line.
                            stdout.write(f'The clip {index} has been rendered!') # Show the final message.
                            break

            print(f'- CLIP {index}:')
            print(f'Name: {file}')

            # adjust = slicer.get_limit() - index
            cut = slicer.cut(file_manager.get_input_path(), file) # Cut the clip.
            print(f'The clip {index} has been cut!')

            thread1 = threading.Thread(target=loading_animation) # Loading animation. # Render the clip.
            start = time()  # Start the timer.
            thread2 = threading.Thread(target=lambda:slicer.render(cut, (f'Sliced_{index}'), '.mp4', file_manager.get_output_path()))

            thread1.start() # Start the loading animation.
            thread2.start() # Start the rendering

            thread2.join() # Wait for the rendering to finish.
            end = time() # End the timer.

            animation_event.set() # Activate the event to stop the animation.
            thread1.join() # Wait for the animation to finish.

            print(f'\nTime: {int(end - start)} seconds.\n') # Show the time of the process.

    except TypeError: # Empty directory or invalid videos.
        print('Error! The directory is empty or has not valid videos.')

    except OSError: # File Corrupted.
        print('Error! The clip could not be rendered.')

app = QApplication([])  # Create the application.

render = RenderWindow() # Create the RenderWindow object.

interface = MainWindow() # Create the GraphicInterface object.
interface.main_window(render.render_window) # Show the window.

exit(app.exec_())  # Execute the event loop.


