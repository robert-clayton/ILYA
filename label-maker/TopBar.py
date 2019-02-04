from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('TopBar { '
                            'background: rgb(70,70,70); '
                            'border-top-left-radius:     15px;'
                            'border-top-right-radius:    15px;'
                            'border-width: 0px;'
                            'border-style: solid; }')
        self.setMinimumHeight(50)
        
        drop_shadow = QGraphicsDropShadowEffect(self)
        drop_shadow.setOffset(QPointF(0,5))
        drop_shadow.setColor(QColor(30,30,30,100))
        drop_shadow.setBlurRadius(10)
        self.setGraphicsEffect(drop_shadow)

        # Movement logic vars
        self.mouse_move_pos     = self.window().pos()
        self.mouse_press_pos    = self.window().pos()
        self.can_move           = False
        self.dragging_threshold = 5

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.mouse_press_pos = self.window().pos()
            self.mouse_move_pos = event.globalPos()
            self.can_move       = True

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        move_dist = (event.globalPos() - self.mouse_move_pos).manhattanLength()
        if self.can_move and move_dist > self.dragging_threshold:
            self.window().move(self.mouse_press_pos + event.globalPos() - self.mouse_move_pos)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.can_move = False


# class Button(QFrame):
#     def __init__(self):
#         super().__init__()

#     def 
#         self.setWindowState(QtCore.Qt.WindowMaximized)