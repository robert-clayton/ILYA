import pandas as pd
import ThemeManager
from PySide2.QtCore import Signal, QObject

class BoxManager(QObject):
    '''Handles adding and removing rows to and from the dataset'''

    def __init__(self):
        super().__init__()
        self._dataFrame = pd.read_csv(ThemeManager.DATA_PATH)
        self._labels = self.loadLabels()

        # new box variables
        self._newBoxLabelName   = 'Default' # Give Functionality to this
        self._newBoxIsOccluded  = False
        self._newBoxIsTruncated = False
        self._newBoxIsGroupOf   = False
        self._newBoxIsDepiction = False
        self._newBoxIsInside    = False
    
    def setNewBoxLabelName(self, param):
        self._newBoxLabelName = param
        self.newBoxLabelNameChanged.emit(param)

    def setNewBoxIsOccluded(self, param):
        self._newBoxIsOccluded = param
        self.newBoxIsOccludedChanged.emit(param)

    def setNewBoxIsTruncated(self, param):
        self._newBoxIsTruncated = param
        self.newBoxIsTruncatedChanged.emit(param)
    
    def setNewBoxIsGroupOf(self, param):
        self._newBoxIsGroupOf = param
        self.newBoxIsGroupOfChanged.emit(param)

    def setNewBoxIsDepiction(self, param):
        self._newBoxIsDepiction = param
        self.newBoxIsDepictionChanged.emit(param)
    
    def setNewBoxIsInside(self, param):
        self._newBoxIsInside = param
        self.newBoxIsInsideChanged.emit(param)

    def getBoxesForImage(self, imageID):
        matches = self._dataFrame.loc[self._dataFrame['ImageID'] == imageID]
        return [Box(*matchList) for matchList in matches.values.tolist()]

    def addBoxToDataFrame(self, imageID, xMin, xMax, yMin, yMax):
        box =   [imageID, 
                'label-maker', 
                self._newBoxLabelName,
                1.0,
                xMin, xMax, yMin, yMax,
                self._newBoxIsOccluded,
                self._newBoxIsTruncated,
                self._newBoxIsGroupOf,
                self._newBoxIsDepiction,
                self._newBoxIsInside]
        self._dataFrame.loc[len(self._dataFrame)] = box
        return Box(*box)

    def saveDataFrame(self):
        self._dataFrame.to_csv(ThemeManager.DATA_PATH, index=False)

    def loadLabels(self):
        with open(ThemeManager.LABELS_PATH, 'r') as labels:
            return [label.rstrip('\n') for label in labels]

    newBoxLabelNameChanged    = Signal(object)
    newBoxIsOccludedChanged   = Signal(object)
    newBoxIsTruncatedChanged  = Signal(object)
    newBoxIsGroupOfChanged    = Signal(object)
    newBoxIsDepictionChanged  = Signal(object)
    newBoxIsInsideChanged     = Signal(object)

class Box():
    '''A single row to add to the dataset'''

    def __init__(self, imageID = '', source = '', labelName = '', confidence = 1.0, 
                xMin = 0.0, xMax = 0.0, yMin = 0.0, yMax = 0.0, 
                isOccluded = False, isTruncated = False, isGroupOf = False, 
                isDepiction = False, isInside = False):
        self.imageID    = imageID
        self.source     = source
        self.labelName  = labelName
        self.confidence = confidence
        self.xMin       = xMin
        self.xMax       = xMax
        self.yMin       = yMin
        self.yMax       = yMax
        self.isOccluded = isOccluded
        self.isTruncated= isTruncated
        self.isGroupOf  = isGroupOf
        self.isDepiction= isDepiction
        self.isInside   = isInside

    def getData(self):
        return [self.imageID, self.source, self.labelName, self.confidence, 
                self.xMin, self.xMax, self.yMin, self.yMax, 
                self.isOccluded, self.isTruncated, self.isGroupOf, 
                self.isDepiction, self.isInside]
    
    def getRect(self):
        return (self.xMin, self.xMax, self.yMin, self.yMax)

    def getLabel(self):
        return self.labelName