from typing import Optional, overload
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ..Common.Icon import *
from ..Common.StyleSheet import *
from ..Common.QFunctions import *
from .Button import ButtonBase

##############################################################################################################################

class ProgressBarBase(QProgressBar):
    """
    Base class for progressBar components
    """
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        StyleSheetBase.ProgressBar.apply(self)

    def setBorderless(self, borderless: bool) -> None:
        self.setProperty("isBorderless", borderless)

    def setTransparent(self, transparent: bool) -> None:
        self.setProperty("isTransparent", transparent)

    def clearDefaultStyleSheet(self) -> None:
        StyleSheetBase.ProgressBar.deregistrate(self)


class ClickableProgressBar(ProgressBarBase):
    """
    Clickable progressBar component
    """
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.exectuteButton = ButtonBase(self)
        self.exectuteButton.setIcon(IconBase.Play)
        self.pauseButton = ButtonBase(self)
        self.pauseButton.setIcon(IconBase.Pause)
        self.terminateButton = ButtonBase(self)
        self.terminateButton.setIcon(IconBase.X)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(self.exectuteButton)
        layout.addWidget(self.pauseButton)
        layout.addWidget(self.terminateButton)

        self.setRange(0, 100)
        self.setValue(0)

##############################################################################################################################