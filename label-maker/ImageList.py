import os
import ThemeManager
from PIL                import Image
from PySide2.QtWidgets  import QListView, QStyledItemDelegate, QStyle, QFrame, QAbstractItemView
from PySide2.QtCore     import QSize, Signal, QThread, Qt
from PySide2.QtGui      import QImageReader, QStandardItemModel, QStandardItem, QPixmap

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
        self.setItemDelegate(Thumbnail())
        self.setLayoutMode(QListView.Batched)
        self.setBatchSize(10)
    
    def populate(self, folder):
        self.populateThread = Populate(folder)
        self.populateThread.modelFinished.connect(self.setModel)
        self.populateThread.start()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            self.selectedImageChanged.emit(index)
    
    selectedImageChanged = Signal(object)

# TODO: Do not draw bottom-left corner to keep with the window's style
class Thumbnail(QStyledItemDelegate):
    '''Styled Item Delegate paints images directly to the List View at the desired resolution'''
    def __init__(self):
        super().__init__()
        self.reader = QImageReader()

    def sizeHint(self, option, index):
        item = index.model().data(index, role=Qt.UserRole)
        with Image.open(item) as img:
            width, height = img.size
        dx = option.rect.width() / width
        height *= dx
        size = QSize(option.rect.width(), height)
        self.reader.setScaledSize(size)
        return size

    def paint(self, painter, option, index):
        painter.save()
        item = index.model().data(index, role=Qt.UserRole)

        self.reader.setFileName(item)
        image = QPixmap.fromImageReader(self.reader)
        painter.translate(option.rect.x(), option.rect.y())

        if option.state & (QStyle.State_Selected | QStyle.State_MouseOver):
            painter.setOpacity(1)
        else:
            painter.setOpacity(0.90)

        painter.drawPixmap(0, 0, image)
        painter.restore()

class Populate(QThread):
    '''Worker to populate a Standard Item Model off of the GUI thread'''

    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    def getImageFolderContents(self, folder):
        validExts = ('.jpg', '.jpeg', '.png')
        path = os.path.join(ThemeManager.IMAGE_FOLDERS_PATH, folder)
        contents = map(lambda f: f.name, os.scandir(path))
        yield from filter(lambda f: any(f.endswith(ext) for ext in validExts), contents)

    def run(self):
        model = QStandardItemModel()

        for image in self.getImageFolderContents(self.folder.data(role=Qt.UserRole)):
            url = os.path.join(ThemeManager.IMAGE_FOLDERS_PATH, self.folder.data(role=Qt.UserRole), image)
            item = QStandardItem(image)
            item.setData(url, role=Qt.UserRole)
            model.appendRow(item)
        
        self.modelFinished.emit(model)

    modelFinished = Signal(object)