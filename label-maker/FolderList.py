import os
import ThemeManager
from PySide2.QtCore     import Qt, Signal, QSize
from PySide2.QtWidgets  import QListView, QStyledItemDelegate, QFrame, QAbstractItemView, QStyle
from PySide2.QtGui      import QStandardItemModel, QStandardItem, QFont, QColor, QBrush

class FolderList(QListView):
    def __init__(self):
        super().__init__()
        self.folderModel = QStandardItemModel()
        self.setModel(self.folderModel)
        self.setFrameStyle(QFrame.NoFrame)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setItemDelegate(Folder())

        self.setStyleSheet('FolderList { background-color: Transparent; color: rgb(190,190,190); }')
        self.setAttribute(Qt.WA_TranslucentBackground)

        for idx, folder in enumerate(self.getImageFolders()):
            item = QStandardItem(folder)
            item.setData(folder.replace('imgur', '').replace('reddit_sub', '').replace('_', ''), role=Qt.DisplayRole)
            item.setData(os.path.join(ThemeManager.IMAGE_FOLDERS_PATH, folder), role=Qt.UserRole)
            item.setData(folder, role=Qt.UserRole+1)

            self.folderModel.appendRow(item)

    def getImageFolders(self):
        contents = map(lambda f: f.name, os.scandir(ThemeManager.IMAGE_FOLDERS_PATH))
        yield from filter(lambda f: os.path.isdir(os.path.join(ThemeManager.IMAGE_FOLDERS_PATH, f)), contents)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            self.selectedFolderChanged.emit(index)

    selectedFolderChanged = Signal(object)

class Folder(QStyledItemDelegate):
    def __init__(self, height=20):
        super().__init__()
        self.height = height

    def sizeHint(self, option, index):
        return QSize(option.rect.width(), self.height)
    
    def paint(self, painter, option, index):
        painter.save()
        item = index.model().data(index, role=Qt.DisplayRole)
        font = QFont('Arial', 10)

        if option.state & QStyle.State_Selected:
            pen = painter.pen()
            pen.setColor(QColor(0,0,0,255))
            painter.setPen(pen)
            painter.setBrush(QBrush(ThemeManager.ACCENT_QC))
            painter.drawRect(option.rect.x(), option.rect.y(), option.rect.width() - 1, option.rect.height() - 1)
        
        painter.translate(option.rect.x(), option.rect.y())
        painter.setFont(font)

        painter.drawText(20,15,item)
        painter.restore()