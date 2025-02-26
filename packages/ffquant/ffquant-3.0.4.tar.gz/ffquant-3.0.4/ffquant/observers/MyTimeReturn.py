import backtrader as bt
import pytz
import ffquant.utils.global_backtest_data as global_backtest_data

__ALL__ = ['MyTimeReturn']

class MyTimeReturn(bt.observers.TimeReturn):
    def __init__(self):
        super(MyTimeReturn, self).__init__()
        self.treturns = global_backtest_data.treturns

    def start(self):
        super(MyTimeReturn, self).start()
        self.treturns.clear()

    # 这个next方法会在策略的next方法之后执行
    def next(self):
        super(MyTimeReturn, self).next()
        msg = {
            "datetime": self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "timereturn": self.lines.timereturn[0]
        }
        self.treturns.append(msg)
