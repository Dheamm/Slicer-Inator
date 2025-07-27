'''Module for the main window of the application. 
This module is responsible to create the render window of the application and start the render thread.'''

# Libraries:
from PyQt5.QtCore import Qt # To set the alignment of the labels.
from PyQt5.QtGui import QIcon # To set the icon.
from PyQt5.QtCore import QSize # To set the size of the icon.


from PyQt5.QtCore import pyqtSignal

# Local Classes:
from Interface.Window import Window # Import Window local class

class SettingsWindow(Window):
    
    settings_applied = pyqtSignal(object)

    def __init__(self, data_json):
        super().__init__(data_json)
        self.__data_json = data_json
        self.config_map = {
            key: {"value": val} for key, val in self.__data_json.items()
            }
        self._setup_ui()

    def _setup_ui(self):
        super().window_settings((400, 1000), 'SlicerInator - Settings')
        self.setWindowIcon(QIcon('Interface/Images/settings.png'))
        
        # Layouts:
        main_layout = super().main_layout_settings()
        secondary_layouts = super().create_secondary_layout(main_layout, 5)

        btn_close = super().button_settings((50, 50), '', 'Press to close the settings window.', font_size=0)
        secondary_layouts[0].addWidget(btn_close, 0, 0, alignment=Qt.AlignLeft)
        btn_close.setIcon(QIcon('Interface/Images/close.png'))
        btn_close.setIconSize(QSize(42, 42))
        btn_close.clicked.connect(lambda: self.close())
        btn_close.clicked.connect(lambda: self.controller.get_render_window().setEnabled(True))

        lbl_title = super().label_settings((200, 60), 'Settings', 'SlicerInator - Settings', font_size=20)
        secondary_layouts[0].addWidget(lbl_title, 0,  0, alignment=Qt.AlignCenter)

        # Proccess Settings:
        lbl_duration = super().label_settings((150, 50), 'Duration/clip:', 'Duration', font_size=10)
        secondary_layouts[1].addWidget(lbl_duration, 1, 0, alignment=Qt.AlignRight)
        lbl_duration.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.txt_duration = super().input_settings((150, 50), 'int', placeholder=f'{self.__data_json.get("duration")}s', tooltip='Set the duration of each clip in seconds.')
        secondary_layouts[1].addWidget(self.txt_duration, 1, 1, alignment=Qt.AlignLeft)


        lbl_clip_limit = super().label_settings((150, 50), 'Clips limit:', 'Clips Limit', font_size=10)
        secondary_layouts[1].addWidget(lbl_clip_limit, 2, 0, alignment=Qt.AlignRight)
        lbl_clip_limit.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.txt_clip_limit = super().input_settings((150, 50), 'int', placeholder=f'{self.__data_json.get("clip_limit")}', tooltip='Set the limit of clips to render.')
        secondary_layouts[1].addWidget(self.txt_clip_limit, 2, 1, alignment=Qt.AlignLeft)

        lbl_transitions = super().label_settings((150, 50), 'Transitions:', 'Transitions', font_size=10)
        secondary_layouts[1].addWidget(lbl_transitions, 3, 0, alignment=Qt.AlignRight)
        lbl_transitions.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.txt_transitions = super().input_settings((150, 50), 'int', placeholder=f'{self.__data_json.get("transitions")}s', tooltip='Set the time of transitions to apply.')
        secondary_layouts[1].addWidget(self.txt_transitions, 3, 1, alignment=Qt.AlignLeft)

        lbl_overlay = super().label_settings((150, 50), 'Overlay:', 'Overlay', font_size=10)
        secondary_layouts[1].addWidget(lbl_overlay, 4, 0, alignment=Qt.AlignRight)
        lbl_overlay.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")
    
        def CurrentIndexChanged(widget, attribute, item_list):
            for i, item in enumerate(item_list):
                if item == attribute:
                    widget.setCurrentIndex(i)
                    break

        overlay_items = ['off','left-top', 'left-center', 'left-bottom', 'center-top', 'center-center', 'center-bottom', 'right-top', 'right-center', 'right-bottom']    
        self.cb_overlay = super().combobox_settings((150, 50), 'Select position of overlay.', overlay_items)
        CurrentIndexChanged(self.cb_overlay, self.__data_json.get("overlay"), overlay_items)
        secondary_layouts[1].addWidget(self.cb_overlay, 4, 1, alignment=Qt.AlignLeft)

        # Output Settings:

        lbl_output_name = super().label_settings((150, 50), 'Output name:', 'Output Name', font_size=10)
        secondary_layouts[2].addWidget(lbl_output_name, 1, 0, alignment=Qt.AlignRight)
        lbl_output_name.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.txt_output_name = super().input_settings((150, 50), 'str', placeholder=f'{self.__data_json.get("output_name")}', tooltip='Set the name of the output file.')
        secondary_layouts[2].addWidget(self.txt_output_name, 1, 1, alignment=Qt.AlignLeft)
        self.txt_output_name.setEnabled(False)  # Disable editing the output name

        lbl_format = super().label_settings((150, 50), 'Format:', 'Format', font_size=10)
        secondary_layouts[2].addWidget(lbl_format, 2, 0, alignment=Qt.AlignRight)
        lbl_format.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        format_items = ['.mp4', '.avi', '.mov', '.mkv', '.flv']
        self.cb_format = super().combobox_settings((150, 50), 'Select the video format.', format_items)
        CurrentIndexChanged(self.cb_format, self.__data_json.get("format"), format_items)
        secondary_layouts[2].addWidget(self.cb_format, 2, 1, alignment=Qt.AlignLeft)

        self.lbl_render_type = super().label_settings((150, 50), 'Render type:', 'Render Type', font_size=10)
        secondary_layouts[2].addWidget(self.lbl_render_type, 3, 0, alignment=Qt.AlignRight)
        self.lbl_render_type.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        render_type_items = ['Compact', 'Separated']
        self.cb_render_type = super().combobox_settings((150, 50), 'Select the render type.', render_type_items)
        CurrentIndexChanged(self.cb_render_type, self.__data_json.get("render_type"), render_type_items)
        self.cb_render_type.setToolTip('Select the render type.' \
        '\nCompact: Render all clips in one video file.' \
        '\nSeparated: Render each clip in a separate video file.')
        self.cb_render_type.setItemData(0, 'Compact: Render all clips in one video file.', Qt.ToolTipRole)
        self.cb_render_type.setItemData(1, 'Separated: Render each clip in a separate video file.', Qt.ToolTipRole)
        secondary_layouts[2].addWidget(self.cb_render_type, 3, 1, alignment=Qt.AlignLeft)
        #tooltip en los items del combobox

        lbl_delete_original = super().label_settings((150, 50), 'Delete original:', 'Delete Original Files', font_size=10)
        secondary_layouts[2].addWidget(lbl_delete_original, 4, 0, alignment=Qt.AlignRight)
        lbl_delete_original.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        delete_original_items = ['on', 'off']
        self.cb_delete_original = super().combobox_settings((150, 50), 'Select whether to delete original files after rendering.', delete_original_items)
        CurrentIndexChanged(self.cb_delete_original, self.__data_json.get("delete_original"), delete_original_items)
        secondary_layouts[2].addWidget(self.cb_delete_original, 4, 1, alignment=Qt.AlignLeft)


        # Video Settings:

        lbl_fps = super().label_settings((150, 50), 'FPS:', 'FPS', font_size=10)
        secondary_layouts[3].addWidget(lbl_fps, 1, 0, alignment=Qt.AlignRight)
        lbl_fps.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.txt_fps = super().input_settings((150, 50), 'int', placeholder=f'{self.__data_json.get("fps")}', tooltip='Set the frames per second of the video.')
        secondary_layouts[3].addWidget(self.txt_fps, 1, 1, alignment=Qt.AlignLeft)

        lbl_bitrate = super().label_settings((150, 50), 'Bitrate:', 'Bitrate', font_size=10)
        secondary_layouts[3].addWidget(lbl_bitrate, 2, 0, alignment=Qt.AlignRight)
        lbl_bitrate.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.txt_bitrate = super().input_settings((150, 50), 'int', placeholder=f'{self.__data_json.get("bitrate")}', tooltip='Set the bitrate of the video in kbps.')
        secondary_layouts[3].addWidget(self.txt_bitrate, 2, 1, alignment=Qt.AlignLeft)

        lbl_threads = super().label_settings((150, 50), 'Threads:', 'CPU-Threads', font_size=10)
        secondary_layouts[3].addWidget(lbl_threads, 3, 0, alignment=Qt.AlignRight)
        lbl_threads.setStyleSheet(f"QLabel {{border: 2px solid lightgrey;}}")

        self.txt_threads = super().input_settings((150, 50), 'int', placeholder=f'{self.__data_json.get("threads")}', tooltip='Set the number of CPU threads to use for rendering.')
        secondary_layouts[3].addWidget(self.txt_threads, 3, 1, alignment=Qt.AlignLeft)

        self.btn_apply = super().button_settings((150, 50), 'Apply', 'Press to apply the settings.', font_size=14)
        self.btn_apply.clicked.connect(lambda: self.apply_settings())
        secondary_layouts[4].addWidget(self.btn_apply, 0, 0, alignment=Qt.AlignCenter)

        assignments = [
            ("duration", self.txt_duration, "lineedit"),
            ("clip_limit", self.txt_clip_limit, "lineedit"),
            ("transitions", self.txt_transitions, "lineedit"),
            ("overlay", self.cb_overlay, "combobox"),
            ("output_name", self.txt_output_name, "lineedit"),
            ("format", self.cb_format, "combobox"),
            ("render_type", self.cb_render_type, "combobox"),
            ("delete_original", self.cb_delete_original, "combobox"),
            ("fps", self.txt_fps, "lineedit"),
            ("bitrate", self.txt_bitrate, "lineedit"),
            ("threads", self.txt_threads, "lineedit")
        ]

        for key, widget, wtype in assignments:
            self.config_map[key]["widget"] = widget
            self.config_map[key]["type"] = wtype

        for key, info in self.config_map.items():
            if "widget" not in info or "type" not in info:
                continue
            widget = info["widget"]
            wtype = info["type"]
            if wtype == "lineedit":
                widget.textChanged.connect(self.check_changes)
            elif wtype == "combobox":
                widget.currentIndexChanged.connect(self.check_changes)

    def open(self):
        self.load_theme(self.__data_json.get('theme'))
        self.enable_apply_button(False)
        self.show()

    def enable_apply_button(self, state):
        self.btn_apply.setEnabled(state)

    def check_changes(self):
        changes = {}

        # {
        # "duration": {"value": 45, "widget": txt_duration, "type": "lineedit"},
        # "overlay": {"value": "off", "widget": cb_overlay, "type": "combobox"},
        # "fps": {"value": 60, "widget": txt_fps, "type": "lineedit"}
        # }

        for key, info_dict in self.config_map.items():
            if "widget" not in info_dict or "type" not in info_dict:
                continue
            widget = info_dict["widget"]
            original_value = str(info_dict["value"])

            if info_dict["type"] == "lineedit":
                current = widget.text().strip()
            elif info_dict["type"] == "combobox":
                current = widget.currentText()
            else:
                continue

            if current != "" and current != original_value:
                changes[key] = current

        self.enable_apply_button(bool(changes)) # if dict is not empty
        self.pending_changes = changes

    def apply_settings(self):
        if not self.pending_changes:
            return  # No changes to apply

        for key, new_value in self.pending_changes.items():
            self.__data_json[key] = new_value
            self.config_map[key]["value"] = new_value

        for key, widget in self.config_map.items():
            if "widget" in widget and "type" in widget:
                if widget["type"] == "lineedit":
                    widget["widget"].setPlaceholderText(str(self.__data_json.get(key)))
                elif widget["type"] == "combobox":
                    widget["widget"].setCurrentText(str(self.__data_json.get(key)))

        self.settings_applied.emit(self.pending_changes) 

        self.pending_changes = {}

        self.enable_apply_button(False)
