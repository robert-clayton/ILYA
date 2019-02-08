import os, sys, json
import ThemeManager, FileManager
from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *
from TopBar             import TopBar
from FolderList         import FolderList
from ImageList          import ImageList
from ScrollBar          import ScrollBar
from Canvas             import Canvas

class Central(QFrame):
    '''Initializes, styles, and connects the various classes'''

    def __init__(self):
        super().__init__()
        # Initiate objects
        self.overallLayout  = QVBoxLayout(self)
        self.topBar         = TopBar()
        self.contentLayout  = QHBoxLayout()
        self.selectorArea   = QFrame()
        self.selectorLayout = QVBoxLayout(self.selectorArea)
        self.folderArea     = QFrame()
        self.folderLayout   = QHBoxLayout(self.folderArea)
        self.folderList     = FolderList()
        self.folderBar      = ScrollBar(self.folderList)
        self.canvas         = Canvas()
        self.imageArea      = QFrame()
        self.imageList      = ImageList()
        self.imageLayout    = QHBoxLayout(self.imageArea)
        self.imageBar       = ScrollBar(self.imageList)

        # Styling
        self.setStyleSheet('Central { '
                            'background-color: ' + ThemeManager.BG + ';'
                            'border-top-left-radius:     15px;'
                            'border-bottom-left-radius:  15px;'
                            'border-top-right-radius:    15px;'
                            'border-bottom-right-radius: 15px;'
                            'border-width: 0px;'
                            'border-style: solid; }')
        self.overallLayout.setMargin(0)
        self.overallLayout.setSpacing(0)
        self.contentLayout.setAlignment(Qt.AlignCenter)
        self.contentLayout.setMargin(0)        
        self.contentLayout.setSpacing(0)
        self.selectorLayout.setMargin(0)
        self.selectorLayout.setSpacing(0)
        self.folderLayout.setMargin(0)
        self.folderLayout.setSpacing(0)
        self.imageLayout.setMargin(0)
        self.imageLayout.setSpacing(0)
        self.folderList.setVerticalScrollBar(self.folderBar)
        self.imageList.setVerticalScrollBar(self.imageBar)
        self.selectorArea.setMaximumWidth(400)
        self.selectorArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout
        self.folderLayout.addWidget(self.folderList)
        self.folderLayout.addSpacerItem(QSpacerItem(-7, 0))
        self.folderLayout.addWidget(self.folderBar)
        self.imageLayout.addWidget(self.imageList)
        self.imageLayout.addSpacerItem(QSpacerItem(-7, 0))
        self.imageLayout.addWidget(self.imageBar)
        self.selectorLayout.addWidget(self.folderArea, 15)
        self.selectorLayout.addWidget(self.imageArea, 85)
        self.contentLayout.addWidget(self.selectorArea, 30)
        self.contentLayout.addWidget(self.canvas, 70)
        self.overallLayout.addLayout(self.contentLayout)
        self.overallLayout.insertWidget(0, self.topBar)

        # Connections
        self.folderList.selectedFolderChanged.connect(self.populateImageList)
        self.imageList.selectedImageChanged.connect(self.changeCanvasImage)
        self.canvas.deleteRequested.connect(FileManager.deleteImage)

    def populateImageList(self, folder):
        self.imageList.populate(folder)
        self.canvas.setMessage('Switching Folders - {}'.format(folder.data(role=Qt.DisplayRole)))

    def changeCanvasImage(self, image):
        self.canvas.changeImage(image)
        self.canvas.setMessage('Switching Images - {}'.format(image.data(role=Qt.DisplayRole)))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central = Central()
        self.setCentralWidget(central)
        self.setWindowTitle('Label Maker')
        self.setWindowIcon(QIcon(FileManager.iconPath))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()
    