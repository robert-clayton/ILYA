from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *

import os, sys, json
from PIL import Image
from FolderList import FolderList
from FlowLayout import FlowLayout
from FileManager import FileManager

file_manager = FileManager()


class ImageViewer(QFrame):
    def __init__(self, image = None):
        super().__init__()
        self.setMinimumSize(QSize(850, 725))
        self.image = QPixmap(image)
        self.setStyleSheet('ImageViewer { background: rgb(50,50,50); }')

    def paintEvent(self, event):
        scaled_image = self.image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        source = scaled_image.size()
        target = self.size()


        self.dx = target.width() - source.width() if target.width() - source.width() else source.width() - target.width()
        self.dy = target.height() - source.height() if target.height() - source.height() else source.height() - target.height()

        painter = QPainter(self)
        painter.drawPixmap(self.dx / 2, self.dy / 2, scaled_image)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.end()

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)

class Central(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('Central { background: rgb(30,30,30); }')
        self.layout                 = QHBoxLayout(self)
        self.folder_images_layout   = FlowLayout()
        self.focused_image          = ImageViewer('C:\\Users\\draug\\Desktop\\floof.png')
        self.folder_list            = FolderList(file_manager.get_images_folders())
        self.folder_list.setMaximumWidth(300)
        
        self.layout.addLayout(self.folder_images_layout)
        self.layout.addWidget(self.focused_image)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.folder_list)

        self.folder_list.selectedChanged.connect(self.tell)

    def tell(self, param):
        print(param.data(data=Qt.UserRole))

    def fill_images_layout(self, folder):
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central = Central()
        self.setCentralWidget(central)
        self.setWindowTitle('Label Maker')
        self.setWindowIcon(QIcon(os.path.join(file_manager.current_dir, 'logo.ico')))

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()