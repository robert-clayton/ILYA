import pandas as pd

class BoxFactory():
    '''Handles boxes---rows---in general: saving, loading, parsing'''
    def __init__(self):
        self.oldBoxes = []
        self.newBoxes = []
        self.csvFile = None
        
    
    def loadCSV(self, csvFile=None):
        if not csvFile: csvFile = self.csvFile

class Box():
    '''A single row of the generated dataset'''

    def __init__(image_id = '', source = '', label_name = '', confidence = 1.0, 
                xmin = 0.0, xmax = 0.0, ymin = 0.0, ymax = 0.0, 
                is_occluded = False, is_group_of = False, is_depiction = False, is_inside = False):
        self.image_id       = image_id
        self.source         = source
        self.label_name     = label_name
        self.confidence     = confidence
        self.xmin           = xmin
        self.xmax           = xmax
        self.ymin           = ymin
        self.ymax           = ymax
        self.is_occluded    = is_occluded
        self.is_group_of    = is_group_of
        self.is_depiction   = is_depiction
        self.is_inside      = is_inside

    def get_row(self):
        return [self.image_id, self.source, self.label_name, self.confidence, 
                self.xmin, self.xmax, self.ymin, self.ymax, 
                self.is_occluded, self.is_group_of, self.is_depiction, self.is_inside]