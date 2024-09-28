import re

# class Renombrar(Cortar):
#     '''Proceso de renombrar los clips.'''
#     def patron_fecha(self):
#         '''Patrón de búsqueda para los nombres de los clips.'''
#         fecha = re.search(r'\d{4}.\d{2}.\d{2}', nombre_entrada).group()

#         return fecha



fecha_entrada = '2024.09.24' #yyyy.mm.dd
separador = input('Ingrese el separador de la fecha de entrada: ')
if separador in ['.', '-', '_', '/']:
    partes = fecha_entrada.split(separador)
    dia = partes[2]
    mes = partes[1]
    año = partes[0]

separador = input('Ingrese el separador de la fecha de salida: ')
if separador in ['.', '-', '_', '/']:
    fecha_salida = f'{dia}{separador}{mes}{separador}{año}'
    print(fecha_salida)