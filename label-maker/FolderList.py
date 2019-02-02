from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *

class FolderList(QListView):
    def __init__(self, folder_iterator):
        super().__init__()
        self.setMinimumWidth(300)
        self.folder_model = QStandardItemModel()
        self.setModel(self.folder_model)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollBar(ScrollBar(self))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet('FolderList { background: rgb(30,30,30); color: rgb(190,190,190); }')

        for idx, folder in enumerate(folder_iterator):
            item = QStandardItem(folder)
            item.setData(folder.replace('imgur', '').replace('reddit_sub', '').replace('_', ''), role=Qt.DisplayRole)
            item.setData(folder, role=Qt.UserRole)

            self.folder_model.appendRow(item)

        self.selectionModel().currentChanged.connect(self.changed)

    def changed(self, from_index, to_index):
        self.selectedChanged.emit(to_index)

    selectedChanged = Signal(object)

class ScrollBar(QScrollBar):
    def __init__(self, parent_ref = None):
        super().__init__(parent_ref)
        if parent_ref: parent_ref.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        self.setStyleSheet(
            'ScrollBar:vertical {'
                'border: 0px;'
                'border-radius: 3px;'
                'background: transparent;'
                'width: 10px;'
            '}'

            'ScrollBar::sub-page:vertical, ScrollBar::add-page:vertical {'
                'background: none;'
                'border-radius: 3px;'
            '}'

            'ScrollBar::handle:vertical {'
                'background: rgb(237,182,234);'
                'min-height: 20px;'
                'border-radius: 3px;'
            '}'

            'ScrollBar:up-arrow:vertical, ScrollBar::down-arrow:vertical {'
                'color: none;'
                'border: none;'
                'background: none;'
            '}'

            'ScrollBar::add-line:vertical,  ScrollBar::sub-line:vertical {'
                'border: none;'
                'background: none;'
            '}'
        )
    
    def wheelEvent(self, event):
        dy = event.angleDelta().y() / 2
        try:
            dy += self.scroll_animation.currentValue() - self.scroll_animation.endValue()
        except:
            pass

        self.lerp_curve = QEasingCurve(QEasingCurve.InOutQuad)
        self.scroll_animation = QPropertyAnimation(self, b'value')
        
        self.scroll_animation.setDuration(100)
        self.scroll_animation.setEasingCurve(self.lerp_curve)
        self.scroll_animation.setStartValue(self.value())
        self.scroll_animation.setEndValue(self.value() - dy)
        self.scroll_animation.start()