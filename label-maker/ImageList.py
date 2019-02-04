from PySide2.QtWidgets  import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from ScrollBar          import ScrollBar
from FileManager        import FileManager as fm
import os, copy
from PIL                import Image
import time

class ImageList(QListView):
    def __init__(self, model = None):
        super().__init__()
        if model: self.setModel(model)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFrameStyle(QFrame.NoFrame)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollBar(ScrollBar(self))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLayoutMode(QListView.Batched)
        self.setBatchSize(10)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if event.oldSize().width() != event.size().width():
            self.setItemDelegate(Thumbnail(self.width()))
    
    def populate(self, folder):
        self.populate_thread = Populate(folder)
        self.populate_thread.modelFinished.connect(self.setModel)
        self.populate_thread.start()

class Thumbnail(QStyledItemDelegate):
    def __init__(self, width):
        super().__init__()
        self.width  = width
        self.height = None
        self.reader = QImageReader()
    
    def set_width(self, param):
        self.width = param

    def sizeHint(self, option, index):
        item = index.model().data(index, role=Qt.UserRole)
        with Image.open(item) as img:
            width, height = img.size
        dx = self.width / width
        self.height = height * dx
        size = QSize(self.width, self.height)
        self.reader.setScaledSize(size)
        return size

    def paint(self, painter, option, index):
        painter.save()
        item = index.model().data(index, role=Qt.UserRole)

        # Suppress libpng profile warnings
        try:
            self.reader.setFileName(item)
            image = QPixmap.fromImageReader(self.reader)
        except:
            pass
        painter.translate(option.rect.x(), option.rect.y())
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

        if option.state & (QStyle.State_Selected | QStyle.State_MouseOver):
            painter.setOpacity(1)
        else: #not option.state & QStyle.State_MouseOver:
            painter.setOpacity(0.90)

        painter.drawPixmap(0, 0, image)

        painter.restore()

class Populate(QThread):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    def run(self):
        model = QStandardItemModel()

        for image in fm().get_image_folder_contents(self.folder.data(role=Qt.UserRole)):
            url = os.path.join(fm.images_folder, self.folder.data(role=Qt.UserRole), image)
            item = QStandardItem(image)
            item.setData(url, role=Qt.UserRole)
            model.appendRow(item)
        
        self.modelFinished.emit(model)

    modelFinished = Signal(object)