from pathlib import Path
from PyQt5.QtWidgets import QApplication
import json

class JsonCreator():
    def __init__(self, config_path='config.json'):
        self.__config_path = config_path

    def get_config_path(self):
        return self.__config_path
    
    def set_config_path(self, config_path):
        self.__config_path = config_path

    def create_json(self):
        path = Path(self.get_config_path())
        if not path.exists():
            # Create json wth defaul values
            default_data = {
            "theme": "dark",
            "font": "Arial",

            "duration": 45,
            "clip_limit": 10,
            "transitions": 3,
            "overlay": "off",

            "output_name": "compact_video",
            "format": ".mp4",
            "render_type": "compact",

            "fps": 60,
            "bitrate": 16000,
            "threads": 4
        }

            path.write_text(json.dumps(default_data, indent=4))

    def get_full_json(self):
        path = Path(self.get_config_path())
        if not path.exists():
            return None

        try:
            data = json.loads(path.read_text())
            return data
        except json.JSONDecodeError:
            return None

    def get_json(self, key, config_path='config.json'):
        path = Path(config_path)
        if not path.exists():
            return None

        try:
            data = json.loads(path.read_text())
            return data.get(key)
        except json.JSONDecodeError:
            return None
        
    def set_json(self, key, value, config_path='config.json'):
        path = Path(config_path)

        if path.exists():
            try:
                data = json.loads(path.read_text())
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

        data[key] = value
        path.write_text(json.dumps(data, indent=4))
