'''
Prepared by: Ítalo Osorio
Date of creation: 06/06/2024
Last modification: 19/02/2025

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

#Completed tasks:
# Todo: Manejar videos corrompidos y saltarselos. ✔️
# Todo: Hacer que la barra de progreso no avance si el video no se pudo cortar. ✔️
# Todo: Configurar opcion de borrar el video original  ✔️
# Todo: El reporter tiene el uso del disco.✔️
# Todo: agregar info al reporter sobre de si el video original fue borrado.✔️

# Pending tasks:
# Todo: Que te muestre los clips totales en la interfaz que quedan y los que llevas
# Todo: Agregar un boton para ir a la carpeta de salida y entrada y tambien abrir el reporte.
# Todo: Si se da la casualidad de que hayan dos archivos con el mismo nombre en la carpeta de salida, se sobreescribiran, hacer que aparezca en el nombre (2) o algo así.
# Todo: Que los mensajes aparezcan en la interfaz y no en la consola.
# Todo: Mejorar la interfaz grafica.
# Todo: Agregar un boton de pausa.
# Todo: Agregar un boton de reanudar.
# Todo: Borrar el archivo temporal que se crea al iniciar el render si es que este se detiene por algo.
# Todo: Hacer que al crear el csv se borre si hay uno anterior o al menos que se reescriba (Solo al crear, no al llenar info)
# Todo: Seleccionar el nombre del juego segun el nombre del clip
# Todo: Al usar el boton back durante el proceso de renderizado no pasa lo que esperarias.
# Todo: Agregar un boton pause que permita reanudar el proceso de renderizado.
# Todo: Una vez el programa ya ha rendirazo todos los clips, al volver al menu y luego volver a la renderwindow, el progressbar se queda en 100.
# Todo: Borrar archivo temporal que se crea al parar el render.
# Todo: A veces se inicia la barra de render cuando el renderthread da error
# Todo: Hacer una opcion para convertir los videos en mp3 ideal para la musica o liberar aun mas espacio.