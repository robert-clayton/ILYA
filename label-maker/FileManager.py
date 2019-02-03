from PySide2.QtCore import *
import os

class FileManager(QObject):
    '''Handles grabbing files and saving boxes as they are generated'''
    
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