from PySide2.QtWidgets  import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from ScrollBar          import ScrollBar
from FileManager        import FileManager as fm
import os, copy

class ImageList(QListView):
    def __init__(self, model = None):
        super().__init__()
        if model: self.setModel(model)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollBar(ScrollBar(self))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setItemDelegate(Image(self.width()))
        self.setLayoutMode(QListView.Batched)
        self.setBatchSize(10)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setItemDelegate(Image(self.width()))
    
    def populate(self, folder):
        self.populate_thread = Populate(folder)
        self.populate_thread.modelFinished.connect(self.setModel)
        self.populate_thread.start()

class Image(QStyledItemDelegate):
    def __init__(self, width):
        super().__init__()
        self.width = width

    def sizeHint(self, option, index):
        item = index.model().data(index, role=Qt.UserRole)
        image = QPixmap(item).scaledToWidth(self.width)
        return image.size()

    def paint(self, painter, option, index):
        painter.save()
        item = index.model().data(index, role=Qt.UserRole)
        image = QPixmap(item).scaledToWidth(self.width, Qt.SmoothTransformation)
        painter.translate(option.rect.x(), option.rect.y())
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.drawPixmap(0, 0, image)
        painter.restore()

class Populate(QThread):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    def run(self):
        model = QStandardItemModel()

        for image in fm().get_image_folder_contents(self.folder.data(role=Qt.UserRole)):
            url = os.path.join(fm().images_folder, self.folder.data(role=Qt.UserRole), image)
            item = QStandardItem(image)
            item.setData(url, role=Qt.UserRole)
            model.appendRow(item)
        
        self.modelFinished.emit(model)

    modelFinished = Signal(object)