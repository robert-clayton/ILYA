#!/usr/bin/env python3
import ThemeManager
from PySide2.QtCore     import  Signal, Qt, QPointF
from PySide2.QtGui      import  QIcon, QColor
from PySide2.QtWidgets  import  QFrame, QVBoxLayout, QHBoxLayout, QMainWindow, QApplication, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect, QWidget
from TopBar             import  TopBar
from FolderList         import  FolderList
from ImageList          import  ImageList
from ScrollBar          import  ScrollBar
from Canvas             import  Canvas
from BoxManager         import  BoxManager

class Central(QFrame):
    '''Initializes, styles, and connects the various classes'''

    def __init__(self):
        super().__init__()
        # Objects
        self.dropShadow     = QGraphicsDropShadowEffect(self)
        self.boxManager     = BoxManager()
        self.overallLayout  = QVBoxLayout(self)
        self.topBar         = TopBar()
        self.contentLayout  = QHBoxLayout()
        self.selectorArea   = QFrame()
        self.selectorLayout = QVBoxLayout(self.selectorArea)
        self.folderArea     = QFrame()
        self.folderLayout   = QHBoxLayout(self.folderArea)
        self.folderList     = FolderList()
        self.folderBar      = ScrollBar(self.folderList)
        self.canvas         = Canvas(self.boxManager)
        self.imageArea      = QFrame()
        self.imageList      = ImageList()
        self.imageLayout    = QHBoxLayout(self.imageArea)
        self.imageBar       = ScrollBar(self.imageList)

        # Styling
        self.setStyleSheet('Central { background: transparent; }')
        self.overallLayout.setMargin(20)
        self.dropShadow.setOffset(QPointF(0,4))
        self.dropShadow.setColor(QColor(0,0,0,100))
        self.dropShadow.setBlurRadius(10)
        self.setGraphicsEffect(self.dropShadow)
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
        self.folderList.selectedFolderChanged.connect(self.handleSelectedFolderChanged)
        self.imageList.selectedImageChanged.connect(self.handleSelectedImageChanged)

    def handleSelectedFolderChanged(self, folder):
        self.imageList.populate(folder)
        self.canvas.changeImage(None)
        self.canvas.setMessage('Switching Folders - {}'.format(folder.data(role=Qt.DisplayRole)))
        self.topBar.setSelectedFolder(str(folder.data(role=Qt.UserRole+1)))
        self.topBar.setSelectedImage('')

    def handleSelectedImageChanged(self, image):
        self.canvas.changeImage(image)
        self.canvas.setMessage('Switching Images - {}'.format(image.data(role=Qt.DisplayRole)))
        self.topBar.setSelectedImage(str(image.data(role=Qt.DisplayRole)))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central = Central()
        self.setCentralWidget(self.central)
        self.setWindowTitle('Label Maker')
        self.setWindowIcon(QIcon(ThemeManager.ICON_PATH))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def closeEvent(self, event):
        self.central.boxManager.saveDataFrame()
        super().closeEvent(event)

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()
    
