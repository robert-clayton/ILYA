from PySide2.QtCore     import  Qt, Signal, QPoint
from PySide2.QtWidgets  import  QVBoxLayout, QHBoxLayout, QDialog, \
                                QLabel, QPushButton
import ThemeManager

class ConfirmDelete(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        # Objects
        self.layout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()
        self.cancelButton = QPushButton('Cancel')
        self.confirmButton = QPushButton('Confirm')
        self.messageText = QLabel('Are you sure you wish to delete this image?')

        # Layouts
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.confirmButton)
        self.layout.addWidget(self.messageText)
        self.layout.addLayout(self.buttonLayout)

        # Styling
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.WA_DeleteOnClose)
        self.layout.setSpacing(30)
        self.setStyleSheet('ConfirmDelete {'
            'background-color: ' + ThemeManager.BG + ';'
            'border-top-left-radius:     15px;'
            'border-bottom-left-radius:  15px;'
            'border-top-right-radius:    15px;'
            'border-bottom-right-radius: 15px;'
            'border-width: 0px;'
            'border-style: solid;'
            '}')
        self.messageText.setStyleSheet('color: ' + ThemeManager.LABEL + ';')
        self.confirmButton.setStyleSheet('QPushButton {'
            'background-color: ' + ThemeManager.ACCENT + ';'
            'color: ' + ThemeManager.LABEL_DARK + ';'
            '}')
        self.cancelButton.setStyleSheet('QPushButton {'
            'background-color: ' + ThemeManager.BG_L1 + ';'
            'color: ' + ThemeManager.LABEL + ';'
            '}')

        # Connections
        self.cancelButton.clicked.connect(self.close)
        self.confirmButton.clicked.connect(self.accepted)
        self.confirmButton.clicked.connect(self.close)

    def showEvent(self, event):
        super().showEvent(event)
        self.move(self.pos() +
                QPoint(self.width() / 2, self.height() / 2)
            )