# This module has a base methods to each windows.

# Libraries:
from PyQt5.QtWidgets import QMainWindow # To create the main window.
from PyQt5.QtWidgets import QPushButton # To create buttons.
from PyQt5.QtGui import QFont # To set the font.
from PyQt5.QtWidgets import QToolTip # To set the tooltip.
from PyQt5.QtWidgets import QMessageBox # To show messages.

class Window(QMainWindow):
    def window_parameters(self, title, color, width=500, height=250):
        '''Set the window parameters.'''
        self.setWindowTitle(title) # Set the window title
        self.setFixedSize(width, height) # Set fixed size
        self.setStyleSheet(f"background-color: {color}") # Set the background color

    def button_config(self, text, background_color, font, font_size, tooltip_text, style='', bold=True):
        '''Method to configure the buttons.'''
        btn = QPushButton(text, self) # Create the button
        btn.setStyleSheet(f"background-color: {background_color}; {style}") # Set the background color
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