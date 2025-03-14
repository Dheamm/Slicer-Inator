'''
Prepared by: Ítalo Osorio
Date of creation: 06/06/2024
Last modification: 14/03/2025

Purpose: Refactor the video cutter script “Slicer Inator.py” in classes and methods.
PS: My first “POO” test in Python :D!
'''

# Libraries:
from sys import exit # To close the application.
from PyQt5.QtWidgets import QApplication # To create the interface application.

# Local Classes:
from Interface.WindowsController import WindowsController # Import WindowsController local class.


def start_application():
    # Interface:
    app = QApplication([]) # Create the application to show the interface.
    interface = WindowsController() # Instance of MainWindow

    interface.get_main_window().open() # Show the window with a parameter of RenderWindow.
    exit(app.exec_()) # Execute the event loop.

if __name__ == '__main__':
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
# Todo: Que la información que muestra la consola se muestre en la interfaz. ✔️
# Todo: Al borrar el archivo temporal, si el render se detiene, el archivo temporal no puede ser borrado pq se está usando. ✔️
# Todo: Si el usario ejecuta el programa, que deba seleccionar una input path. ## Se selecciona por defecto. ✔️

## Pending tasks: ##
#Refaactor:
# Todo: Tener una clase controlador (Al estilo MVC (Model-View-Controller)) que maneje los atributos de settings y centralizarlo ahí, tener las rutas y otras cosas y que esta sea singelton.

#Interface:
# Todo: Que la barra sea mas precisa (y real).
# Todo: Embellecer la interfaz grafica.
# Todo: Agregar una ventana emergente o simplemente un avis cuando haya un error.

#Errors:
# Todo: Si en settings ingresan valores invalidos controlarlos.
# Todo: Hay situaciones (sobre todo cuando el render tira una excepción) que el ciclo de la barra sigue.
# Todo: Mejorar el manejo de errores y ser mas especifico con el.
# Todo: Si el proceso termina con un archivo corrupto la barra sigue.

# Funionalities:
# Todo: Que se descuenten en el conteo los clips corruptos y que solo intente renderizar en base al limite de clips y no a la cantidad archivos.
# Todo: En settings al cambiar a perclip que automaticamente se quite las transiciones y se bloquee el ticket de transiciones.
# Todo: Que en settings se puedan editar varias cosas de la etiqueta de overlay, como el fondo el color, fuente y mas
# Todo: En el overlay si es que un clip estaba corrupto pueden aparecer cosas como clip 1 en el nombre y saltarse a clip 3 por ejemplo.
# Todo: Cuando no se pueda renderizar que muestro un mensaje de error en la interfaz.
# Todo: Agregar metadata al video para saber si ya fue renderizado.
# Todo: Agregar un log de todo lo que ha hecho el programa visible desde la interfaz. Que muestre los mensaje del proceso.
# Todo: Que la fecha salga en el nombre en el formato que el usuario quiera.
# Todo: Opción para poder pausar y reanudar el proceso.
# Todo: Boton en settings para volver a los ajustes predeterminados (cuando hayan mas settings.)
# Todo: Agregar clip limit, para que el usuario pueda seleccionar cuantos clips quiere renderizar.
# Todo: Opción de pasar al siguiente clip en el renderizado.
# Todo: Que el usuario pueda seleccionar el juego según el nombre del clip.
# Todo: Agregar mas parametros en la config como los fps, resolución, etc.
# Todo: Ventana o apartado de configuración para cambiar los parametros de corte, renderizado y limites de los clips.
# Todo: Darle la opción al usuario de convertir los videos a mp3.
# Todo: Usar SQL y de esa forma poder hacer consultas mas complejas y poder continuar el proceso si se cierra la aplicación.

# Possible:
# Todo: Si existe un reporte.csv borrarlo y crear uno nuevo. (Opción de borrarlo para el usuario)
# Todo: Refactorizar renamer y también las ventanas que reciben como parametros en el constructor el objeto slicer y file_manager.