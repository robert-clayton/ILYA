import ThemeManager
from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *

class ScrollBar(QScrollBar):
    '''Kinetic-scrolling and styled sidebar'''
    def __init__(self, parentRef = None, kineticScroll = True):
        super().__init__(parentRef)
        self.kineticScroll = kineticScroll
        if parentRef and kineticScroll: 
            parentRef.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        self.setStyleSheet(
           'ScrollBar::handle:vertical {'
                'background: ' + ThemeManager.ACCENT + ';'
                'min-height: 20px;'
                'border-radius: 3px;'
            '}'
            'ScrollBar:up-arrow:vertical, ScrollBar::down-arrow:vertical {'
                'color: none;'
                'border: none;'
                'background: none;'
            '}'
            'ScrollBar::add-line:vertical,  ScrollBar::sub-line:vertical {'
                'border: none;'
                'background: none;'
            '}'
            'ScrollBar:vertical {'
                'border: 0px;'
                'border-radius: 3px;'
                'background: transparent;'
                'width: 7px;'
            '}'
            'ScrollBar::sub-page:vertical, ScrollBar::add-page:vertical {'
                'background: none;'
                'border-radius: 3px;'
            '}')

    def wheelEvent(self, event):
        if self.kineticScroll:
            dy = event.angleDelta().y() / 2
            try:
                dy += self.scrollAnimation.currentValue() - self.scrollAnimation.endValue()
            except:
                pass

            self.lerpCurve = QEasingCurve(QEasingCurve.InOutQuad)
            self.scrollAnimation = QPropertyAnimation(self, b'value')
            self.scrollAnimation.setDuration(100)
            self.scrollAnimation.setEasingCurve(self.lerpCurve)
            self.scrollAnimation.setStartValue(self.value())
            self.scrollAnimation.setEndValue(self.value() - dy)
            self.scrollAnimation.start()
        else:
            super().wheelEvent(event)