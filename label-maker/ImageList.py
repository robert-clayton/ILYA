from PySide2.QtWidgets  import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from FileManager        import FileManager as fm
import os, copy
from PIL                import Image

class ImageList(QListView):
    def __init__(self, model = None):
        super().__init__()
        if model: self.setModel(model)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet('background-color: Transparent;')
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLayoutMode(QListView.Batched)
        self.setBatchSize(10)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if event.oldSize().width() != event.size().width():
            self.setItemDelegate(Thumbnail(self.width()))
    
    def populate(self, folder):
        self.populateThread = Populate(folder)
        self.populateThread.modelFinished.connect(self.setModel)
        self.populateThread.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            self.selectedImageChanged.emit(index)
    
    selectedImageChanged = Signal(object)

class Thumbnail(QStyledItemDelegate):
    def __init__(self, width):
        super().__init__()
        self.thumbnailWidth = width
        self.height = None
        self.reader = QImageReader()
    
    def setThumbnailWidth(self, param):
        self.thumbnailWidth = param

    def sizeHint(self, option, index):
        item = index.model().data(index, role=Qt.UserRole)
        with Image.open(item) as img:
            width, height = img.size
        dx = self.thumbnailWidth / width
        self.height = height * dx
        size = QSize(self.thumbnailWidth, self.height)
        self.reader.setScaledSize(size)
        return size

    def paint(self, painter, option, index):
        painter.save()
        item = index.model().data(index, role=Qt.UserRole)

        # Suppress some of the libpng profile warnings
        try:
            self.reader.setFileName(item)
            image = QPixmap.fromImageReader(self.reader)
        except:
            pass
        painter.translate(option.rect.x(), option.rect.y())
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

        if option.state & (QStyle.State_Selected | QStyle.State_MouseOver):
            painter.setOpacity(1)
        else:
            painter.setOpacity(0.90)

        painter.drawPixmap(0, 0, image)
        painter.restore()

class Populate(QThread):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    def run(self):
        model = QStandardItemModel()

        for image in fm().getImageFolderContents(self.folder.data(role=Qt.UserRole)):
            url = os.path.join(fm.imagesFolder, self.folder.data(role=Qt.UserRole), image)
            item = QStandardItem(image)
            item.setData(url, role=Qt.UserRole)
            model.appendRow(item)
        
        self.modelFinished.emit(model)

    modelFinished = Signal(object)