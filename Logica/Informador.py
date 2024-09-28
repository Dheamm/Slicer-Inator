from Logica.GestorArchivos import GestorArchivos #Importar clase GestorArchivos.
import os


class Informador(GestorArchivos):
    '''Informe o resumen de los procesos realizados.'''

    def __init__(self, ruta_clips, formatos_clip):
        super().__init__(ruta_clips, formatos_clip)


    def __creacion_archivo(self):
        '''Crear el archivo de resumen.'''
        archivo = open(fr'{self.mostrar_valores('get_salida')}\resumen.csv', 'a', encoding='utf-8') # Se crea el archivo.
        archivo.write('nombre original,eliminado,renombrado,juego,fecha,nº,proceso recortado,tiempo\n'.upper()) # Se crean las columnas del archivo.
        archivo.close()


    def obtener_resumen(self, tipo):
        '''Obtener el resumen.'''
        if tipo == 'crear_csv':
            return self.__creacion_archivo()
