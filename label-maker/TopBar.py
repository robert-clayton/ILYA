import os
import ThemeManager
from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *

class TopBar(QFrame):
    '''Interactable bar at the top of the application'''
    def __init__(self):
        super().__init__()
        # Variables
        self.mouseMovePos       = self.window().pos()
        self.mousePressPos      = self.window().pos()
        self.draggingThreshold  = 5
        self.selectedFolder     = ''
        self.selectedImage      = ''
        
        # Objects
        self.dropShadow     = QGraphicsDropShadowEffect(self)
        self.icon           = QLabel()
        self.iconReader     = QImageReader()
        self.title          = QLabel()
        self.minimize       = Button('Minimize')
        self.close          = Button('Close')
        self.layout         = QHBoxLayout(self)

        # Layout
        self.layout.addWidget(self.icon, alignment=Qt.AlignLeft)
        self.layout.addStretch(1)
        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)
        self.layout.addStretch(1)
        self.layout.addWidget(self.minimize, alignment=Qt.AlignRight)
        self.layout.addWidget(self.close, alignment=Qt.AlignRight)

        # Styling
        self.setStyleSheet('TopBar { '
                            'background: ' + ThemeManager.TOP_BAR + ';'
                            'border-top-left-radius:     15px;'
                            'border-top-right-radius:    15px;'
                            'border-width: 0px;'
                            'border-style: solid; }')
        self.setMinimumHeight(35)
        self.iconReader.setScaledSize(QSize(20,20))
        self.iconReader.setFileName(ThemeManager.ICON_PATH)
        self.icon.setPixmap(QPixmap.fromImage(self.iconReader.read()))
        self.title.setStyleSheet('color: ' + ThemeManager.ACCENT + ';')
        self.dropShadow.setOffset(QPointF(0,5))
        self.dropShadow.setColor(QColor(30,30,30,100))
        self.dropShadow.setBlurRadius(10)
        self.setGraphicsEffect(self.dropShadow)
        self.layout.setContentsMargins(20,0,20,0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignVCenter)
    
    def setSelectedFolder(self, param):
        self.selectedFolder = str(param)
        self.updateTitle()
    
    def setSelectedImage(self, param):
        self.selectedImage = str(param)
        self.updateTitle()
    
    def updateTitle(self):
        if self.selectedFolder:
            self.title.setText('./' + self.selectedFolder + '/' + self.selectedImage)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressPos = self.window().pos()
            self.mouseMovePos = event.globalPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        moveDist = (event.globalPos() - self.mouseMovePos).manhattanLength()
        if moveDist > self.draggingThreshold:
            self.window().move(self.mousePressPos + event.globalPos() - self.mouseMovePos)
        super().mouseMoveEvent(event)

class Button(QFrame):
    '''Holds the various functionality requirements a top bar's button would need'''
    def __init__(self, buttonType):
        super().__init__()
        # Variables
        self.buttonType = buttonType

        # Objects
        self.layout = QHBoxLayout(self)
        self.label = QLabel(buttonType)
        
        # Layout
        self.layout.addWidget(self.label)

        # Styling
        self.layout.setMargin(0)
        self.label.setFont(QFont('Arial', 9, QFont.Bold))
        self.label.setStyleSheet('color: ' + ThemeManager.LABEL + ';')

    def enterEvent(self, event):
        self.label.setStyleSheet('color: ' + ThemeManager.ACCENT + ';')
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.label.setStyleSheet('color: ' + ThemeManager.LABEL + ';')
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.buttonType == 'Minimize':
            self.window().showMinimized()
        elif self.buttonType == 'Close':
            self.window().close()