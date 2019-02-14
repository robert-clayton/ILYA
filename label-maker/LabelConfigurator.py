import ThemeManager
from PySide2.QtWidgets import QFrame, QVBoxLayout
from PySide2.QtCore import Signal, QSize, Qt
from PySide2.QtGui import QImageReader, QPainter, QPen, QFont, QPixmap, QFontMetrics

class LabelConfigurator(QFrame):
    def __init__(self, boxManager):
        super().__init__()
        # Objects
        self.boxManager         = boxManager
        self.layout             = QVBoxLayout(self)
        self.isOccludedButton   = Check('Occluded', False)
        self.isTruncatedButton  = Check('Truncated', False)
        self.isGroupOfButton    = Check('Group Of', False)
        self.isDepictionButton  = Check('Depiction', False)
        self.isInsideButton     = Check('Inside', False)

        # Layout
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.isOccludedButton)
        self.layout.addWidget(self.isTruncatedButton)
        self.layout.addWidget(self.isGroupOfButton)
        self.layout.addWidget(self.isDepictionButton)
        self.layout.addWidget(self.isInsideButton)

        # Styling
        self.layout.setContentsMargins(5,10,5,10)
        self.layout.setSpacing(15)

        # Connections
        self.isOccludedButton.stateChanged.connect(boxManager.setNewBoxIsOccluded)
        self.isTruncatedButton.stateChanged.connect(boxManager.setNewBoxIsTruncated)
        self.isGroupOfButton.stateChanged.connect(boxManager.setNewBoxIsGroupOf)
        self.isDepictionButton.stateChanged.connect(boxManager.setNewBoxIsDepiction)
        self.isInsideButton.stateChanged.connect(boxManager.setNewBoxIsInside)

class Check(QFrame):
    def __init__(self, name, default = False):
        super().__init__()
        # Variables
        self.name    = name
        self.hovered = False
        self.enabled = default
        self.padding = 5

        # Objects
        self.image = QImageReader()
        self.imageSize = QSize(20,20)

        # Styling
        self.font = QFont('Arial', 8)
        self.font.setWeight(QFont.Bold)
        self.nameHeight = QFontMetrics(self.font).height()
        self.nameWidth = QFontMetrics(self.font).width(self.name)
        
        self.image.setScaledSize(self.imageSize)
        self.setFixedSize(self.imageSize.width() + self.padding + self.nameWidth, self.imageSize.height())
    
    def setPadding(self, param):
        self.padding = param
        self.update()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.hovered = False
        self.update()
    
    def mouseReleaseEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.enabled = not self.enabled
            self.stateChanged.emit(self.enabled)
            self.update()

    def paintEvent(self, event):
        # Set checked depending on state
        self.image.setFileName(ThemeManager.CHECKED_PATH if self.enabled else ThemeManager.UNCHECKED_PATH)
        
        # Init painter and draw image at correct location
        painter = QPainter(self)
        pixmap = QPixmap.fromImageReader(self.image)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.drawPixmap(0, (self.height() - pixmap.height()) / 2, pixmap)

        # Style font and draw text at correct location
        painter.setFont(self.font)
        pen = QPen()
        pen.setColor(ThemeManager.LABEL_QC if any([self.hovered, self.enabled]) else ThemeManager.LABEL_LOW_OPACITY_QC)
        painter.setPen(pen)
        painter.drawText(pixmap.width() + self.padding, self.height() / 2 + self.nameHeight / 4, self.name)
    
    stateChanged = Signal(object)