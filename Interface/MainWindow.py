import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def window_parameters(self, title="Slicer Inator", width=500, height=250, color='lightgrey'):
        '''Set the window parameters.'''
        self.setWindowTitle(title) # Set the window title
        self.setFixedSize(width, height) # Set fixed size
        self.setStyleSheet(f"background-color: {color};")

    def main_window(self, start):
        self.window_parameters()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)      

        # Title Label:
        lbl_title = QLabel("Slicer Inator", self) # Create a label
        lbl_title.setStyleSheet("font-weight: bold; font-size: 30px;") # Set the label style
        lbl_title.setGeometry(160, 20, 200, 70)

        # Start Button:
        btn_start = QPushButton("Start", self)
        btn_start.setStyleSheet("background-color: lightblue; font-weight: bold; font-size: 16px;")
        btn_start.setGeometry(155, 100, 200, 50)
        btn_start.clicked.connect(start) # Start the new window.
        btn_start.clicked.connect(self.hide) # Hide last window.

        # Exit Button:
        btn_exit = QPushButton("Exit", self)
        btn_exit.setStyleSheet("background-color: lightcoral; font-weight: bold; font-size: 16px;")
        btn_exit.setGeometry(230, 160, 50, 30)
        btn_exit.clicked.connect(self.close)

        self.show() # Show the window