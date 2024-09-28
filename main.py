'''
Elaborador por: Ítalo Osorio
Fecha de creación: 06/06/2024
Última modificación: 28/09/2024

Propósito: Refactorizar el script de cortador de videos "Cortador_Inadoor.py" en clases y métodos.
PD: Mi primera prueba de "POO" en Python :D!
'''

# Librerías:
import os # Para limpiar la consola y manejar rutas.
import time # Para hacer pausas.
import re # Para buscar patrones en los nombres de los archivos.
import tkinter as tk # Para crear una interfaz gráficas mínima.
from datetime import datetime # Para medir el tiempo de ejecución.
from tkinter import filedialog # Para abrir el explorador de archivos.
from moviepy.editor import VideoFileClip # Para cortar y manipular videos.
# Clases:
from Logica.Cortador import Cortador
from Logica.Informador import Informador

# Parámetros:
RUTA_CLIPS = r'C:\Users\Dheam\Videos\Prueba'
CANTIDAD_CLIPS = 10
DURACION_CLIP = 45
FORMATOS_CLIP = ('.mp4', '.avi', '.mov', '.mkv', '.flv')

def clear(cooldown=0):
    '''Limpiar la consola con cooldown opcional a la acción anterior.'''
    time.sleep(cooldown)
    os.system('cls' if os.name == 'nt' else 'clear')
clear()


def select(input_text):
    '''Validar la selección del usuario y usarla globalmente'''
    while True:
        try:
            vuser_select = input(input_text)
            return vuser_select
        except ValueError:
            print('Error! Debe ingresar un valor válido. Intente nuevamente.')

archivo = Informe(RUTA_CLIPS, FORMATOS_CLIP)
archivo.obtener_resumen('crear_csv')

#cortar = Cortar(RUTA_CLIPS, FORMATOS_CLIP, DURACION_CLIP)
#cortar.proceso_corte('cortar')