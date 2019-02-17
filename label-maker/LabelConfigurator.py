import ThemeManager, ListDelegate
from PySide2.QtWidgets  import  QFrame, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListView
from PySide2.QtCore     import  Signal, QSize, Qt, QStringListModel
from PySide2.QtGui      import  QImageReader, QPainter, QPen, QFont, QPixmap, QFontMetrics

class LabelConfigurator(QDialog):
    def __init__(self, boxManager, spawnPos):
        super().__init__()
        # Variables
        self.spawnPos           = spawnPos

        # Objects
        self.boxManager         = boxManager
        self.layout             = QVBoxLayout(self)
        self.topLayout          = QHBoxLayout()
        self.settingsLayout     = QHBoxLayout()
        self.title              = QLabel('Label Configurator')
        self.isOccludedButton   = Check('Occluded',     boxManager.getRecentIsOccluded())
        self.isTruncatedButton  = Check('Truncated',    boxManager.getRecentIsTruncated())
        self.isGroupOfButton    = Check('Group Of',     boxManager.getRecentIsGroupOf())
        self.isDepictionButton  = Check('Depiction',    boxManager.getRecentIsDepiction())
        self.isInsideButton     = Check('Inside',       boxManager.getRecentIsInside())
        self.cancelButton       = QPushButton('Cancel')
        self.labelsModel        = QStringListModel()
        self.labelsView         = QListView()

        # Layout
        self.setWindowFlags(Qt.Popup)
        self.settingsLayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.settingsLayout.setMargin(0)
        self.settingsLayout.addWidget(self.isOccludedButton)
        self.settingsLayout.addWidget(self.isTruncatedButton)
        self.settingsLayout.addWidget(self.isGroupOfButton)
        self.settingsLayout.addWidget(self.isDepictionButton)
        self.settingsLayout.addWidget(self.isInsideButton)
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.cancelButton)
        self.layout.addLayout(self.topLayout)
        self.layout.addWidget(self.labelsView)
        self.layout.addLayout(self.settingsLayout)

        # Styling
        self.setStyleSheet('LabelConfigurator { '
                            'background-color: ' + ThemeManager.BG_L1 + ';'
                            'border-top-left-radius:     ' + str(ThemeManager.CURVE) + 'px;'
                            'border-bottom-left-radius:  ' + str(ThemeManager.CURVE) + 'px;'
                            'border-top-right-radius:    ' + str(ThemeManager.CURVE) + 'px;'
                            'border-bottom-right-radius: ' + str(ThemeManager.CURVE) + 'px;'
                            'border-width: 0px;'
                            'border-style: solid;'
                            '}')
        self.layout.setContentsMargins(5,10,5,10)
        self.layout.setSpacing(15)
        self.labelsModel.setStringList(boxManager.loadLabels())
        self.labelsView.setStyleSheet('QListView { '
            'background: transparent;'
            '}')
        self.labelsView.setFrameStyle(QFrame.NoFrame)
        self.labelsView.setModel(self.labelsModel)
        self.labelsView.setItemDelegate(ListDelegate.ListDelegate())
        
        index = None
        try:
            row     = self.labelsModel.stringList().index(boxManager.getRecentLabelName())
            index   = self.labelsModel.index(row)
        except ValueError:
            index   = self.labelsModel.index(0)
        if index is not None:
            self.labelsView.setCurrentIndex(index)

        # Connections
        self.cancelButton.clicked.connect(self.reject)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.move(self.spawnPos)

    def closeEvent(self, event):
        labelConfig = (self.labelsView.selectedIndexes()[0].data(role=Qt.DisplayRole), 
                        self.isOccludedButton.getEnabled(), 
                        self.isTruncatedButton.getEnabled(), 
                        self.isGroupOfButton.getEnabled(), 
                        self.isDepictionButton.getEnabled(), 
                        self.isInsideButton.getEnabled())
        self.labelAccepted.emit(labelConfig)
        super().closeEvent(event)
    
    labelAccepted = Signal(object)

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
    
    def getEnabled(self):
        return self.enabled
    
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