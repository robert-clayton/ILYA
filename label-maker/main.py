from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtGui      import *
from PySide2.QtWidgets  import *

import os, sys, json
from PIL import Image
from FolderList import FolderList
from FlowLayout import FlowLayout

file_manager = None

class FileManager(QObject):
    def __init__(self):
        super().__init__()
        self.current_dir    = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.save_location  = os.path.dirname(os.path.realpath(__file__))
        self.images_folder  = os.path.join(self.current_dir, 'Images')
        self.labels_folder  = os.path.join(self.current_dir, 'Labels')

    def get_images_folders(self):
        contents = map(lambda f: f.name, os.scandir(self.images_folder))
        yield from filter(lambda f: os.path.isdir(os.path.join(self.images_folder, f)), contents)

    def get_image_folder_contents(self, folder):
        valid_exts = ('.jpg', '.png')
        path = os.path.join(self.images_folder, folder)
        contents = map(lambda f: f.name, os.scandir(path))
        yield from filter(lambda f: any(f.endswith(ext) for ext in valid_exts), contents)

    def load(self):
        with open(os.path.join(self.current_dir, 'config.ini'), 'w') as f:
            self.set_contents(json.loads(f))
    
    def save(self):
        with open(os.path.join(self.current_dir, 'config.ini'), 'w') as f:
            f.write(json.dumps(self.get_contents))

    def get_contents(self):
        return {
            'image_dir' : self.images_folder,
            'label_dir' : self.labels_folder,
            'save_dir'  : self.save_location
        }
    
    def set_contents(self, param):
        self.images_folder = param.get('image_dir', self.images_folder)
        self.labels_folder = param.get('label_dir', self.labels_folder)
        self.save_location = param.get('save_dir',  self.save_location)

    def delete_image(self, img_name):
        os.remove(os.path.join(self.images_folder, img_name))

class ImageViewer(QFrame):
    def __init__(self, image = None):
        super().__init__()
        self.setMinimumSize(QSize(850, 725))
        # self.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.image = QPixmap(image)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0,0, self.image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.end()



class Central(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('Central { background: rgb(30,30,30); }')
        self.layout         = QHBoxLayout(self)
        # self.images_layout  = FlowLayout()
        self.focused_image  = ImageViewer('C:\\Users\\draug\\Desktop\\floof.png')
        self.folder_list    = FolderList(file_manager.get_images_folders())
        self.folder_list.setMaximumWidth(300)
        
        
        self.layout.addWidget(self.focused_image)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.folder_list)
        # self.layout.setAlignment(self.folder_list, Qt.AlignRight)

        self.folder_list.selectedChanged.connect(self.tell)

    def tell(self, param):
        print(param.data(data=Qt.UserRole))
        
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global file_manager
        file_manager = FileManager()

        central = Central()
        self.setCentralWidget(central)
        self.setWindowTitle('Label Maker')
        self.setWindowIcon(QIcon(os.path.join(file_manager.current_dir, 'logo.ico')))

def main():
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()