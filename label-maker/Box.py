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
        self.is_occluded    = is_occluded
        self.is_group_of    = is_group_of
        self.is_depiction   = is_depiction
        self.is_inside      = is_inside