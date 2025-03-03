from typing import Dict

import pyqtgraph as pg
from pydantic import BaseModel
from qtpy import QtCore, QtWidgets

from ..datapoint import DataPointTracker

# Set background color
pg.setConfigOption("background", "w")

import numpy as np

PLOT_COLORS = np.random.rand(100, 3) * 255


class KeyValueDisplay(QtWidgets.QWidget):
    class Config(BaseModel):
        pass

    def __init__(self, config: Config, datapoint: DataPointTracker):
        super(KeyValueDisplay, self).__init__()
        self.config = config
        self.datapoint = datapoint

        self.label = QtWidgets.QLabel()
        self.label.setText(datapoint.id)

        self.value = QtWidgets.QLCDNumber()
        self.value.setDigitCount(3)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.value)

        self.setLayout(layout)
        self.update()

    def update(self):  # type: ignore
        self.value.display(self.datapoint.last_value)


class NumberGraphDisplay(QtWidgets.QWidget):
    active_series: Dict[DataPointTracker, KeyValueDisplay]

    def __init__(self):
        super(NumberGraphDisplay, self).__init__()
        self.active_series = {}

        self.series: Dict[str, KeyValueDisplay] = {}

        self.data_layout = QtWidgets.QVBoxLayout()
        self.test_label = QtWidgets.QLabel()
        self.test_label.setText("Test")
        self.data_layout.addWidget(self.test_label)
        self.setLayout(self.data_layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def add_datapoint(self, data: DataPointTracker):
        print("Adding datapoint")
        display = KeyValueDisplay(KeyValueDisplay.Config(), data)
        self.active_series[data] = display
        self.data_layout.addWidget(display)

    def update(self):  # type: ignore
        for series in self.active_series.values():
            series.update()
