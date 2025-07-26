# Libraries:
from PyQt5.QtWidgets import QMainWindow # To create the main window.
from PyQt5.QtWidgets import QWidget # To create a widget.
from PyQt5.QtWidgets import QVBoxLayout # To create a vertical layout.
from PyQt5.QtWidgets import QGridLayout # To create a grid layout.
from PyQt5.QtCore import Qt # To set the alignment of the widgets.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtGui import QFont # To set the font.
from PyQt5.QtWidgets import QToolTip # To set the tooltip.
from PyQt5.QtWidgets import QLineEdit # To create inputs.
from PyQt5.QtGui import QIntValidator # To validate the input.
from PyQt5.QtGui import QDoubleValidator # To validate the input.
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtWidgets import QComboBox # To create comboboxes
from PyQt5.QtWidgets import QCheckBox # To create checkboxes
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtGui import QColor # To set the color.
from PyQt5.QtWidgets import QProgressBar # To create progress bars.
from PyQt5.QtCore import pyqtSignal

class Window(QMainWindow):
    def __init__(self, data_json):
        super().__init__()
        self.__data_json = data_json

        # Central Widget:
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

    def set_controller(self, controller):
        self.controller = controller

    def font_settings(self, font_size:int, bold:bool=True):
        return QFont(self.__data_json.get("font"), font_size, QFont.Bold if bold else QFont.Normal)

    def tooltip_settings(self, font_size:int=8, bold:bool=False):
        QToolTip.setFont(self.font_settings(font_size, bold))

    def load_theme(self, theme):
        with open(f"Themes\\{theme}.qss", "r") as file:
            self.setStyleSheet(file.read())

    def window_settings(self, geometry:tuple[int,int], title:str):
        # screen_geometry = self.screen().geometry() # Get the screen geometry.
        # x = (screen_geometry.width() - geometry[0]) // 2 # Center the window horizontally.
        # y = (screen_geometry.height() - geometry[1]) // 2 # Center the window vertically.
        # self.setGeometry(x, y, *geometry)

        self.setFixedSize(*geometry)
        self.setWindowTitle(title)
        self.tooltip_settings()
        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowMinimizeButtonHint)

    def main_layout_settings(self, margins_geometry:tuple[int,int,int,int]=(20,0,20,0), spacing:int=0):
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(*margins_geometry)
        main_layout.setSpacing(spacing)

        return main_layout


    def create_secondary_layout(self, main_layout, number:int):
        horizontal_layouts = []
        for i in range(number):
            widget = QWidget()
            layout = QGridLayout(widget)
            layout.setContentsMargins(20, 10, 20, 10)
            layout.setSpacing(10)

            horizontal_layouts.append(layout)
            if i != (0):
                if i != (number - 1):
                    widget.setObjectName(f'border_widget')

                    widget.setStyleSheet(f"""
                    QWidget {{
                        border-radius: 10px;  /* Round Borders */
                        padding: 10px;        /* Space between content */
                    }}""")

            main_layout.addWidget(widget)
            main_layout.setStretch(i, 1)

        return horizontal_layouts
    
    def label_settings(self, geometry:tuple[int,int], text:str, tooltip:str, font_size:int, style='', bold=True):
        lbl = QLabel(text)
        lbl.setFixedSize(*geometry)
        lbl.setFont(self.font_settings(font_size, bold))
        lbl.setToolTip(tooltip)
        lbl.setAlignment(Qt.AlignCenter)

        return lbl

    def button_settings(self, geometry:tuple[int,int], text:str, tooltip_text:str, font_size:int, style='', bold=True):
        btn = QPushButton(text)
        btn.setFixedSize(*geometry)
        btn.setFont(self.font_settings(font_size, bold)) # Set the font
        btn.setToolTip(tooltip_text) # Set the tooltip

        # Colors:
        # quiero este color #65ABFF

        background_color = QColor(101, 171, 255) # Light blue color
        hover_color = background_color.lighter(130).name() # Darker color
        push_color = background_color.darker(130).name() # Lighter color


        btn.setStyleSheet(f"""
                    QPushButton {{
                        border-radius: {geometry[1] / 2}px; /* Circle */
                        padding: 0px;
                        margin: 0px;}}""")
        

        return btn
    
    def progress_bar_settings(self, geometry:tuple[int,int,int,int], tooltip:str=None):
        pbar = QProgressBar()
        pbar.setFixedSize(*geometry)
        pbar.setRange(0, 100)
        pbar.setToolTip(tooltip)
        pbar.setStyleSheet(f"""
        QProgressBar {{
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 20px;
            padding: 2px;
        }}

        QProgressBar::chunk {{
            border-radius: 10px;
        }}
        """)

        return pbar
    
    def input_settings(self, geometry:tuple[int,int], validator:str=None, placeholder:str=None, tooltip:str=None):
        '''Method to configure the inputs.'''
        txt = QLineEdit(self)
        txt.setFixedSize(*geometry)
        txt.setStyleSheet("""
        QLineEdit {
            border-radius: 5px;
            font-family: Arial;
            font-size: 14px;
            font-weight: bold;
        }
        QLineEdit::placeholder {
            font-family: Arial;
            font-size: 14px;
            font-weight: bold;
        }
    """)
        txt.setPlaceholderText(placeholder)
        txt.setToolTip(tooltip)

        # Set Validator:
        if validator == 'int':
            txt.setValidator(QIntValidator())
        elif validator == 'float':
            txt.setValidator(QDoubleValidator())
        elif validator == 'str':
            regex_str = QRegularExpression("^[A-Za-zÁÉÍÓÚáéíóúñÑ]+$") 
            txt.setValidator(QRegularExpressionValidator(regex_str, self))
        elif validator == None:
            pass

        return txt

    def combobox_settings(self, geometry:tuple[int,int], tooltip:str=None, items:list[str]=[]):
        '''Method to configure the comboboxes.'''
        cb = QComboBox(self)
        ruta_imagen = r"C:\Users\Dheam\Downloads\down.png"
        ruta_imagen = ruta_imagen.replace("\\", "/")

        cb.setFixedSize(*geometry)
        cb.setStyleSheet(f"""
        QComboBox {{
            border-radius: 5px;
            padding: 2px 10px 2px 10px;
            font-family: Arial;
            font-size: 12px;
        }}
        QComboBox::drop-down {{
            width: 25px;
            border: 2px;
        }}
        QComboBox::down-arrow {{
            image: url({ruta_imagen});
            width: 16px;
            height: 16px;}}
            
        QComboBox QAbstractItemView {{
        border-radius: 5px;
        padding: 5px;}}""")

        cb.addItems(items)
        cb.setToolTip(tooltip)

        font = QFont('Arial', 8, QFont.Bold)
        cb.setFont(font)
        return cb

    def checkbox_config(self, geometry:tuple[int,int], tooltip:str=None):
        '''Method to configure the checkboxes.'''
        cb = QCheckBox(self)
        cb.setGeometry(*geometry)
        cb.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px; 
                height: 20px; 
                border-radius: 10px; /* Circle */
            }
        """)
        cb.setToolTip(tooltip)
        return cb