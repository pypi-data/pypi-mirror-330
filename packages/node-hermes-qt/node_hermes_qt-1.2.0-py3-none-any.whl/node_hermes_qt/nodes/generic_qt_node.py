from abc import ABC, abstractmethod
from typing import Literal, Type
from enum import Enum
from pydantic import BaseModel
from qtpy import QtWidgets, QtCore


class GenericNodeWidget(QtWidgets.QWidget):
    def __init__(self, component: "GenericQtNode"):
        super().__init__()
        self.node = component


class TabConfig(BaseModel):
    type: Literal["tab"]
    name: str


class DockConfig(BaseModel):
    class DockWidgetPosition(Enum):
        LEFT = "left"
        RIGHT = "right"
        TOP = "top"
        BOTTOM = "bottom"
        FLOATING = "floating"

        def to_qt(self) -> QtCore.Qt.DockWidgetArea | None:
            if self == DockConfig.DockWidgetPosition.LEFT:
                return QtCore.Qt.DockWidgetArea.LeftDockWidgetArea
            elif self == DockConfig.DockWidgetPosition.RIGHT:
                return QtCore.Qt.DockWidgetArea.RightDockWidgetArea
            elif self == DockConfig.DockWidgetPosition.TOP:
                return QtCore.Qt.DockWidgetArea.TopDockWidgetArea
            elif self == DockConfig.DockWidgetPosition.BOTTOM:
                return QtCore.Qt.DockWidgetArea.BottomDockWidgetArea
            elif self == DockConfig.DockWidgetPosition.FLOATING:
                return None

    type: Literal["dock"]
    name: str
    position: DockWidgetPosition


class GenericQtNode(ABC):
    class Config(BaseModel):
        interface: TabConfig | DockConfig | None = None

    @property
    @abstractmethod
    def widget(self) -> Type[GenericNodeWidget]:
        raise NotImplementedError
