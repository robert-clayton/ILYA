import os, sys, json
from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *
from FolderList         import FolderList
from ImageList          import ImageList
from Canvas             import Canvas
from FileManager        import FileManager as fm

class Central(QFrame):
    def __init__(self):
        super().__init__()
        # Initiate objects
        self.layout         = QHBoxLayout(self)
        self.focused_image  = Canvas(image='C:\\Users\\draug\\Desktop\\floof.png')
        self.image_list     = ImageList()
        self.folder_list    = FolderList(fm().get_images_folders())

        # Styling
        self.setStyleSheet('Central { background: rgb(30,30,30); }')
        self.folder_list.setMaximumWidth(300)
        
        # Layout
        self.layout.addWidget(self.image_list, 20)
        self.layout.addWidget(self.focused_image, 60)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.folder_list, 20)

        # Connections
        self.folder_list.currentRowChanged.connect(self.image_list.populate)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central = Central()
        self.setCentralWidget(central)
        self.setWindowTitle('Label Maker')
        self.setWindowIcon(QIcon(os.path.join(fm.current_dir, 'logo.ico')))

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()