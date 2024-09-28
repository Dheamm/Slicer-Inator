import os #Para manejar rutas.
from Logica.GestorArchivos import GestorArchivos #Importar clase GestorArchivos.
from moviepy.editor import VideoFileClip

class Cortador(GestorArchivos):
    '''Proceso de cortar los clips.'''
    def __init__(self, ruta_clips, formatos_clip, duracion_clip):
        super().__init__(ruta_clips, formatos_clip)
        self.__duracion_clip = duracion_clip


    def __cortar_clip(self, ruta_entrada, archivos_validos):
        '''Cortar el clip.'''
        for archivo in archivos_validos:
            clip_original = VideoFileClip(os.path.join(ruta_entrada, archivo)) #Se carga el clip original.

            # SE RECORTA EL CLIP (SE MANTIENEN LOS SEGUNDOS FINALES).
            duracion_total = clip_original.duration # Duracion total del clip.
            tiempo_inicio = max(0, duracion_total - (self.__duracion_clip)) # Se consigue el tiempo antes de duracion clip.
            clip_recortado = clip_original.subclip(tiempo_inicio, duracion_total) # Desde el tiempo de inicio hasta el final.

        return clip_recortado


    def __renderizar_clip(self, clip_recortado):
        '''Renderizar el clip.'''
        salida = os.path.join(super().mostrar_valores('get_salida'), 'jose' + '.mp4') # Se guarda el clip recortado en la ruta de salida.
        clip_recortado.write_videofile(salida, # Se guarda el clip recortado en la ruta de salida.
                                    codec="libx264",
                                    fps=60,
                                    threads=4,
                                    audio_codec="aac",
                                    ffmpeg_params=["-vcodec", "h264_nvenc"],
                                    bitrate="16000k")


    def proceso_corte(self, tipo):
        '''Llamar al corteador de clips.'''
        if tipo == 'cortar':
            self.__renderizar_clip(
                self.__cortar_clip(
                    super().mostrar_valores('get_ruta'), super().mostrar_valores('archivos_validos')))
        else:
            raise ValueError('Error! Tipo de parámetro no válido. Intente nuevamente.')