import backtrader as bt
from ffquant.utils.Logger import Logger, stdout_log
import pytz

class BaseStrategy(bt.Strategy):
    params = (
        ('name', None),
        ('logger', None),
        ('debug', None),
        ('test', None),
    )

    def __init__(self):
        if self.p.logger is not None:
            self.logger = self.p.logger
        elif self.p.name is not None:
            self.logger = Logger(self.p.name)

    def next(self):
        cur_bar_date_str = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d")
        prev_bar_date_str = self.data.datetime.datetime(-1).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d")
        if prev_bar_date_str < cur_bar_date_str:
            stdout_log.info(f"re-initialize strategy due to date change from {prev_bar_date_str} to {cur_bar_date_str}")
            self.initialize()
            self.start()

    def initialize(self):
        pass

    def start(self):
        pass