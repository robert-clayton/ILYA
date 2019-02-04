from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *
from Box                import Box

class Canvas(QFrame):
    MIN_BOX_SIZE = 0.0025 # percent of image

    def __init__(self, label_name = 'Default', image_data = None):
        super().__init__()
        self.setMinimumSize(QSize(850, 725))
        self.image_data = image_data
        self.image = QPixmap(image_data.data(role=Qt.DisplayRole)) if image_data else None
        self.setStyleSheet('Canvas { background-color: rgba(50,50,50,255); }')

        self.label_name = label_name
        self.drawn_rects  = []
        self.drawing_rect = None
        self.drawing = False

    def change_image(self, new_image_index):
        self.image_data = new_image_index
        self.image = QPixmap(new_image_index.data(role=Qt.UserRole))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # If image is set
        if self.image:
            # Scale image down
            self.scaled_image = self.image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Find xy offsets
            self.dx = self.size().width()  - self.scaled_image.size().width()  if self.size().width()  - self.scaled_image.size().width()  else self.scaled_image.size().width()  - self.size().width()
            self.dy = self.size().height() - self.scaled_image.size().height() if self.size().height() - self.scaled_image.size().height() else self.scaled_image.size().height() - self.size().height()

            # Paint rescaled image
            
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.drawPixmap(self.dx / 2, self.dy / 2, self.scaled_image)

            # Paint in-progress box
            if self.drawing_rect:
                x, y, x2, y2 = self.drawing_rect
                # Convert % to xy coords, account for off by one error
                x  = (x * self.scaled_image.size().width() + self.dx / 2) - 1
                y  = (y * self.scaled_image.size().height() + self.dy / 2) - 1
                x2 = (x2 * self.scaled_image.size().width() + self.dx / 2) - 1
                y2 = (y2 * self.scaled_image.size().height() + self.dy / 2) - 2
                painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))

            # Paint existing boxes
            for rect in self.drawn_rects:
                x, y, x2, y2 = rect
                # Convert % to xy coords, account for off by one error
                x  = (x * self.scaled_image.size().width() + self.dx / 2) - 1
                y  = (y * self.scaled_image.size().height() + self.dy / 2) - 1
                x2 = (x2 * self.scaled_image.size().width() + self.dx / 2) - 1
                y2 = (y2 * self.scaled_image.size().height() + self.dy / 2) - 2
                painter.drawRect(QRect(QPoint(x, y), QPoint(x2, y2)))

        painter.end()

    def translate_mouse_event_to_percent(self, event):
        try:
            # Translate mouse event location to percentage
            x = (event.x() - self.dx / 2) / self.scaled_image.size().width()
            y = (event.y() - self.dy / 2) / self.scaled_image.size().height()

            # Cap to max and min
            x = max(min(1.0, x), 0.0)
            y = max(min(1.0, y), 0.0)
            return (x, y)
        except:
            return (0.0,0.0)
    
    def check_box_valid(self, points):
        x, y, x2, y2 = points
        area = abs(x - x2) * abs(y2 - y)
        return area > self.MIN_BOX_SIZE

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.x_press, self.y_press = self.translate_mouse_event_to_percent(event)
        self.drawing = True
        
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.drawing:
            self.x_move, self.y_move = self.translate_mouse_event_to_percent(event)
            self.drawing_rect = (self.x_press, self.y_press, self.x_move, self.y_move)
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.drawing and self.check_box_valid(self.drawing_rect):
            self.drawn_rects.append(self.drawing_rect)
        self.update()
        self.drawing = False            

    boxCompleted = Signal(object)