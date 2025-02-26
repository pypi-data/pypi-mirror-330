from typing import Optional, overload
from PyEasyUtils import singledispatchmethod
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ..Common.Icon import *
from ..Common.StyleSheet import *
from ..Common.QFunctions import *

##############################################################################################################################

class SplitterBase(QSplitter):
    """
    Base class for splitter components
    """
    @singledispatchmethod
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        StyleSheetBase.Splitter.apply(self)

    @__init__.register
    def _(self, arg__1: Qt.Orientation, parent: QWidget = None) -> None:
        self.__init__(parent)
        self.setOrientation(arg__1)

    def setBorderless(self, borderless: bool) -> None:
        self.setProperty("isBorderless", borderless)

    def setTransparent(self, transparent: bool) -> None:
        self.setProperty("isTransparent", transparent)

    def clearDefaultStyleSheet(self) -> None:
        StyleSheetBase.Splitter.deregistrate(self)

##############################################################################################################################