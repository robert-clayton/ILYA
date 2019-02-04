from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *
from FileManager        import FileManager as fm
import ThemeManager
import os

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        # Movement logic vars
        self.mouse_move_pos     = self.window().pos()
        self.mouse_press_pos    = self.window().pos()
        self.can_move           = False
        self.dragging_threshold = 5
        
        # Objects
        self.drop_shadow    = QGraphicsDropShadowEffect(self)
        self.icon           = QLabel()
        self.icon_reader    = QImageReader()
        self.minimize       = Button('Minimize')
        self.close          = Button('Close')
        self.layout         = QHBoxLayout(self)

        # Layout
        self.layout.addWidget(self.icon)
        self.layout.addStretch(1)
        self.layout.addWidget(self.minimize)
        self.layout.addWidget(self.close)

        # Styling
        self.setStyleSheet('TopBar { '
                            'background: ' + ThemeManager.TOP_BAR + ';'
                            'border-top-left-radius:     15px;'
                            'border-top-right-radius:    15px;'
                            'border-width: 0px;'
                            'border-style: solid; }')
        self.setMinimumHeight(50)
        self.icon_reader.setScaledSize(QSize(20,20))
        self.icon_reader.setFileName(os.path.join(fm.current_dir, 'logo.ico'))
        self.icon.setPixmap(QPixmap.fromImage(self.icon_reader.read()))
        self.drop_shadow.setOffset(QPointF(0,5))
        self.drop_shadow.setColor(QColor(30,30,30,100))
        self.drop_shadow.setBlurRadius(10)
        self.setGraphicsEffect(self.drop_shadow)
        self.layout.setContentsMargins(20,0,20,0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignVCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_press_pos = self.window().pos()
            self.mouse_move_pos = event.globalPos()
            self.can_move       = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        move_dist = (event.globalPos() - self.mouse_move_pos).manhattanLength()
        if self.can_move and move_dist > self.dragging_threshold:            
            self.window().move(self.mouse_press_pos + event.globalPos() - self.mouse_move_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.can_move = False
        super().mouseReleaseEvent(event)

class Button(QFrame):
    def __init__(self, button_type):
        super().__init__()
        # Variables
        self.button_type = button_type

        # Objects
        self.layout = QHBoxLayout(self)
        self.label = QLabel(button_type)
        
        # Layout
        self.layout.addWidget(self.label)

        # Styling
        self.layout.setMargin(0)
        self.label.setFont(QFont('Arial', 9, QFont.Bold))
        self.label.setStyleSheet('color: ' + ThemeManager.LABEL + ';')

    def enterEvent(self, event):
        self.label.setStyleSheet('color: ' + ThemeManager.ACCENT + ';')
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.label.setStyleSheet('color: ' + ThemeManager.LABEL + ';')
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.button_type == 'Minimize':
            self.window().showMinimized()
        elif self.button_type == 'Close':
            self.window().close()