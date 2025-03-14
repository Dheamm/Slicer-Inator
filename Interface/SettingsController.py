class SettingsController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, 
                clips_limit:int=10000,
                show_transition:bool=True, 
                show_overlay:bool=True, 
                render_per_clip:bool=False):
        self.__clips_limit = clips_limit
        self.__show_transition = show_transition
        self.__show_overlay = show_overlay
        self.__render_per_clip = render_per_clip

    def get_clips_limit(self):
        '''Get the limit of clips.'''
        return self.__clips_limit
    
    def set_clips_limit(self, new_limit:int):
        '''Set the limit of clips.'''
        self.__clips_limit = new_limit

    def get_show_transition(self):
        '''Get the status of the transitions.'''
        return self.__show_transition
    
    def set_show_transition(self, new_status:bool):
        '''Set the status of the transitions.'''
        self.__show_transition = new_status

    def get_show_overlay(self):
        '''Get the status of the overlay text.'''
        return self.__show_overlay
    
    def set_show_overlay(self, new_status:bool):
        '''Set the status of the overlay text.'''
        self.__show_overlay = new_status

    def get_render_per_clip(self):
        '''Get the status of the per clip.'''
        return self.__render_per_clip
    
    def set_render_per_clip(self, new_status:bool):
        '''Set the status of the per clip.'''
        self.__render_per_clip = new_status
