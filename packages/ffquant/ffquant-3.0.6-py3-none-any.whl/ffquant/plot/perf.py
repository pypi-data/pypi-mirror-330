import backtrader as bt
import threading
from ffquant.plot.dash_graph import show_perf_graph, update_task_field
from ffquant.observers.MyBkr import MyBkr
from ffquant.observers.MyBuySell import MyBuySell
from ffquant.observers.MyDrawDown import MyDrawDown
from ffquant.observers.MyTimeReturn import MyTimeReturn
from ffquant.analyzers.OrderAnalyzer import OrderAnalyzer
import inspect
import os
from ffquant.utils.backtest_data_serialize import prepare_data_for_pickle
import time
from ffquant.utils.Logger import stdout_log

__ALL__ = ['run_and_show_performance']

# 做了两件事 1、执行cerebro.run() 2、计算性能数据 并调用Dash进行展示
# riskfree_rate 无风险利率
# use_local_dash_url为true时 打开性能界面时使用的是本地ip 如果False 使用的是域名
# backtest_data_dir 指定存储回测数据的目录
# task_id是搭配backtest_manage工程而使用的 指的是建立的回测任务的id
def run_and_show_performance(
        cerebro,
        strategy_name=None,
        riskfree_rate = 0.01,
        use_local_dash_url=False,
        backtest_data_dir=None,
        task_id=None,
        debug=False):
    if hasattr(cerebro, 'runstrats'):
        raise Exception('Cerebro already run. Cannot run again')

    # 一般是用策略的脚本名
    if strategy_name is None or strategy_name == '':
        frame = inspect.stack()[1]
        caller_file_path = frame.filename
        strategy_name = os.path.basename(caller_file_path)
        if strategy_name.endswith('.py'):
            strategy_name = strategy_name[:-3]

    # 这里是为了记录策略执行过程中的各种基础数据 方便后面的性能计算
    add_observers(cerebro, debug)

    # 这里用Analyzer而不是Observer是因为只有Analyzer才有notify_order回调方法 这里是为了记录订单的执行信息
    add_analyzers(cerebro, debug)

    is_live_trade = False
    for data in cerebro.datas:
        if data.islive():
            is_live_trade = True

    # 准备timeframe和compression信息 用于保存到pkl文件中
    timeframe = "Minutes"
    compression = 1
    if len(cerebro.datas) > 0 and cerebro.datas[0].p.timeframe == bt.TimeFrame.Seconds:
        timeframe = "Seconds"
        compression = cerebro.datas[0].p.compression

    # 回测是run完就show 所以单线程就行 但是实时的话需要一边run 一边show 所以需要多线程
    if is_live_trade:
        threading.Thread(target=lambda: cerebro.run(), daemon=True).start()
        time.sleep(15)
        backtest_data = prepare_data_for_pickle(
            strategy_name=strategy_name,
            timeframe=timeframe,
            compression=compression,
            riskfree_rate=riskfree_rate,
            use_local_dash_url=use_local_dash_url,
            debug=debug)
        show_perf_graph(backtest_data, is_live=is_live_trade, backtest_data_dir=backtest_data_dir, task_id=task_id, debug=debug)
    else:
        # 这里禁止preload模式 是为了让MyFeed和MyLiveFeed的逻辑尽可能保持一致 让他们的next方法都被调用
        cerebro.p.preload = False

        cerebro.run()

        if task_id is not None:
            for runstrat in cerebro.runstrats:
                if len(runstrat) > 0 and runstrat[0].logger is not None:
                    strat_log_path = runstrat[0].logger.log_filepath
                    stdout_log(f"strat_log_path: {strat_log_path}")
                    update_task_field(task_id, 'strat_log_path', strat_log_path)
                    break

        backtest_data = prepare_data_for_pickle(
            strategy_name=strategy_name,
            timeframe=timeframe,
            compression=compression,
            riskfree_rate=riskfree_rate,
            use_local_dash_url=use_local_dash_url,
            debug=debug)
        show_perf_graph(backtest_data, is_live=is_live_trade, backtest_data_dir=backtest_data_dir, task_id=task_id, debug=debug)

def add_observers(cerebro, debug=False):
    cerebro.addobserver(MyBkr)
    cerebro.addobserver(MyBuySell)
    cerebro.addobserver(MyDrawDown)

    if len(cerebro.datas) > 0:
        timeframe = cerebro.datas[0].p.timeframe
        compression = cerebro.datas[0].p.compression
        cerebro.addobserver(
            MyTimeReturn,
            timeframe=timeframe,
            compression=compression
        )

def add_analyzers(cerebro, debug=False):
    cerebro.addanalyzer(OrderAnalyzer)