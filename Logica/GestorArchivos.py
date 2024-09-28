'''Clase Archivo: Obtener la lista de archivos y los archivos válidos especificamente.'''

#Librerias:
from os import listdir # Para leer los archivos de una ruta.
from os import makedirs # Para crear carpetas.
from os.path import join # Para unir rutas.

class GestorArchivos():
    '''Obtener la lista de archivos y los archivos especificamente.'''
    def __init__(self, ruta_clips, formatos_clip):
        self.__ruta_clips = ruta_clips
        self.__formatos_clip = formatos_clip


    def __obtener_lista(self):
        '''Obtener la lista de clips en la ruta seleccionada.'''
        lista_archivos = listdir(self.__ruta_clips)

        return lista_archivos


    def __obtener_ruta_salida(self):
        '''Obtener la ruta de salida.'''
        ruta_salida = join(self.mostrar_valores('get_ruta'), 'Recortado')
        makedirs(ruta_salida, exist_ok=True) # Crear carpeta de salida.

        return ruta_salida


    def __obtener_validos(self):
        '''Obtener el archivo seleccionado.'''
        archivos_validos = []
        for archivo in self.__obtener_lista(): # Obtener el nombre de un archivo.
            for formato in self.__formatos_clip:
                if archivo.endswith(formato): # Verificar si el archivo es un formato admitido.
                    archivos_validos.append(archivo) # Agregar a formatos válidos.

        return archivos_validos


    def mostrar_valores(self, tipo):
        '''Mostrar la lista de archivos y obtener ruta.'''
        if tipo == 'get_ruta':
            return self.__ruta_clips

        elif tipo == 'get_salida':
            return self.__obtener_ruta_salida()

        elif tipo == 'lista':
            print('\nLista de archivos: ')
            for i in self.__obtener_lista():
                print (f'- {i}')
            print('')

        elif tipo == 'archivos_validos':
            return self.__obtener_validos()

        else:
            raise ValueError('Error! Tipo de parámetro no válido. Intente nuevamente.')
