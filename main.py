from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *

import os
import sys
import glob
import configparser
from PIL import Image

class FileManager(QObject):
    def __init__(self):
        super().__init__()
        self.images_folder = 'Images'
        self.labels_folder = 'Labels'
        

class Central(QFrame):
    def __init__(self):
        super().__init__()
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central = Central()
        self.setCentralWidget(central)

        
        

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()