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
        self.overall_layout = QHBoxLayout(self)
        self.selector_layout= QVBoxLayout()
        self.focused_image  = Canvas(image='C:\\Users\\draug\\Desktop\\floof.png')
        self.image_list     = ImageList()
        self.folder_list    = FolderList(fm().get_images_folders())

        # Styling
        self.setStyleSheet('Central { background: rgb(30,30,30); }')
        self.folder_list.setMaximumWidth(300)
        self.overall_layout.setAlignment(Qt.AlignCenter)
        self.overall_layout.setMargin(0)
        self.overall_layout.setSpacing(0)

        # Layout
        self.selector_layout.addWidget(self.folder_list, 20)
        self.selector_layout.addWidget(self.image_list, 80)
        self.overall_layout.addLayout(self.selector_layout, 30)
        self.overall_layout.addWidget(self.focused_image, 70)

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