import time
from typing import Dict, List

import pyqtgraph as pg
from pydantic import BaseModel
from qtpy import QtCore, QtWidgets

from .datapoint import DataPointTracker

# Set background color
pg.setConfigOption("background", "w")

# 15 distinct colors
PLOT_COLORS = [
    [0, 0, 0],
    [230, 25, 75],
    [60, 180, 75],
    [255, 225, 25],
    [0, 130, 200],
    [245, 130, 48],
    [145, 30, 180],
    [70, 240, 240],
    [240, 50, 230],
    [210, 245, 60],
    [250, 190, 190],
    [0, 128, 128],
    [230, 190, 255],
    [170, 110, 40],
    [255, 250, 200],
]


class PlotMarkerConfig(BaseModel):
    color: List[int | float] = [0, 0, 0]
    size: int = 3
    symbol: str = "o"

    def get_brush(self):
        return pg.mkBrush(color=self.color)

    def get_pen(self):
        return pg.mkPen(None)


class PlotLineConfig(BaseModel):
    color: List[int | float] = [0, 0, 0]
    line_width: int = 2

    def get_pen(self):
        return pg.mkPen(color=self.color, width=self.line_width)


class PlotTraceConfig(BaseModel):
    line: PlotLineConfig = PlotLineConfig()
    marker: PlotMarkerConfig = PlotMarkerConfig()


class TimeseriesTrace:
    datapoint: DataPointTracker
    plot_widget: pg.PlotWidget
    plot_trace: pg.PlotDataItem

    def __init__(self, config: PlotTraceConfig, plot_widget: pg.PlotWidget, datapoint: DataPointTracker):
        self.config = config
        self.plot_widget = plot_widget
        self.datapoint = datapoint
        self.start_time = time.time()
        self.plot_trace = self.plot_widget.plot(name=self.datapoint.id)
        self.plot_trace.setPen(self.config.line.get_pen())

        # enable marker
        if config.marker:
            self.plot_trace.setSymbol(config.marker.symbol)
            self.plot_trace.setSymbolBrush(config.marker.get_brush())
            self.plot_trace.setSymbolSize(config.marker.size)
            self.plot_trace.setSymbolPen(config.marker.get_pen())

    def update_data(self):
        """Updates the data in the plot"""
        self.plot_trace.setData(self.datapoint.timestamps - self.start_time, self.datapoint.series)  # type: ignore


class TimeseriesGraphDisplay(QtWidgets.QWidget):
    active_series: Dict[DataPointTracker, TimeseriesTrace]

    def __init__(self):
        super(TimeseriesGraphDisplay, self).__init__()
        self.active_series = {}
        self.treeitems_struct = {}

        self.series: Dict[str, TimeseriesTrace] = {}

        self.plotter = pg.PlotWidget()
        self.plotter.addLegend()
        self.plotter.showGrid(x=True, y=True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plotter)

        self.setLayout(layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def add_datapoint(self, data: DataPointTracker):
        config = PlotTraceConfig(
            line=PlotLineConfig(color=PLOT_COLORS[len(self.active_series)]),  # type: ignore
            marker=PlotMarkerConfig(color=PLOT_COLORS[len(self.active_series)]),  # type: ignore
        )
        self.active_series[data] = TimeseriesTrace(config, self.plotter, data)

    def update_data(self):
        """Regenerates the trace for all the active series"""
        for series in self.active_series.values():
            series.update_data()
