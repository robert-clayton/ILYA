from PySide2.QtCore import *
import os
import csv

class FileManager():
    '''Handles grabbing files and saving boxes as they are generated'''
    currentDir    = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    saveLocation  = os.path.dirname(os.path.realpath(__file__))
    imagesFolder  = os.path.join(currentDir, 'Images')
    labelsFolder  = os.path.join(currentDir, 'Labels')

    def getImagesFolders(self):
        contents = map(lambda f: f.name, os.scandir(self.imagesFolder))
        yield from filter(lambda f: os.path.isdir(os.path.join(self.imagesFolder, f)), contents)

    def getImageFolderContents(self, folder):
        validExts = ('.jpg', '.jpeg', '.png')
        path = os.path.join(self.imagesFolder, folder)
        contents = map(lambda f: f.name, os.scandir(path))
        yield from filter(lambda f: any(f.endswith(ext) for ext in validExts), contents)
    
    def getLabels(self):
        try:
            with open(os.path.join(self.currentDir, 'labels.txt'), 'r') as f:
                return f.read()
        except:
            return []

    def deleteImage(self, imgData):
        os.remove(imgData.data(role=Qt.UserRole))
        imgData.model().removeRow(imgData.row())