import os
from PySide2.QtCore import Qt

def getImageFolders():
    contents = map(lambda f: f.name, os.scandir(imagesFolder))
    yield from filter(lambda f: os.path.isdir(os.path.join(imagesFolder, f)), contents)

def getImageFolderContents(folder):
    validExts = ('.jpg', '.jpeg', '.png')
    path = os.path.join(imagesFolder, folder)
    contents = map(lambda f: f.name, os.scandir(path))
    yield from filter(lambda f: any(f.endswith(ext) for ext in validExts), contents)

def getLabels():
    try:
        with open(os.path.join(currentDir, 'labels.txt'), 'r') as f:
            return f.read()
    except:
        return []

def deleteImage(imgData):
    os.remove(imgData.data(role=Qt.UserRole))
    imgData.model().removeRow(imgData.row())

currentDir      = os.getcwd()
imagesFolder    = os.path.join(currentDir, 'Images')
labelsFolder    = os.path.join(currentDir, 'Labels')
iconPath        = os.path.join(currentDir, 'logo.ico')