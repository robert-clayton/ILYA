import os
from PySide2.QtCore     import Qt, Signal, QSize
from PySide2.QtWidgets  import QListView, QFrame, QAbstractItemView
from PySide2.QtGui      import QStandardItemModel, QStandardItem, QPainter, QBrush
from . import ThemeManager, ListDelegate

class FolderList(QListView):
    def __init__(self):
        super().__init__()
        # Objects
        self.brush          = QBrush()
        self.folderModel    = QStandardItemModel()

        # Styling
        self.setModel(self.folderModel)
        self.setFrameStyle(QFrame.NoFrame)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setItemDelegate(ListDelegate.ListDelegate())
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.brush.setColor(ThemeManager.BG_QC)
        self.brush.setStyle(Qt.SolidPattern)

        self.populate()

    def populate(self):
        for idx, folder in enumerate(self.getImageFolders()):
            item = QStandardItem(folder)
            item.setData(folder.replace('imgur', '').replace('reddit_sub', '').replace('_', ''), role=Qt.DisplayRole)
            item.setData(folder, role=Qt.DisplayRole)
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

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setBrush(self.brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(event.rect())
        super().paintEvent(event)

    selectedFolderChanged = Signal(object)