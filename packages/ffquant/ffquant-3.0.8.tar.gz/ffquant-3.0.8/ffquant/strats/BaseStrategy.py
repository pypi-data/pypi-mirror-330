import backtrader as bt
from ffquant.utils.Logger import Logger

class BaseStrategy(bt.Strategy):

    params = (
        ('name', None),
        ('logger', None),
    )

    def __init__(self):
        if self.p.logger is not None:
            self.logger = self.p.logger
        elif self.p.name is not None:
            self.logger = Logger(self.p.name)