import ThemeManager
from PySide2.QtCore     import  Qt, QSize
from PySide2.QtGui      import  QColor, QFont, QFontMetrics, QPen, QBrush
from PySide2.QtWidgets  import  QStyledItemDelegate, QStyle

class ListDelegate(QStyledItemDelegate):
    def __init__(self, height=20):
        super().__init__()
        self.height = height
        self.font   = QFont('Arial', 10)
        fontHeight  = QFontMetrics(self.font).height()
        self.y      = self.height / 2 + fontHeight / 4 + fontHeight / 8 - 1

    def sizeHint(self, option, index):
        return QSize(option.rect.width(), self.height)
    
    def paint(self, painter, option, index):
        painter.save()
        item = index.model().data(index, role=Qt.DisplayRole)
        pen = painter.pen()

        if option.state & QStyle.State_Selected:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(ThemeManager.ACCENT_QC))
            painter.drawRect(option.rect.x(), option.rect.y(), option.rect.width() - 1, option.rect.height() - 1)
            pen.setColor(QColor(0,0,0,255))
            painter.setPen(pen)
        elif option.state & QStyle.State_MouseOver:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(ThemeManager.ACCENT_MED_OPACITY_QC))
            painter.drawRect(option.rect.x(), option.rect.y(), option.rect.width() - 1, option.rect.height() - 1)
            pen.setColor(QColor(0,0,0,255))
            painter.setPen(pen)
            
        else:
            pen.setColor(ThemeManager.LABEL_QC)
            painter.setPen(pen)

        painter.translate(option.rect.x(), option.rect.y())
        painter.setFont(self.font)
        painter.drawText(20,self.y,item)
        painter.restore()