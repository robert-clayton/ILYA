from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *
from FileManager        import FileManager as fm
import os

class FolderList(QListView):
    def __init__(self, folderIterator):
        super().__init__()
        self.folderModel = QStandardItemModel()
        self.setModel(self.folderModel)
        self.setFrameStyle(QFrame.NoFrame)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet('FolderList { background-color: Transparent; color: rgb(190,190,190); }')
        self.setAttribute(Qt.WA_TranslucentBackground)

        for idx, folder in enumerate(folderIterator):
            item = QStandardItem(folder)
            item.setData(folder.replace('imgur', '').replace('reddit_sub', '').replace('_', ''), role=Qt.DisplayRole)
            item.setData(os.path.join(fm.currentDir, fm.imagesFolder, folder), role=Qt.UserRole)

            self.folderModel.appendRow(item)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if event.oldSize().width() != event.size().width():
            self.setItemDelegate(Folder(self.width()))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            self.selectedFolderChanged.emit(index)

    selectedFolderChanged = Signal(object)

class Folder(QStyledItemDelegate):
    def __init__(self, width, height=20):
        super().__init__()
        self.width = width
        self.height = height

    def set_width(self, param):
        self.width = param
    
    def sizeHint(self, option, index):
        return QSize(self.width, self.height)
    
    def paint(self, painter, option, index):
        painter.save()
        item = index.model().data(index, role=Qt.DisplayRole)
        painter.translate(option.rect.x(), option.rect.y())
        painter.setFont(QFont('Arial', 10))
        painter.drawText(20,10,item)
        painter.restore()