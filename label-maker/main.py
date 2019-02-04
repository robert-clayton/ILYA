import os, sys, json
import ThemeManager
from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *
from TopBar             import TopBar
from FolderList         import FolderList
from ImageList          import ImageList
from ScrollBar          import ScrollBar
from Canvas             import Canvas
from FileManager        import FileManager as fm

class Central(QFrame):
    def __init__(self):
        super().__init__()
        # Initiate objects
        self.overall_layout = QVBoxLayout(self)
        self.top_bar        = TopBar()
        self.content_layout = QHBoxLayout()
        self.selector_area  = QFrame()
        self.selector_layout= QVBoxLayout(self.selector_area)
        self.folder_area    = QFrame()
        self.folder_layout  = QHBoxLayout(self.folder_area)
        self.folder_list    = FolderList(fm().get_images_folders())
        self.folder_bar     = ScrollBar(self.folder_list)
        self.canvas         = Canvas()
        self.image_area     = QFrame()
        self.image_list     = ImageList()
        self.image_layout   = QHBoxLayout(self.image_area)
        self.image_bar      = ScrollBar(self.image_list)

        # Styling
        self.setStyleSheet('Central { '
                            'background-color: ' + ThemeManager.BG + ';'
                            'border-top-left-radius:     15px;'
                            'border-bottom-left-radius:  15px;'
                            'border-top-right-radius:    15px;'
                            'border-bottom-right-radius: 15px;'
                            'border-width: 0px;'
                            'border-style: solid; }')
        self.overall_layout.setMargin(0)
        self.overall_layout.setSpacing(0)
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.content_layout.setMargin(0)        
        self.content_layout.setSpacing(0)
        self.selector_layout.setMargin(0)
        self.selector_layout.setSpacing(0)
        self.folder_layout.setMargin(0)
        self.folder_layout.setSpacing(0)
        self.image_layout.setMargin(0)
        self.image_layout.setSpacing(0)
        self.folder_list.setVerticalScrollBar(self.folder_bar)
        self.image_list.setVerticalScrollBar(self.image_bar)
        self.selector_area.setMaximumWidth(400)
        self.selector_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout
        self.folder_layout.addWidget(self.folder_list)
        self.folder_layout.addSpacerItem(QSpacerItem(-7, 0))
        self.folder_layout.addWidget(self.folder_bar)
        self.image_layout.addWidget(self.image_list)
        self.image_layout.addSpacerItem(QSpacerItem(-7, 0))
        self.image_layout.addWidget(self.image_bar)
        self.selector_layout.addWidget(self.folder_area, 15)
        self.selector_layout.addWidget(self.image_area, 85)
        self.content_layout.addWidget(self.selector_area, 30)
        self.content_layout.addWidget(self.canvas, 70)
        self.overall_layout.addLayout(self.content_layout)
        self.overall_layout.insertWidget(0, self.top_bar)

        # Connections
        self.folder_list.selectedFolderChanged.connect(self.populate_image_list)
        self.image_list.selectedImageChanged.connect(self.change_canvas_image)

    def populate_image_list(self, folder):
        self.image_list.populate(folder)
        self.canvas.set_message('Switching Folders - {}'.format(folder.data(role=Qt.DisplayRole)))

    def change_canvas_image(self, image):
        self.canvas.change_image(image)
        self.canvas.set_message('Switching Images - {}'.format(image.data(role=Qt.DisplayRole)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central = Central()
        self.setCentralWidget(central)
        self.setWindowTitle('Label Maker')
        self.setWindowIcon(QIcon(os.path.join(fm.current_dir, 'logo.ico')))

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()
    