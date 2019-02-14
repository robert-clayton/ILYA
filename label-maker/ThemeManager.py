from PySide2.QtGui import QColor
import os

CURRENT_DIR         = os.getcwd()
RESOURCES_PATH      = os.path.join(CURRENT_DIR,     'Resources')
IMAGE_FOLDERS_PATH  = os.path.join(CURRENT_DIR,     'Images')
DATA_PATH           = os.path.join(CURRENT_DIR,     'data.csv')
LABELS_PATH         = os.path.join(CURRENT_DIR,     'labels.txt')
ICON_PATH           = os.path.join(RESOURCES_PATH,  'logo.ico')
CHECKED_PATH        = os.path.join(RESOURCES_PATH,  'checked.png')
UNCHECKED_PATH      = os.path.join(RESOURCES_PATH,  'unchecked.png')

TOP_BAR     = 'rgba(70,70,70,255)'
LABEL       = 'rgba(200,200,200,255)'
LABEL_DARK  = 'rgba(20,20,20,255)'
ACCENT      = 'rgba(237,182,234,255)'
BG          = 'rgba(30,30,30,255)'
BG_L1       = 'rgba(40,40,40,255)'
BG_L2       = 'rgba(50,50,50,255)'

ACCENT_QC               = QColor(237,182,234,255)
ACCENT_LOW_OPACITY_QC   = QColor(237,182,234,40)
ACCENT_VLOW_OPACITY_QC  = QColor(237,182,234,25)
LABEL_QC                = QColor(200,200,200,255)
LABEL_LOW_OPACITY_QC    = QColor(200,200,200,70)
BG_L2_QC                = QColor(50,50,50,255)