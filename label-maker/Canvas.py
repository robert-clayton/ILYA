import os
from PySide2.QtCore     import QTimer, Signal, QSize, QRect, QPoint, Qt, QPersistentModelIndex
from PySide2.QtGui      import QPainter, QPen, QFont, QFontMetrics, QPixmap, QColor
from PySide2.QtWidgets  import QFrame
from BoxManager         import BoxManager
from DeletePopup        import ConfirmDelete
import ThemeManager

class Canvas(QFrame):
    '''Takes care of showing the currently focused image and the main app use case of creating labels'''
    MIN_BOX_SIZE = 0.0025 # percent of image

    def __init__(self, boxManager):
        super().__init__()
        # Variables
        self.message = ''
        self.messageResetTimer = QTimer()
        self.imageData = None
        self.boxes  = []
        self.drawingRect = None
        self.drawing = False

        # Objects
        self.image = None
        self.boxManager = boxManager

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
        # Set new image index
        self.imageData = QPersistentModelIndex(newImageIndex)
        self.image = QPixmap(newImageIndex.data(role=Qt.UserRole))

        # Get matching boxes already in data frame
        self.boxes = self.boxManager.getBoxesForImage(newImageIndex.data(role=Qt.DisplayRole))

        # Update to redraw
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # If image is set
        if self.imageData:
            if self.imageData.isValid():
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
                    x, x2, y, y2 = self.drawingRect
                    # Convert % to xy coords, account for off by one error
                    x  = (x * self.scaledImage.size().width() + self.dx / 2) - 1
                    y  = (y * self.scaledImage.size().height() + self.dy / 2) - 1
                    x2 = (x2 * self.scaledImage.size().width() + self.dx / 2) - 2
                    y2 = (y2 * self.scaledImage.size().height() + self.dy / 2) - 2
                    painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))

                # Paint existing boxes
                for box in self.boxes:
                    x, x2, y, y2 = box.getRect()
                    # Convert % to xy coords, account for off by one error, and draw box's rect
                    x  = (x * self.scaledImage.size().width() + self.dx / 2) - 1
                    y  = (y * self.scaledImage.size().height() + self.dy / 2) - 1
                    x2 = (x2 * self.scaledImage.size().width() + self.dx / 2) - 1
                    y2 = (y2 * self.scaledImage.size().height() + self.dy / 2) - 2
                    painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))

                    # Draw box's label
                    pen = QPen()
                    font = QFont('Arial', 8)
                    pen.setColor(QColor(10,10,10))
                    painter.setPen(pen)
                    painter.drawText(x + 2, y + 11, box.getLabel())

            # Image this index was referencing was deleted
            else: 
                self.boxes = []
                self.imageData = None

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
            x, x2, y, y2 = points
            area = abs(x2 - x) * abs(y2 - y)
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
            self.drawingRect = (self.xPress, self.xMove, self.yPress, self.yMove)
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() is Qt.LeftButton:
            self.handleDrawnBox()
        elif event.button() is Qt.RightButton and self.image:
            confirmDelete = ConfirmDelete(self)
            confirmDelete.accepted.connect(self.deleteImage)
            confirmDelete.exec_()

    def handleDrawnBox(self):
        '''Called by mouse release event. Lets the Box Manager know to add box to data frame.'''
        if self.drawing and self.checkBoxValid(self.drawingRect):
            x, x2, y, y2 = self.drawingRect
            newBox = self.boxManager.addBoxToDataFrame(self.imageData.data(role=Qt.DisplayRole), min([x, x2]), max([x, x2]), min([y, y2]), max([y, y2]))
            self.boxes.append(newBox)
        self.drawingRect = None
        self.update()
        self.drawing = False

    #FIXME: PermissionError: [WinError 32] The process cannot access the file because it is being used by another process
    def deleteImage(self):
        path = self.imageData.data(role=Qt.UserRole)
        self.imageData.model().removeRow(self.imageData.row())
        self.update()
        os.remove(path)