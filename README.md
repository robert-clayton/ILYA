# Image Labels You Affix - ILYA [![](https://badgen.net/github/license/robert-clayton/ILYA)](https://github.com/robert-clayton/ILYA/edit/master/LICENSE.txt) ![](https://badgen.net/github/last-commit/robert-clayton/ILYA)

A tool for labeling bounding boxes on images to be used for ML training.

# Requirements

- Python 3.x

# Installation

- Open `cmd` and `cd` into the project folder
- Run `pip install -r requirements.txt`

# How To Use

- Put images into a subfolder within `./Images/`
- Run app with `python3 main.py`
- Select the folder you want to label
- Press the `Load Images` button to begin
- Click and drag a box around the desired area
- Select proper label from the popup
- Repeat until finished with image
- Press `Next` to move to the next image, or use the `Spacebar` shortcut
- Labels are stored in the `Labels` subfolder


# Data Format
Taking a cue from Google's Open Images Dataset V4, boxes are saved in CSV format with the following columns:

- ImageID: String - The image this box belongs to as a relative path inside `Images`
- Source: String - How the box was made. Everything produced by `label-maker` will be `xclick`
- LabelName: String - What class this box is represents. Set the class list in `labels.txt`
- Confidence: Float - Dummy value, always 1.0
- XMin, XMax, YMin, YMax: Float - Box coordinates, normalized to the image as [0.0 ... 1.0]
- IsOccluded: Bool - Whether the object is occluding by another object
- IsTruncated: Bool - Whether the object is a part of the LabelName object
- IsGroupOf: Bool - Whether the object is a group of the LabelName object
- IsDepiction: Bool - Whether the object is a depiction of the LabelName object
- IsInside: Bool - Whether the object is the inside of the LabelName object
