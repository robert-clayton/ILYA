from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *
from Box                import Box
import ThemeManager
from DeletePopup        import ConfirmDelete

class Canvas(QFrame):
    MIN_BOX_SIZE = 0.0025 # percent of image

    def __init__(self, labelName = 'Default', imageData = None):
        super().__init__()
        # Variables
        self.message = ''
        self.messageResetTimer = QTimer()
        self.labelName = labelName
        self.imageData = imageData
        self.drawnRects  = []
        self.drawingRect = None
        self.drawing = False

        # Objects
        self.image = QPixmap(imageData.data(role=Qt.DisplayRole)) if imageData else None

        # Styling
        self.setMinimumSize(QSize(850, 725))
        self.setStyleSheet('Canvas { '
            'background-color: rgba(50,50,50,255);'
            'border-bottom-right-radius: 15px;'
            '}')
        self.messageResetTimer.setInterval(3000)
        self.messageResetTimer.setSingleShot(True)
        
        # Connections
        self.messageResetTimer.timeout.connect(self.resetMessage)

    def setMessage(self, param):
        self.message = param
        self.update()
        self.messageResetTimer.start()

    def resetMessage(self):
        self.message = ''
        self.update()

    def changeImage(self, newImageIndex):
        self.imageData = newImageIndex
        self.image = QPixmap(newImageIndex.data(role=Qt.UserRole))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # If image is set
        if self.image:
            # Scale image down
            self.scaledImage = self.image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Find xy offsets
            self.dx = self.size().width()  - self.scaledImage.size().width()  if self.size().width()  - self.scaledImage.size().width()  else self.scaledImage.size().width()  - self.size().width()
            self.dy = self.size().height() - self.scaledImage.size().height() if self.size().height() - self.scaledImage.size().height() else self.scaledImage.size().height() - self.size().height()

            # Paint rescaled image
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.drawPixmap(self.dx / 2, self.dy / 2, self.scaledImage)

            # Paint in-progress box
            if self.drawingRect:
                x, y, x2, y2 = self.drawingRect
                # Convert % to xy coords, account for off by one error
                x  = (x * self.scaledImage.size().width() + self.dx / 2) - 1
                y  = (y * self.scaledImage.size().height() + self.dy / 2) - 1
                x2 = (x2 * self.scaledImage.size().width() + self.dx / 2) - 1
                y2 = (y2 * self.scaledImage.size().height() + self.dy / 2) - 2
                painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))

            # Paint existing boxes
            for rect in self.drawnRects:
                x, y, x2, y2 = rect
                # Convert % to xy coords, account for off by one error
                x  = (x * self.scaledImage.size().width() + self.dx / 2) - 1
                y  = (y * self.scaledImage.size().height() + self.dy / 2) - 1
                x2 = (x2 * self.scaledImage.size().width() + self.dx / 2) - 1
                y2 = (y2 * self.scaledImage.size().height() + self.dy / 2) - 2
                painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))

        if self.message:
            pen = QPen()
            font = QFont('Arial', 20)
            messageWidth = QFontMetrics(font).width(self.message)
            painter.setFont(font)
            pen.setColor(ThemeManager.ACCENT_QC)
            painter.setPen(pen)
            painter.drawText((self.width() - messageWidth) / 2, self.height() * .9, self.message)

        painter.end()

    def translateMousePosToPercent(self, event):
        '''Takes a given mouse event and translates the coordinates into image-relative percentages.'''
        try:
            # Translate mouse event location to percentage
            x = (event.x() - self.dx / 2) / self.scaledImage.size().width()
            y = (event.y() - self.dy / 2) / self.scaledImage.size().height()

            # Cap to max and min
            x = max(min(1.0, x), 0.0)
            y = max(min(1.0, y), 0.0)
            return (x, y)
        except:
            return (0.0,0.0)
    
    def checkBoxValid(self, points):
        '''Calculates total area % of image the box takes. Must be greater than MIN_BOX_SIZE.'''
        try:
            x, y, x2, y2 = points
            area = abs(x - x2) * abs(y2 - y)
            return area > self.MIN_BOX_SIZE
        except TypeError:
            return False

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() is Qt.LeftButton:
            self.xPress, self.yPress = self.translateMousePosToPercent(event)
            self.drawing = True
        
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.drawing:
            self.xMove, self.yMove = self.translateMousePosToPercent(event)
            self.drawingRect = (self.xPress, self.yPress, self.xMove, self.yMove)
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() is Qt.LeftButton:
            if self.drawing and self.checkBoxValid(self.drawingRect):
                self.drawnRects.append(self.drawingRect)
            self.drawingRect = None
            self.update()
            self.drawing = False
        elif event.button() is Qt.RightButton:
            self.createConfirmDialog()

    def createConfirmDialog(self):
        confirmDelete = ConfirmDelete(self)
        confirmDelete.confirmed.connect(self.requestDelete)
        
        

        confirmDelete.exec_()

        

    def requestDelete(self):
        self.deleteRequested.emit(self.imageData)

    boxCompleted = Signal(object)
    deleteRequested = Signal(object)