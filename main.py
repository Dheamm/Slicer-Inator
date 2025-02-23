'''
Prepared by: Ítalo Osorio
Date of creation: 06/06/2024
Last modification: 23/02/2025

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
# Todo: Agregar info al reporter sobre de si el video original fue borrado.✔️
# Todo: Agregar un boton para abrir la carpeta de salida y entrada.✔️
# Todo: Que te muestre los clips totales en la interfaz que quedan y los que llevas.✔️
# Todo: Si el render se detiene, borrar el archivo temporal que este crea. (Realmente lo borra al iniciar)✔️
# Todo: Cambiar ubicación del archivo temporal que se crea al renderizar. ✔️

## Pending tasks: ##
#Interface:
# Todo: Que la información que muestra la consola se muestre en la interfaz.
# Todo: Que la barra sea mas precisa (y real).
# Todo: Embellecer la interfaz grafica.

#Errors:
# Todo: Hay situaciones (sobre todo cuando el render tira una excepción) que el ciclo de la barra sigue.
# Todo: Al borrar el archivo temporal, si el render se detiene, el archivo temporal no puede ser borrado pq se está usando.

# Funionalities:
# Todo: Opción para poder pausar y reanudar el proceso.
# Todo: Opción de pasar al siguiente clip en el renderizado.
# Todo: Que el usuario pueda seleccionar el juego según el nombre del clip.
# Todo: Ventana o apartado de configuración para cambiar los parametros de corte, renderizado y limites de los clips.
# Todo: Darle la opción al usuario de convertir los videos a mp3.
# Todo: Usar SQL y de esa forma poder hacer consultas mas complejas y poder continuar el proceso si se cierra la aplicación.

# Possible:
# Todo: Si existe un reporte.csv borrarlo y crear uno nuevo. (Opción de borrarlo para el usuario)