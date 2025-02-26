from typing import Optional, overload
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ..Common.StyleSheet import *
from ..Common.QFunctions import *
from .Menu import MenuBase

##############################################################################################################################

class SpinBoxBase(QSpinBox):
    """
    Base class for spinBox components
    """
    _contextMenu = None

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        StyleSheetBase.SpinBox.apply(self)

    def wheelEvent(self, event: QWheelEvent) -> None:
        event.ignore()

    @property
    def contextMenu(self):
        if self._contextMenu is None:
            self._contextMenu = MenuBase(self)
        return self._contextMenu

    @contextMenu.setter
    def contextMenu(self, menu: MenuBase):
        ''''''
        self._contextMenu = menu

    def setContextMenu(self, actions: dict)-> None:
        self.setContextMenuPolicy(Qt.CustomContextMenu) if self.contextMenuPolicy() != Qt.CustomContextMenu else None
        self.customContextMenuRequested.connect(
            lambda position: (
                self.contextMenu.clear(),
                showContextMenu(self, self.contextMenu, actions, self.mapToGlobal(position))
            )
        )

    def setBorderless(self, borderless: bool) -> None:
        self.setProperty("isBorderless", borderless)

    def setTransparent(self, transparent: bool) -> None:
        self.setProperty("isTransparent", transparent)

    def clearDefaultStyleSheet(self) -> None:
        StyleSheetBase.SpinBox.deregistrate(self)

##############################################################################################################################

class DoubleSpinBoxBase(QDoubleSpinBox):
    """
    Base class for doubleSpinBox components
    """
    _contextMenu = None

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        StyleSheetBase.SpinBox.apply(self)

    def wheelEvent(self, event: QWheelEvent) -> None:
        event.ignore()

    @property
    def contextMenu(self):
        if self._contextMenu is None:
            self._contextMenu = MenuBase(self)
        return self._contextMenu

    @contextMenu.setter
    def contextMenu(self, menu: MenuBase):
        ''''''
        self._contextMenu = menu

    def setContextMenu(self, actions: dict)-> None:
        self.setContextMenuPolicy(Qt.CustomContextMenu) if self.contextMenuPolicy() != Qt.CustomContextMenu else None
        self.customContextMenuRequested.connect(
            lambda position: (
                self.contextMenu.clear(),
                showContextMenu(self, self.contextMenu, actions, self.mapToGlobal(position))
            )
        )

    def setBorderless(self, borderless: bool) -> None:
        self.setProperty("isBorderless", borderless)

    def setTransparent(self, transparent: bool) -> None:
        self.setProperty("isTransparent", transparent)

    def clearDefaultStyleSheet(self) -> None:
        StyleSheetBase.SpinBox.deregistrate(self)

##############################################################################################################################