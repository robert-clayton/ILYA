from PySide2.QtCore import *
import os
import csv

class FileManager():
    '''Handles grabbing files and saving boxes as they are generated'''
    current_dir    = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    save_location  = os.path.dirname(os.path.realpath(__file__))
    images_folder  = os.path.join(current_dir, 'Images')
    labels_folder  = os.path.join(current_dir, 'Labels')

    def get_images_folders(self):
        contents = map(lambda f: f.name, os.scandir(self.images_folder))
        yield from filter(lambda f: os.path.isdir(os.path.join(self.images_folder, f)), contents)

    def get_image_folder_contents(self, folder):
        valid_exts = ('.jpg', '.jpeg', '.png')
        path = os.path.join(self.images_folder, folder)
        contents = map(lambda f: f.name, os.scandir(path))
        yield from filter(lambda f: any(f.endswith(ext) for ext in valid_exts), contents)
    
    def get_labels(self):
        try:
            with open(os.path.join(self.current_dir, 'labels.txt'), 'r') as f:
                return f.read()
        except:
            return []

    def delete_image(self, img_name):
        os.remove(os.path.join(self.images_folder, img_name))