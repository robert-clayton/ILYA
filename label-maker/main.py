import os, sys, json
from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *
from FolderList         import FolderList
from FlowLayout         import FlowLayout
from FileManager        import FileManager as fm
from ImageList          import ImageList
from Box                import Box



class ImageViewer(QFrame):
    MIN_BOX_SIZE = 0.0025 # percent of image

    def __init__(self, label_name = 'Default', image = None):
        super().__init__()
        self.setMinimumSize(QSize(850, 725))
        self.image = QPixmap(image) if image else None
        self.setStyleSheet('ImageViewer { background: rgb(50,50,50); }')

        self.label_name = label_name
        self.drawn_rects  = []
        self.drawing_rect = None
        self.drawing = False

    def paintEvent(self, event):
        # If image is set
        if self.image:
            # Scale image down
            self.scaled_image = self.image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Find xy offsets
            self.dx = self.size().width()  - self.scaled_image.size().width()  if self.size().width()  - self.scaled_image.size().width()  else self.scaled_image.size().width()  - self.size().width()
            self.dy = self.size().height() - self.scaled_image.size().height() if self.size().height() - self.scaled_image.size().height() else self.scaled_image.size().height() - self.size().height()

            # Paint rescaled image
            painter = QPainter(self)
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
        # Translate mouse event location to percentage
        x = (event.x() - self.dx / 2) / self.scaled_image.size().width()
        y = (event.y() - self.dy / 2) / self.scaled_image.size().height()

        # Cap to max and min
        x = max(min(1.0, x), 0.0)
        y = max(min(1.0, y), 0.0)
        return (x, y)
    
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
        if self.check_box_valid(self.drawing_rect):
            self.drawn_rects.append(self.drawing_rect)
        self.update()
        self.drawing = False            

    boxCompleted = Signal(object)

class Central(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('Central { background: rgb(30,30,30); }')
        self.layout                 = QHBoxLayout(self)
        self.focused_image  = ImageViewer(image='C:\\Users\\draug\\Desktop\\floof.png')
        self.image_list     = ImageList()
        self.folder_list    = FolderList(fm().get_images_folders())
        self.folder_list.setMaximumWidth(300)
        
        self.layout.addWidget(self.image_list, 20)
        self.layout.addWidget(self.focused_image, 60)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.folder_list, 20)
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