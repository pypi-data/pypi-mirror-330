import polars as pl
from node_hermes_core.utils.frequency_counter import FrequencyCounter
from pydantic import BaseModel


class DataPointTracker:
    series: pl.Series | None = None
    timestamps: pl.Series | None = None

    class Config(BaseModel):
        cache_size: int = 5000

    def __init__(self, config: Config, id: str):
        self.config = config
        self.id = id
        self.last_value = 0
        self.display_name = id
        self.frequency_counter = FrequencyCounter()

    @property
    def name(self):
        return self.display_name

    def update(self, value: pl.Series, timestamp: pl.Series):
        if len(value) == 0:
            return

        if self.series is None:
            self.series = pl.Series(value)
        else:
            self.series = pl.concat([self.series, value])

        if self.timestamps is None:
            self.timestamps = pl.Series(timestamp)
        else:
            self.timestamps = pl.concat([self.timestamps, timestamp])

        self.last_value = value[-1]
        self.frequency_counter.update(len(value), timestamp[-1])

        # Trim the series
        if len(self.series) > self.config.cache_size:
            self.series = self.series.slice(self.config.cache_size//10)
            self.timestamps = self.timestamps.slice(self.config.cache_size//10)

    def __hash__(self):
        return hash(self.id)
