import os
from PySide2.QtCore import QTimer, Signal, QSize, QRect, \
                        QPoint, Qt, QPersistentModelIndex
from PySide2.QtGui import QPainter, QPen, QFont, QFontMetrics, \
                        QPixmap, QColor, QBrush, QPainterPath
from PySide2.QtWidgets import QFrame
from . import ThemeManager, LabelConfigurator

class Canvas(QFrame):
    '''Takes care of showing the currently focused image and the main app use case of creating labels'''
    MIN_BOX_SIZE = 0.0025 # percent of image

    def __init__(self, boxManager):
        super().__init__()
        # Variables
        self.message     = ''
        self.imageData   = None
        self.boxes       = []
        self.drawingRect = None
        self.drawing     = False

        # Objects
        self.image              = None
        self.messageResetTimer  = QTimer()
        self.brush              = QBrush()
        self.pen                = QPen()
        self.font               = QFont('Arial', 8)
        self.boxManager         = boxManager

        # Styling
        self.setMinimumSize(QSize(850, 725))
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
        if newImageIndex:
            self.imageData = QPersistentModelIndex(newImageIndex)
            image = QPixmap(newImageIndex.data(role=Qt.UserRole))
            self.scaledImage = image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Get matching boxes already in data frame
            self.boxes = self.boxManager.getBoxesForImage(newImageIndex.data(role=Qt.DisplayRole))
        else:
            self.imageData = None
            self.scaledImage = None
            self.boxes = []

        # Update to redraw
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # TODO: Use QPainterPath's arcTo function to do this in a single draw
        # Draw background
        painter.save()
        self.brush.setColor(ThemeManager.BG_L2_QC)
        self.brush.setStyle(Qt.SolidPattern)
        painter.setBrush(self.brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.size().width() / 2, self.size().height()) # Left Side
        painter.drawRect(0, 0, self.size().width(), self.size().height() / 2) # Top Side
        painter.drawRoundedRect(self.rect(), ThemeManager.CURVE, ThemeManager.CURVE)
        painter.restore()

        # If image is set
        if self.imageData:
            if self.imageData.isValid():
                # Find xy offsets
                self.dx = self.size().width()  - self.scaledImage.size().width()  if self.size().width()  - self.scaledImage.size().width()  else self.scaledImage.size().width()  - self.size().width()
                self.dy = self.size().height() - self.scaledImage.size().height() if self.size().height() - self.scaledImage.size().height() else self.scaledImage.size().height() - self.size().height()

                # Paint rescaled image
                painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
                painter.drawPixmap(self.dx / 2, self.dy / 2, self.scaledImage)

                # Paint in-progress box
                if self.drawingRect:
                    painter.save()
                    x, x2, y, y2 = self.drawingRect
                    # Convert % to xy coords, account for off by one error
                    x  = (x * self.scaledImage.size().width() + self.dx / 2) - 1
                    y  = (y * self.scaledImage.size().height() + self.dy / 2) - 1
                    x2 = (x2 * self.scaledImage.size().width() + self.dx / 2) - 2
                    y2 = (y2 * self.scaledImage.size().height() + self.dy / 2) - 2

                    # Setup painter's brush and pen colors
                    self.brush.setColor(ThemeManager.ACCENT_LOW_OPACITY_QC)
                    self.brush.setStyle(Qt.SolidPattern)
                    self.pen.setColor(ThemeManager.ACCENT_QC)
                    painter.setBrush(self.brush)
                    painter.setPen(self.pen)
                    painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))
                    painter.restore()

                # Paint existing boxes
                for box in self.boxes:
                    painter.save()

                    # Draw box's rect
                    x, x2, y, y2 = box.getRect()
                    x  = (x * self.scaledImage.size().width() + self.dx / 2) - 1
                    y  = (y * self.scaledImage.size().height() + self.dy / 2) - 1
                    x2 = (x2 * self.scaledImage.size().width() + self.dx / 2) - 1
                    y2 = (y2 * self.scaledImage.size().height() + self.dy / 2) - 2
                    self.brush.setColor(ThemeManager.ACCENT_VLOW_OPACITY_QC)
                    self.brush.setStyle(Qt.SolidPattern)
                    self.pen.setColor(ThemeManager.ACCENT_QC)
                    painter.setBrush(self.brush)
                    painter.setPen(self.pen)
                    painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))

                    # Draw label BG
                    painter.setPen(Qt.NoPen)
                    self.brush.setColor(ThemeManager.ACCENT_QC)
                    painter.setBrush(self.brush)
                    labelWidth = QFontMetrics(self.font).width(box.getLabel())
                    labelHeight = QFontMetrics(self.font).height()
                    painter.drawRect(x, y, labelWidth + 4, labelHeight)

                    # Draw label
                    self.pen.setColor(ThemeManager.BLACK_QC)
                    painter.setPen(self.pen)
                    painter.drawText(x + 2, y + 11, box.getLabel())
                    painter.restore()

        if self.message:
            painter.save()
            font = QFont('Arial', 20)
            messageWidth = QFontMetrics(font).width(self.message)
            painter.setFont(font)
            self.pen.setColor(ThemeManager.ACCENT_QC)
            painter.setPen(self.pen)
            painter.drawText((self.width() - messageWidth) / 2, self.height() * .9, self.message)
            painter.restore()

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
        if event.button() == Qt.LeftButton:
            self.handleDrawnBox(event.globalPos())

    def handleDrawnBox(self, spawnPos):
        '''Called by mouse release event. Lets the Box Manager know to add box to data frame.'''
        if self.drawing and self.checkBoxValid(self.drawingRect):
            newConfig = LabelConfigurator.LabelConfigurator(self.boxManager, spawnPos)
            newConfig.labelAccepted.connect(self.addNewBox)
            newConfig.exec_()
        self.drawingRect = None
        self.update()
        self.drawing = False

    def addNewBox(self, labelConfig):
        x, x2, y, y2 = self.drawingRect
        labelName, isOccluded, isTruncated, isGroupOf, isDepiction, isInside = labelConfig
        xMin = min([x, x2])
        xMax = max([x, x2])
        yMin = min([y, y2])
        yMax = max([y, y2])
        newBox = self.boxManager.addBoxToDataFrame(self.imageData.data(role=Qt.DisplayRole), labelName, xMin, xMax, yMin, yMax, isOccluded, isTruncated, isGroupOf, isDepiction, isInside)
        self.boxes.append(newBox)