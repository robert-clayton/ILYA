from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *
from ScrollBar          import ScrollBar
from FileManager        import FileManager as fm
import os

class FolderList(QListView):
    def __init__(self, folder_iterator):
        super().__init__()
        self.folder_model = QStandardItemModel()
        self.setModel(self.folder_model)
        self.setFrameStyle(QFrame.NoFrame)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollBar(ScrollBar(self))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet('FolderList { background: rgb(30,30,30); color: rgb(190,190,190); }')

        for idx, folder in enumerate(folder_iterator):
            item = QStandardItem(folder)
            item.setData(folder.replace('imgur', '').replace('reddit_sub', '').replace('_', ''), role=Qt.DisplayRole)
            item.setData(os.path.join(fm.current_dir, fm.images_folder, folder), role=Qt.UserRole)

            self.folder_model.appendRow(item)

        self.selectionModel().currentRowChanged.connect(self.changed)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if event.oldSize().width() != event.size().width():
            self.setItemDelegate(Folder(self.width()))

    def changed(self, selected, deselected):
        self.currentRowChanged.emit(selected)

    currentRowChanged = Signal(object)

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
        painter.setFont(QFont('Airal', 10))
        painter.drawText(0,0,item)


        painter.restore()