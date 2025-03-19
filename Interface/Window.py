# This module has a base methods to each windows.

# Libraries:
from PyQt5.QtWidgets import QMainWindow # To create the main window.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtGui import QFont # To set the font.
from PyQt5.QtWidgets import QToolTip # To set the tooltip.
from PyQt5.QtWidgets import QMessageBox # To show messages.
from PyQt5.QtWidgets import QLineEdit # To create inputs.
from PyQt5.QtGui import QIntValidator # To validate the input.
from PyQt5.QtGui import QDoubleValidator # To validate the input.
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtWidgets import QComboBox # To create comboboxes
from PyQt5.QtWidgets import QCheckBox # To create checkboxes
from PyQt5.QtWidgets import QLabel # To create labels.
from PyQt5.QtGui import QColor

class Window(QMainWindow):
    def window_parameters(self, title, color, width=500, height=250):
        '''Set the window parameters.'''
        self.setWindowTitle(title) # Set the window title
        self.setFixedSize(width, height) # Set fixed size
        self.setStyleSheet(f"background-color: {color}") # Set the background color

    def button_config(self, geometry:tuple[int,int,int,int], text, background_color, font, font_size, tooltip_text, style='', bold=True):
        '''Method to configure the buttons.'''
        btn = QPushButton(text, self) # Create the button
        btn.setGeometry(*geometry)

        color = QColor(background_color)

        btn.setStyleSheet(f""" 
                        background-color: {background_color};
                        border-radius: {geometry[3] / 2}px; /* Circle */
                        border: 2px solid {color.darker(130).name()};
                        {style}
                        """)

        btn.setFont(QFont(font, font_size, QFont.Bold if bold else QFont.Normal)) # Set the font

        QToolTip.setFont(QFont('Arial', 10, QFont.Bold)) # Set the tooltip font
        btn.setToolTip(tooltip_text) # Set the tooltip
        return btn
    
    def show_message(self, title, message):
        '''Show a message box.'''
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec_()

    def input_config(self, geometry:tuple[int,int,int,int], validator:str=None, placeholder:str=None, tooltip:str=None):
        '''Method to configure the inputs.'''
        txt = QLineEdit(self)
        txt.setGeometry(*geometry) # '*' unpacks the tuple.
        txt.setStyleSheet("background-color: white; color: black; border: 1px solid black; border-radius: 5px;")
        txt.setPlaceholderText(placeholder)
        txt.setToolTip(tooltip)

        # Set Validator:
        if validator == 'int':
            # Only integers.
            txt.setValidator(QIntValidator())
        elif validator == 'float':
            # Only floats.
            txt.setValidator(QDoubleValidator())
        elif validator == 'str':
            # Only letters.
            regex_str = QRegularExpression("^[A-Za-zÁÉÍÓÚáéíóúñÑ]+$") 
            txt.setValidator(QRegularExpressionValidator(regex_str, self))
        elif validator == None:
            # Default: Any input.
            pass

        return txt
    
    def combobox_config(self, geometry:tuple[int,int,int,int], tooltip:str=None, items:list[str]=[]):
        '''Method to configure the comboboxes.'''
        cb = QComboBox(self)
        cb.setGeometry(*geometry)
        cb.setStyleSheet("background-color: white; color: black; border: 1px solid black; border-radius: 5px;")
        cb.addItems(items)
        cb.setToolTip(tooltip)

        font = QFont('Arial', 8, QFont.Bold)
        cb.setFont(font)
        return cb
    
    def checkbox_config(self, geometry:tuple[int,int,int,int], tooltip:str=None):
        '''Method to configure the checkboxes.'''
        cb = QCheckBox(self)
        cb.setGeometry(*geometry)
        cb.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px; 
                height: 20px; 
                border-radius: 10px; /* Circle */
                border: 2px solid black;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: lightblue;
                border: 2px solid black;
            }
        """)
        cb.setToolTip(tooltip)
        return cb

    def label_config(self, geometry:tuple[int,int,int,int], text:str, tooltip:str=None, style:str=None):
        '''Method to configure the labels.'''
        lbl = QLabel(text, self)
        lbl.setGeometry(*geometry)
        lbl.setStyleSheet(style)
        lbl.setToolTip(tooltip)
        return lbl