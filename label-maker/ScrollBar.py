from PySide2            import *
from PySide2.QtCore     import *
from PySide2.QtWidgets  import *
from PySide2.QtGui      import *
import ThemeManager

class ScrollBar(QScrollBar):
    def __init__(self, parent_ref = None, kinetic_scroll = True):
        super().__init__(parent_ref)
        self.kinetic_scroll = kinetic_scroll
        if parent_ref and kinetic_scroll: 
            parent_ref.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
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
        if self.kinetic_scroll:
            dy = event.angleDelta().y() / 2
            try:
                dy += self.scroll_animation.currentValue() - self.scroll_animation.endValue()
            except:
                pass

            self.lerp_curve = QEasingCurve(QEasingCurve.InOutQuad)
            self.scroll_animation = QPropertyAnimation(self, b'value')
            
            self.scroll_animation.setDuration(100)
            self.scroll_animation.setEasingCurve(self.lerp_curve)
            self.scroll_animation.setStartValue(self.value())
            self.scroll_animation.setEndValue(self.value() - dy)
            self.scroll_animation.start()
        else:
            super().wheelEvent(event)