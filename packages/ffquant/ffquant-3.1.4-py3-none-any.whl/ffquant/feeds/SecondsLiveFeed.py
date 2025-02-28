import pandas as pd
import backtrader as bt
import requests
import os
from datetime import datetime, timedelta, timezone
import time
import pytz
import queue
from ffquant.utils.Logger import stdout_log

__ALL__ = ['SecondsLiveFeed']

# 基本原理跟MyLiveFeed一致 请参考MyLiveFeed来理解
class SecondsLiveFeed(bt.feeds.DataBase):
    params = (
        ('url', 'http://192.168.25.127:8288/symbol/info/list'),
        ('symbol', None),
        ('timeframe', bt.TimeFrame.Seconds),
        ('compression', 5),
        ('debug', False),
        ('max_retries', 15),
        ('backpeek_size', 5),
        ('backfill_size', 0),
    )

    lines = (('turnover'),)

    def __init__(self):
        super(SecondsLiveFeed, self).__init__()
        self.live_data_list = list()
        self.hist_data_q = queue.Queue()

    def islive(self):
        return True

    def start(self):
        super().start()
        self.prepare_backfill_data()

    def prepare_backfill_data(self):
        if self.p.backfill_size > 0:
            now = datetime.now()
            end_time = now.replace(second=(now.second // self.p.compression) * self.p.compression, microsecond=0)
            start_time = end_time - timedelta(seconds=self.p.backfill_size * self.p.compression)

            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

            params = {
                'startTime': start_time_str,
                'endTime': end_time_str,
                'symbol': self.p.symbol,
                'interval': f'{self.p.compression}S'
            }

            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, backfill params: {params}, url: {self.p.url}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, backfill response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")

            results = response.get('results', [])
            results.sort(key=lambda x: x['timeClose'])

            last_time_close = None
            for result in results:
                time_close = result["timeClose"]
                if last_time_close is not None:
                    # fill missing klines
                    interval = self.p.compression
                    if time_close > last_time_close + interval * 1000:
                        missing_ts = last_time_close + interval * 1000
                        while missing_ts < time_close:
                            if self.p.debug:
                                missing_kline_local_time_str = datetime.fromtimestamp(missing_ts / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                                stdout_log(f"{self.__class__.__name__}, missing kline time: {missing_kline_local_time_str}")

                            v = self.hist_data_q.queue[-1]
                            if v is not None:
                                new_v = {
                                    'timeOpen': missing_ts - interval * 1000,
                                    'timeClose': missing_ts,
                                    'createTime': 0,    # 约定：只要是沿用的价格数据 createTime和updateTime都为0
                                    'updateTime': 0,    # 约定：只要是沿用的价格数据 createTime和updateTime都为0
                                    'symbol': v['symbol'],
                                    'open': v['close'],
                                    'high': v['close'],
                                    'low': v['close'],
                                    'close': v['close'],
                                    'vol': 0.0,
                                    'turnover': 0.0,
                                    'type': v['type']
                                }
                                self.hist_data_q.put(new_v)
                            missing_ts += interval * 1000

                self.hist_data_q.put(result)
                last_time_close = time_close

    def _load(self):
        if not self.hist_data_q.empty():
            history_item = self.hist_data_q.get()
            self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(history_item['timeClose'] / 1000.0, timezone.utc))
            self.lines.open[0] = history_item['open']
            self.lines.high[0] = history_item['high']
            self.lines.low[0] = history_item['low']
            self.lines.close[0] = history_item['close']
            self.lines.volume[0] = history_item['vol']
            self.lines.turnover[0] = history_item['turnover']
            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, hist_data_q size: {self.hist_data_q.qsize() + 1}, backfill from history, kline datetime: {self.lines.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}")

            # heartbeat info print
            self.print_heartbeat_info(history_item['createTime'])

            self.live_data_list.append(history_item)
            return True

        now = datetime.now()
        cur_kline_local_time = now.replace(second=(now.second // self.p.compression) * self.p.compression, microsecond=0).astimezone()
        start_time = cur_kline_local_time - timedelta(seconds=self.p.compression)

        if len(self.live_data_list) > 0:
            prev_live_data = self.live_data_list[len(self.live_data_list) - 1]
            if prev_live_data is not None:
                prev_kline_local_time = datetime.fromtimestamp(prev_live_data['timeClose'] / 1000.0, timezone.utc).astimezone()
                if prev_kline_local_time >= cur_kline_local_time:
                    return  # kline already exists
                else:
                    # new kline
                    # because market data API denotes Kline by open time, while backtrader denotes Kline by close time
                    start_time = datetime.fromtimestamp(prev_live_data['timeClose'] / 1000.0, timezone.utc).astimezone()

        end_time = start_time + timedelta(seconds=self.p.compression)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        retry_count = 0
        while retry_count < self.p.max_retries:
            retry_count += 1

            params = {
                'startTime': start_time_str,
                'endTime': end_time_str,
                'symbol': self.p.symbol,
                'interval': f'{self.p.compression}S'
            }

            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, fetch data params: {params}, url: {self.p.url}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, fetch data response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")

            results = response.get('results', [])
            if results is not None and len(results) > 0:
                bar = results[0]
                self.live_data_list.append(bar)

                self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(bar['timeClose'] / 1000.0, timezone.utc))
                self.lines.open[0] = bar['open']
                self.lines.high[0] = bar['high']
                self.lines.low[0] = bar['low']
                self.lines.close[0] = bar['close']
                self.lines.volume[0] = bar['vol']
                self.lines.turnover[0] = bar['turnover']

                # heartbeat info print
                self.print_heartbeat_info(bar['createTime'])
                return True
            else:
                time.sleep(0.3)

        if self.backpeek_for_result(cur_kline_local_time):
            # heartbeat info print
            self.print_heartbeat_info(self.live_data_list[len(self.live_data_list) - 1]['createTime'])
            return True
        return False

    def backpeek_for_result(self, cur_kline_local_time):
        # update backpeek window
        end_time = cur_kline_local_time

        # because market data API denotes Kline by open time, while backtrader denotes Kline by close time
        start_time = end_time - timedelta(seconds=self.p.backpeek_size * self.p.compression)

        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        params = {
            'startTime': start_time_str,
            'endTime': end_time_str,
            'symbol': self.p.symbol,
            'interval': f'{self.p.compression}S'
        }
        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, update backpeek window params: {params}, url: {self.p.url}")

        response = requests.get(self.p.url, params=params).json()
        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, update backpeek window response: {response}")

        if response.get('code') != '200':
            raise ValueError(f"API request failed: {response}")
        results = response.get('results', [])
        results.sort(key=lambda x: x['timeClose'])
        for result in results:
            for i in range(0, len(self.live_data_list)):
                if self.live_data_list[i]['timeClose'] == result['timeClose']:
                    self.live_data_list[i] = result
                    break

        if len(self.live_data_list) > 0:
            prev_live_data = self.live_data_list[len(self.live_data_list) - 1]
            if prev_live_data is not None:
                self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(cur_kline_local_time.timestamp(), timezone.utc))
                self.lines.open[0] = prev_live_data['close']
                self.lines.high[0] = prev_live_data['close']
                self.lines.low[0] = prev_live_data['close']
                self.lines.close[0] = prev_live_data['close']
                self.lines.volume[0] = 0.0

                # 延续前面K线的turnover时 如果直接设置turnover为0 会影响量的指标的计算 所以这里做了特殊处理 取前3个K线的turnover的平均值
                turnover_fix_size = min(3, len(self))
                turnover_fix_sum = 0
                for i in range(0, turnover_fix_size):
                    turnover_fix_sum += self.lines.turnover[-i - 1]
                self.lines.turnover[0] = turnover_fix_sum / turnover_fix_size

                self.live_data_list.append({
                    'timeOpen': (int(cur_kline_local_time.timestamp()) - self.p.compression) * 1000,
                    'timeClose': int(cur_kline_local_time.timestamp()) * 1000,
                    'createTime': 0,    # 约定：只要是沿用的价格数据 createTime和updateTime都为0
                    'updateTime': 0,    # 约定：只要是沿用的价格数据 createTime和updateTime都为0
                    'symbol': self.p.symbol,
                    'open': self.lines.open[0],
                    'high': self.lines.high[0],
                    'low': self.lines.low[0],
                    'close': self.lines.close[0],
                    'vol': 0.0,
                    'turnover': self.lines.turnover[0],
                    'type': prev_live_data['type']
                })

                kline_local_time_str = cur_kline_local_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')
                backpeek_time_str = datetime.fromtimestamp(prev_live_data['timeClose'] / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                stdout_log(f"[CRITICAL], {self.__class__.__name__}, kline time: {kline_local_time_str} use backpeek from {backpeek_time_str}")

                return True
        return False

    def print_heartbeat_info(self, create_time=0):
        kline_time_str = self.lines.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
        create_time_str = datetime.fromtimestamp(create_time / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
        stdout_log(f"[INFO], {self.__class__.__name__}, kline time: {kline_time_str}, create time: {create_time_str}, open: {self.lines.open[0]}, high: {self.lines.high[0]}, low: {self.lines.low[0]}, close: {self.lines.close[0]}, volume: {self.lines.volume[0]}, turnover: {self.lines.turnover[0]}")