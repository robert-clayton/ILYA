from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *

import os
import sys
import glob
import configparser
from PIL import Image

CONFIG_FILE     = 'config.ini'
IMAGES_FOLDER   = 'Images'


class Config(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.read(CONFIG_FILE)
        
    def save(self):
        with open(CONFIG_FILE, 'w') as cf:
            self.write(cf)
            
    def reload(self):
        self.read(CONFIG_FILE)
    
    def set_mode(self, param):
        self[] = val
        self.keyChanged.emit(param)    

    keyChanged = PyObject(object)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = Config()
        

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()