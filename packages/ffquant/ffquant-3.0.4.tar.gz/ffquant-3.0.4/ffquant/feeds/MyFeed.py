import backtrader as bt
import requests
import os
from datetime import datetime, timedelta, timezone
from ffquant.utils.Logger import stdout_log
import pytz
import pandas_market_calendars as pmc

__ALL__ = ['MyFeed']

# 该DataFeed用于回测目的 基本流程介绍如下
# 1. 准备backfill的数据 一次性拉取到本地 放到cache_data_list
# 2. 准备start_time到end_time代表的range的数据 一次性拉取到本地 放到cache_data_list
# 3. 填补cache_data_list中的空隙数据
# 4. 在_load中将cache_data_list中的数据返回给框架 直到cache_data_list没有数据为止
class MyFeed(bt.feeds.DataBase):
    params = (
        ('url', 'http://192.168.25.127:8288/symbol/info/list'),
        ('symbol', None),
        ('start_time', None),
        ('end_time', None),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1),
        ('debug', False),
        ('backfill_size', 0),
        ('check_backfill_size', True),
        ('market', 'HKEX'),
    )

    # backtrade默认只有open high low close volume openinterest这几个line 我们在这里加上代表成交额的turnover
    lines = (('turnover'),)

    def __init__(self):
        if self.p.start_time is None or self.p.end_time is None or self.p.symbol is None:
            raise ValueError("Missing required parameters")
        self.cache_data_list = []
        self.cur_index = 0

        self.pmc = pmc.get_calendar(self.p.market)
        start_date = datetime.strptime(self.p.start_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        end_date = datetime.strptime(self.p.end_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        self.schedule = self.pmc.schedule(start_date=start_date, end_date=end_date)

    def is_tradable(self, dt: datetime) -> bool:
        dt = dt.astimezone(pytz.utc)

        date_str = dt.strftime('%Y-%m-%d')

        if date_str not in self.schedule.index:
            return False

        open_time = self.schedule.loc[date_str]['market_open'].to_pydatetime()
        brk_start_time = self.schedule.loc[date_str]['break_start'].to_pydatetime()
        brk_end_time = self.schedule.loc[date_str]['break_end'].to_pydatetime()
        close_time = self.schedule.loc[date_str]['market_close'].to_pydatetime()

        # 这里需要考虑backfill_size而扩展出来的可交易时间 每一天都要考虑
        if self.p.backfill_size > 0:
            tdelta = timedelta(minutes=self.p.compression * self.p.backfill_size)
            if self.p.timeframe == bt.TimeFrame.Seconds:
                tdelta = timedelta(seconds=self.p.compression * self.p.backfill_size)
            open_time = open_time - tdelta
        return open_time <= dt < brk_start_time or brk_end_time <= dt < close_time

    def start(self):
        super().start()

        self.prepare_backfill_data()

        start_time = datetime.strptime(self.p.start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(self.p.end_time, '%Y-%m-%d %H:%M:%S')
        self.prepare_range_data(start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S'))

        self.fill_gap()

    # start方法的调用先于next 但是start方法被调用时 strategy的minperiod还没有被确定 next方法被调用时 strategy的minperiod已经确定
    # 需要根据策略的minperiod来限制backfill_size 所以限制backfill_size需要在next方法中
    def next(self, datamaster=None, ticks=True):
        # 在开始加载行情之前 先判断是否需要截断backfill_size
        # 因为在start方法中 无法判断minperiod
        # if self.cur_index == 0:
        #     running_strats = self._env.runningstrats
        #     max_minperiod = max([strat._minperiod for strat in running_strats])
        #     if self.p.check_backfill_size and self.p.backfill_size > max_minperiod - 1:
        #         stdout_log(f"[CRITICAL], {self.__class__.__name__}, backfill_size({self.p.backfill_size}) > max_minperiod({max_minperiod}), truncate cache_data_list")
        #         self.cache_data_list = self.cache_data_list[(self.p.backfill_size - max_minperiod):]
        #         self.p.backfill_size = max_minperiod - 1

        return super().next(datamaster, ticks)

    def prepare_backfill_data(self):
        if self.p.backfill_size > 0:

            end_time = datetime.strptime(self.p.start_time, '%Y-%m-%d %H:%M:%S')
            start_time = end_time - timedelta(minutes=self.p.backfill_size * self.p.compression)
            if self.p.timeframe == bt.TimeFrame.Seconds:
                start_time = end_time - timedelta(seconds=self.p.backfill_size * self.p.compression)

            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
            self.prepare_range_data(start_time_str, end_time_str)

    def prepare_range_data(self, start_time_str, end_time_str):
        params = {
            'startTime': start_time_str,
            'endTime': end_time_str,
            'symbol': self.p.symbol
        }

        if self.p.timeframe == bt.TimeFrame.Seconds:
            params['interval'] = f'{self.p.compression}S'

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, fetch data params: {params}")

        response = requests.get(self.p.url, params=params).json()
        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, fetch data response: {response}")

        if response.get('code') != '200':
            raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

        results = response.get('results', [])
        if results is not None:
            results.sort(key=lambda x: x['timeClose'])
            for result in results:
                # 因为交易时间的比较是按照左闭右开的规则 所以这里要使用timeOpen来判断指定时间是否可交易
                if self.is_tradable(datetime.fromtimestamp(result['timeOpen'] / 1000.0, timezone.utc)):
                    self.cache_data_list.append(result)

    # 填充空隙数据 如果某根k先缺失 则它的价格的OHLC都继承自上一根k线的close价格 volume和turnover都为0
    def fill_gap(self):
        interval = 60 * self.p.compression
        if self.p.timeframe == bt.TimeFrame.Seconds:
            interval = self.p.compression

        tmp_list = []
        for i in range(0, len(self.cache_data_list)):
            if i == 0:
                tmp_list.append(self.cache_data_list[i])
                continue

            prev_data = self.cache_data_list[i - 1]
            cur_data = self.cache_data_list[i]
            if cur_data['timeClose'] / 1000 - prev_data['timeClose'] / 1000 > interval:
                for j in range(1, int((cur_data['timeClose'] / 1000 - prev_data['timeClose'] / 1000) / interval)):
                    # 因为交易时间的比较是按照左闭右开的规则 所以这里要使用timeOpen来判断指定时间是否可交易
                    if self.is_tradable(datetime.fromtimestamp((prev_data['timeOpen'] + interval * j * 1000) / 1000.0, timezone.utc)):
                        inherited_data = {}
                        inherited_data['type'] = prev_data['type']
                        inherited_data['symbol'] = prev_data['symbol']
                        inherited_data['timeOpen'] = prev_data['timeOpen'] + interval * j * 1000
                        inherited_data['timeClose'] = inherited_data['timeOpen'] + interval * 1000
                        inherited_data['createTime'] = 0
                        inherited_data['updateTime'] = 0
                        inherited_data['open'] = prev_data['close']
                        inherited_data['high'] = prev_data['close']
                        inherited_data['low'] = prev_data['close']
                        inherited_data['close'] = prev_data['close']
                        inherited_data['vol'] = 0
                        inherited_data['turnover'] = 0
                        tmp_list.append(inherited_data)
                        stdout_log(f"{self.__class__.__name__}, fill_gap, kline time: {datetime.fromtimestamp(inherited_data['timeClose'] / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}, filled data: {inherited_data}")
            tmp_list.append(cur_data)
        self.cache_data_list = tmp_list

    def _load(self):
        result = True
        if self.cur_index < len(self.cache_data_list):
            bar = self.cache_data_list[self.cur_index]
            self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(bar['timeClose'] / 1000.0, timezone.utc))
            self.lines.open[0] = bar['open']
            self.lines.high[0] = bar['high']
            self.lines.low[0] = bar['low']
            self.lines.close[0] = bar['close']
            self.lines.volume[0] = bar['vol']
            self.lines.turnover[0] = bar['turnover']
            self.cur_index += 1

            kline_local_time_str = datetime.fromtimestamp(bar['timeClose'] / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
            create_time_str = datetime.fromtimestamp(bar['createTime'] / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
            stdout_log(f"[INFO], {self.__class__.__name__}, kline time: {kline_local_time_str}, create time: {create_time_str}, open: {self.lines.open[0]}, high: {self.lines.high[0]}, low: {self.lines.low[0]}, close: {self.lines.close[0]}")
        else:
            result = False
        return result