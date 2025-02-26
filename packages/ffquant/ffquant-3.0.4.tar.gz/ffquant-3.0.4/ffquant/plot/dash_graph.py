import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import ffquant.plot.dash_ports as dash_ports
import getpass
import pandas as pd
import numpy as np
import psutil
import socket
import os
from ffquant.utils.Logger import stdout_log
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import webbrowser
from ffquant.utils.backtest_data_serialize import prepare_data_for_pickle, serialize_backtest_data
import time
import signal
import threading
import ffquant.utils.global_backtest_data as global_backtest_data
import sqlite3
from pathlib import Path
from ffquant.feeds.Line import Line
from collections import deque
import backtrader as bt
from flask import jsonify
import pymysql
import traceback

__ALL__ = ['get_win_rates']

dash_last_access_time = 0
def get_self_ip():
    addrs = psutil.net_if_addrs()
    for _, interface_addresses in addrs.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET and address.address.startswith('192.168.25.'):
                return address.address

def init_dash_app(strategy_name, port, username, use_local_dash_url=False):
    app = dash.Dash(
        name=strategy_name,
        requests_pathname_prefix=f"/user/{username}/proxy/{port}/" if not use_local_dash_url else None
    )
    app.title = strategy_name
    return app

def init_stats_api(app, strategy_name, timeframe="Minutes", compression=1, riskfree_rate=0.01, use_local_dash_url=False):
    server = app.server
    @server.route("/api/stats", methods=["GET"])
    def get_stats():
        backtest_data = prepare_data_for_pickle(
            strategy_name=strategy_name,
            timeframe=timeframe,
            compression=compression,
            riskfree_rate=riskfree_rate,
            use_local_dash_url=use_local_dash_url)
        win_rates = get_win_rates(origin=None, window_size=0, backtest_data=backtest_data)

        stats = []
        for win_rate_item in win_rates.data:
            filled_order_count = 0
            for symbol in backtest_data["orders"].keys():
                symbol_orders = backtest_data["orders"][symbol]
                for order_item in symbol_orders:
                    if order_item['datetime'] <= win_rate_item["datetime"] and order_item['order_status'] == "Completed":
                        filled_order_count += 1

            rturn = 0.0
            for bvalue_item in backtest_data["broker_values"]:
                if bvalue_item["datetime"] == win_rate_item["datetime"]:
                    initial_bvalue = backtest_data["broker_values"][0]["value"]
                    rturn = (bvalue_item["value"] - initial_bvalue) / initial_bvalue
                    break

            stats.append({
                "datetime": win_rate_item["datetime"],
                "win_rate": win_rate_item["win_rate"],
                "filled_order_count": filled_order_count,
                "return": rturn
            })

        return jsonify(stats)

# 计算订单的来源 origin信息一般来自于实时策略下单时的订单参数origin
def get_order_origin_stats(orders: dict, debug=False):
    order_origin_dict = dict()
    for symbol in orders.keys():
        symbol_orders = orders[symbol]
        for order_item in symbol_orders:
            if order_item['order_status'] != "Completed":
                continue

            order_origin = order_item['origin'] if order_item['origin'] is not None else "Unknown"
            if order_origin not in order_origin_dict.keys():
                order_origin_dict[order_origin] = 1
            else:
                order_origin_dict[order_origin] += 1
    return order_origin_dict

def get_order_symbol_stats(orders: dict, debug=False):
    order_symbol_dict = dict()
    for symbol in orders.keys():
        symbol_orders = orders[symbol]
        for order_item in symbol_orders:
            if order_item['order_status'] != "Completed":
                continue

            if symbol not in order_symbol_dict.keys():
                order_symbol_dict[symbol] = 1
            else:
                order_symbol_dict[symbol] += 1
    return order_symbol_dict

# 计算所有已成交订单的盈亏性能 基本思路就是先定位到所有的平仓单 然后以平仓单为基准计算盈亏数据
def get_order_pnl_stats(orders: dict, positions: dict, timeframe="Minutes", compression=1, debug=False):
    closed_trades = []

    for symbol in orders.keys():
        symbol_orders = orders[symbol]
        for order_item in symbol_orders:
            if order_item['order_status'] != "Completed":
                continue

            order_dt_str = order_item['datetime']
            order_price = order_item['execute_price']
            order_size = order_item['execute_size']
            order_side = order_item['order_type']
            order_origin = order_item['origin'] if order_item['origin'] is not None else "Unknown"
            is_close_order = order_item['is_close_pos']
            if debug:
                stdout_log(f"symbol: {symbol}, order_dt_str: {order_dt_str}, order_price: {order_price}, order_size: {order_size}, order_side: {order_side}, order_origin: {order_origin}")

            if is_close_order:
                tdelta = timedelta(minutes=compression)
                if timeframe == "Seconds":
                    tdelta = timedelta(seconds=compression)
                pos_dt_str = (datetime.strptime(order_dt_str, '%Y-%m-%d %H:%M:%S') - tdelta).strftime('%Y-%m-%d %H:%M:%S')

                pos_price = None
                for pos_item in positions[symbol]:
                    if pos_item['datetime'] == pos_dt_str:
                        pos_price = pos_item['price']
                        break

                if pos_price is not None and pos_price != 0:
                    pnl = None
                    pnl_return = None
                    if order_side == "Buy":
                        pnl = (pos_price - order_price) * order_size
                        pnl_return = pnl / (abs(order_item['execute_size']) * pos_price)
                    else:
                        pnl = (order_price - pos_price) * order_size
                        pnl_return = pnl / (abs(order_item['execute_size']) * pos_price)

                    closed_trades.append({
                        'datetime': order_dt_str,
                        'pnl': pnl,
                        'pnl_return': pnl_return,
                        'is_win': pnl > 0
                    })

                    stdout_log(f"[PNL] symbol: {symbol}, order_dt_str: {order_dt_str}, pnl_return: {pnl_return}")
                else:
                    stdout_log(f"Faild to find position cost price for close order at {order_dt_str}, found pos_price: {pos_price}")

    win_pnls = [trade['pnl'] for trade in closed_trades if trade['is_win']]
    loss_pnls = [trade['pnl'] for trade in closed_trades if not trade['is_win']]

    avg_win_pnl = sum(win_pnls) / len(win_pnls) if len(win_pnls) > 0 else 0
    avg_loss_pnl = abs(sum(loss_pnls) / len(loss_pnls)) if len(loss_pnls) > 0 else 0

    reward_risk_ratio = avg_win_pnl / avg_loss_pnl if avg_loss_pnl > 0 else float('inf')
    win_rate = len(win_pnls) / len(closed_trades) if len(closed_trades) > 0 else 0
    avg_return = sum([trade['pnl_return'] for trade in closed_trades]) / len(closed_trades) if len(closed_trades) > 0 else 0

    return reward_risk_ratio, win_rate, avg_return

def show_perf_graph(backtest_data, is_live=False, backtest_data_dir=None, task_id=None, debug=False):
    strategy_name = backtest_data["strategy_name"]
    use_local_dash_url = backtest_data["use_local_dash_url"]

    # 对于回测的情况 要将数据写到磁盘 并且要将pkl文件的路径更新到数据库
    if backtest_data_dir is not None and not is_live and len(global_backtest_data.klines) > 0:
        pkl_file_path = serialize_backtest_data(
                                strategy_name=strategy_name,
                                timeframe=backtest_data["timeframe"],
                                compression=backtest_data["compression"],
                                riskfree_rate=backtest_data["riskfree_rate"],
                                use_local_dash_url=use_local_dash_url,
                                backtest_data_dir=backtest_data_dir,
                                debug=debug)
        if task_id is not None:
            update_task_field(task_id, "pkl_data_path", pkl_file_path)

    # 获取一个在host上可用的端口
    port = dash_ports.get_available_port()
    username = getpass.getuser()
    username = username[8:] if username.startswith('jupyter-') else username
    app = init_dash_app(strategy_name, port, username, use_local_dash_url)

    init_stats_api(
        app,
        strategy_name,
        timeframe=backtest_data["timeframe"],
        compression=backtest_data["compression"],
        riskfree_rate=backtest_data["riskfree_rate"],
        use_local_dash_url=use_local_dash_url
    )

    # 开头的性能数据表格
    init_table_callback(app, debug)
    # 其余的图形
    init_graph_callback(app, debug)

    header = f"{strategy_name}(live), created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if not is_live:
        dt_range = f"{backtest_data['broker_values'][0]['datetime']} - {backtest_data['broker_values'][-1]['datetime']}"
        header = f"{strategy_name}[{dt_range}], created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 回测其实是实时的一个特殊情况 回测只更新一次 实时更新n次
    interval = dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0,
        max_intervals=0
    )
    if is_live:
        interval = dcc.Interval(
            id='interval-component',
            interval=60*1000,
            n_intervals=0
        )

    # 下载回测数据的按钮
    html_elements = []
    html_elements.append(html.H1(header, style={'textAlign': 'center'}))
    if is_live or len(global_backtest_data.klines) > 0:
        html_elements.append(html.Button("Download Backtest Data", id="download-button", style={'position': 'absolute', 'top': '10px', 'right': '10px'}))
        html_elements.append(dcc.Download(id="download-backtest-data"))
        @app.callback(
            dash.dependencies.Output("download-backtest-data", "data"),
            [dash.dependencies.Input("download-button", "n_clicks")],
            prevent_initial_call=True
        )
        def download_backtest_data(n_clicks):
            if n_clicks:
                pkl_file_path = serialize_backtest_data(
                    strategy_name,
                    timeframe=backtest_data["timeframe"],
                    compression=backtest_data["compression"],
                    riskfree_rate=backtest_data["riskfree_rate"],
                    use_local_dash_url=use_local_dash_url)
                return dcc.send_file(pkl_file_path)

    # 回测数据表格
    html_elements.append(dash_table.DataTable(
        id='metrics-table',
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Metrics'}, 'width': '50%'},
            {'if': {'column_id': 'Result'}, 'width': '50%'}
        ],
        style_table={
            'width': '50%',
            'maxWidth': '800px',
            'margin': '0 auto'
        },
    ))
    # 图形数据
    html_elements.append(dcc.Graph(id='buysell-graph'))
    html_elements.append(interval)
    html_elements.append(dcc.Store(id='backtest-data-store', data=backtest_data))

    app.layout = html.Div(html_elements)

    # 回测的情形 需要超时杀掉服务
    if not is_live:
        TIMEOUT_SECONDS = 15

        @app.server.before_request
        def update_last_access_time():
            global dash_last_access_time
            dash_last_access_time = time.time()

        def monitor_timeout():
            global dash_last_access_time
            dash_last_access_time = time.time()
            while True:
                time.sleep(5)
                if time.time() - dash_last_access_time > TIMEOUT_SECONDS:
                    stdout_log("No activity detected. Shutting down server...")
                    update_task_field(task_id, "dash_pid", None)
                    update_task_field(task_id, "dash_port", None)
                    time.sleep(5)
                    os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=monitor_timeout, daemon=True).start()

    server_url = f"https://strategy.sdqtrade.com"
    if use_local_dash_url:
        server_url = f"http://{get_self_ip()}"

    # 如果是来自backtest_manage的回测任务 还需要更新到backtest_manage的数据库
    if task_id is not None and not is_live:
        update_task_field(task_id, "dash_pid", str(os.getpid()))
        update_task_field(task_id, "dash_port", str(port))
        update_task_field(task_id, "last_dash_started_at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if len(backtest_data["broker_values"]) > 0:
            return_rate = backtest_data["broker_values"][-1]["value"] / backtest_data["broker_values"][0]["value"] - 1
            update_task_field(task_id, "return_rate", str(return_rate))

    if get_self_ip() != "192.168.25.144":
        webbrowser.open(f"http://{get_self_ip()}:{int(port)}")

    # Dash服务被启动
    app.run_server(
        host = '0.0.0.0',
        port = int(port),
        jupyter_mode = "jupyterlab",
        jupyter_server_url = server_url,
        use_reloader=False,
        debug=True)

# 性能表格的初始化 实际是一个不断触发的定时器
def init_table_callback(app, debug=False):
    @app.callback(
        Output('metrics-table', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('backtest-data-store', 'data')]
    )
    def update_metrics_table(n, data):
        backtest_data = data
        if n > 0:
            backtest_data = prepare_data_for_pickle(
                strategy_name=backtest_data["strategy_name"],
                timeframe=backtest_data["timeframe"],
                compression=backtest_data["compression"],
                riskfree_rate=backtest_data["riskfree_rate"],
                use_local_dash_url=backtest_data["use_local_dash_url"])

        riskfree_rate = backtest_data["riskfree_rate"]
        broker_values = backtest_data["broker_values"]
        treturns = backtest_data["treturns"]
        positions = backtest_data["positions"]
        orders = backtest_data["orders"]

        length = len(broker_values)
        if length > 0:
            days_in_year = 252

            bar_interval = 60
            if backtest_data["timeframe"] == "Seconds":
                bar_interval = backtest_data["compression"]
            bars_per_day = (6.5 * 60 * 60) / bar_interval

            total_return = broker_values[-1]['value'] / broker_values[0]['value'] - 1
            annual_return = "NaN"
            annual_return = (1 + total_return / (length / bars_per_day)) ** days_in_year - 1

            std_per_bar = np.std([item['timereturn'] for item in treturns])
            std_annual = std_per_bar * np.sqrt(days_in_year * bars_per_day)

            sharpe = "NaN"
            if std_annual != 0:
                sharpe = (annual_return - riskfree_rate) / std_annual

            completed_order_num = 0
            for symbol in orders.keys():
                completed_order_num += len([item for item in orders[symbol] if item['order_status'] == "Completed"])

            limit_order_num = 0
            for symbol in orders.keys():
                limit_order_num += len([item for item in orders[symbol] if item['exec_type'] == "Limit"])

            completed_limit_order_num = 0
            for symbol in orders.keys():
                completed_limit_order_num += len([item for item in orders[symbol] if item['exec_type'] == "Limit" and item['order_status'] == "Completed"])

            long_positions = []
            short_positions = []
            for symbol in positions.keys():
                long_positions += [item['size'] for item in positions[symbol] if item['size'] > 0]
                short_positions += [item['size'] for item in positions[symbol] if item['size'] < 0]
            max_long_position = max(long_positions) if len(long_positions) > 0 else 0
            max_short_position = abs(min(short_positions)) if len(short_positions) > 0 else 0

            reward_risk_ratio, win_rate, avg_return = get_order_pnl_stats(
                orders=orders,
                positions=positions,
                timeframe=backtest_data["timeframe"],
                compression=backtest_data["compression"],
                debug=debug)
            if debug:
                stdout_log(f"reward_risk_ratio: {reward_risk_ratio}, win_rate: {win_rate}, avg_return: {avg_return}")

            order_origin_dict = get_order_origin_stats(orders, debug=debug)
            order_symbol_dict = get_order_symbol_stats(orders, debug=debug)

            metrics_data = {
                "Metrics": [
                    "总成交订单数量(买+卖)",
                    "限价单成交率",
                    "成交订单来源统计",
                    "成交订单symbol统计",
                    "区间总收益率",
                    "年化收益率",
                    "年化收益波动率",
                    "夏普比率",
                    "平均盈亏比",
                    "交易胜率",
                    "平仓单平均收益率",
                    "多头最大持仓量",
                    "空头最大持仓量"
                ],
                "Result": [
                    f"{completed_order_num}",
                    f"{(completed_limit_order_num/limit_order_num):.8%} ({completed_limit_order_num}/{limit_order_num})" if limit_order_num != 0 else "NaN",
                    f"{str(order_origin_dict)}",
                    f"{str(order_symbol_dict)}",
                    f"{total_return:.8%}",
                    f"{annual_return:.8%}" if annual_return != "NaN" else annual_return,
                    f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
                    f"{sharpe:.8f}" if sharpe != "NaN" else sharpe,
                    f"{reward_risk_ratio:.8f}" if reward_risk_ratio != float('inf') else 'NaN',
                    f"{win_rate:.8%}",
                    f"{avg_return:.8%}",
                    f"{max_long_position}",
                    f"{max_short_position}"
                ]
            }
            return pd.DataFrame(metrics_data).to_dict('records')

# 性能图形的初始化 实际是一个不断触发的定时器
def init_graph_callback(app, debug=False):
    @app.callback(
        Output('buysell-graph', 'figure'),
        Output('backtest-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('backtest-data-store', 'data')]
    )
    def update_graph(n, data):
        backtest_data = data
        if n > 0:
            backtest_data = prepare_data_for_pickle(
                strategy_name=backtest_data["strategy_name"],
                timeframe=backtest_data["timeframe"],
                compression=backtest_data["compression"],
                riskfree_rate=backtest_data["riskfree_rate"],
                use_local_dash_url=backtest_data["use_local_dash_url"])

        figure = make_subplots(
            rows=5, cols=1,
            shared_xaxes=True,  # Share X-axis between the plots
            # vertical_spacing=0.05,
            row_heights=[2, 1, 1, 1, 1], # kline graph, indicator graph, position graph, drawdown graph
            specs=[
                [{"secondary_y": True}],  # The first row enables secondary y
                [{}],  # The second row
                [{}],  # The third row
                [{}],  # The fourth row
                [{}],  # The fifth row
            ]
        )

        arrow_offset = 2
        annotations = []
        for symbol in backtest_data["klines"].keys():
            symbol_klines = backtest_data["klines"][symbol]

            # Fill K-line data
            kline_data = {
                "datetimes": [],
                "prices": []
            }
            for item in symbol_klines:
                kline_data['datetimes'].append(item["datetime"])
                kline_data['prices'].append(item["close"])

            # Add price line to the first row
            figure.add_trace(
                go.Scatter(
                    x=kline_data['datetimes'],
                    y=kline_data['prices'],
                    mode='lines',
                    name=f'{symbol}价格'
                ),
                row=1, col=1  # First row, first column
            )

            # 注意这里的颜色对应关系 很重要！！！
            # purple: market order, orange: limit order, red: lost close pos order, green: won close pos order
            # black: limit order created, gray: limit order cancelled

            symbol_orders = dict(backtest_data["orders"]).get(symbol, [])
            # Handle buy points
            for item in symbol_orders:
                if item['order_status'] == "Completed" and item['order_type'] == "Buy":
                    current_count = 0
                    for annotation in annotations:
                        if annotation['x'] == item['datetime'] and (annotation['arrowcolor'] == "purple" or annotation['arrowcolor'] == "orange" or annotation['arrowcolor'] == "red" or annotation['arrowcolor'] == "green"):
                            current_count += 1
                    close_price = None
                    for kline in backtest_data["klines"][symbol]:
                        if kline['datetime'] == item['datetime']:
                            close_price = kline['close']
                            break

                    last_pos = None
                    symbol_positions = backtest_data["positions"][symbol]
                    for i in range(0, len(symbol_positions)):
                        if symbol_positions[i]['datetime'] == item['datetime']:
                            if i > 0:
                                last_pos = symbol_positions[i - 1]
                            else:
                                last_pos = symbol_positions[i]
                            break

                    hovertext = f"{item['origin']}"
                    realized_pnl = 0
                    if item['is_close_pos']:
                        realized_pnl = (last_pos['price'] - item['execute_price']) * item['execute_size']
                        hovertext = f"{hovertext}, {symbol}平空, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 盈利: {round(realized_pnl, 2)}, 原因: {item['message']}"
                    else:
                        hovertext = f"{hovertext}, {symbol}开多, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 原因: {item['message']}"

                    arrowcolor = ""
                    if item['is_close_pos']:
                        if realized_pnl >= 0:
                            arrowcolor = "green"
                        else:
                            arrowcolor = "red"
                    elif item['exec_type'] == "Market":
                        arrowcolor = "purple"
                    else:
                        arrowcolor = "orange"
                    annotations.append(
                        dict(
                            x=item['datetime'],
                            y=close_price - 10 * current_count - arrow_offset,
                            xref="x",
                            yref="y",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowcolor=arrowcolor,
                            hovertext=hovertext,
                            ax=0,
                            ay=40
                        )
                    )

            # Handle sell points
            for item in symbol_orders:
                if item['order_status'] == "Completed" and item['order_type'] == "Sell":
                    current_count = 0
                    for annotation in annotations:
                        if annotation['x'] == item['datetime'] and (annotation['arrowcolor'] == "purple" or annotation['arrowcolor'] == "orange" or annotation['arrowcolor'] == "red" or annotation['arrowcolor'] == "green"):
                            current_count += 1
                    close_price = None
                    for kline in backtest_data["klines"][symbol]:
                        if kline['datetime'] == item['datetime']:
                            close_price = kline['close']
                            break

                    last_pos = None
                    symbol_positions = backtest_data["positions"][symbol]
                    for i in range(0, len(symbol_positions)):
                        if symbol_positions[i]['datetime'] == item['datetime']:
                            if i > 0:
                                last_pos = symbol_positions[i - 1]
                            else:
                                last_pos = symbol_positions[i]
                            break

                    hovertext = f"{item['origin']}"
                    if item['is_close_pos']:
                        realized_pnl = (item['execute_price'] - last_pos['price']) * item['execute_size']
                        hovertext = f"{hovertext}, {symbol}平多, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 盈利: {round(realized_pnl, 2)}, 原因: {item['message']}"
                    else:
                        hovertext = f"{hovertext}, {symbol}开空, 订单ID: {item['order_id']}, 价格: {item['execute_price']}, 数量: {item['execute_size']}, 原因: {item['message']}"

                    arrowcolor = ""
                    if item['is_close_pos']:
                        if realized_pnl >= 0:
                            arrowcolor = "green"
                        else:
                            arrowcolor = "red"
                    elif item['exec_type'] == "Market":
                        arrowcolor = "purple"
                    else:
                        arrowcolor = "orange"
                    annotations.append(
                        dict(
                            x=item['datetime'],
                            y=close_price + 10 * current_count + arrow_offset,
                            xref="x",
                            yref="y",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowcolor=arrowcolor,
                            hovertext=hovertext,
                            ax=0,       # X-axis shift for the arrow
                            ay=-40      # Y-axis shift for the arrow
                        )
                    )

            # Handle Limit Order Creation
            for item in symbol_orders:
                if item['order_status'] == "Submitted":
                    close_price = None
                    for kline in backtest_data["klines"][symbol]:
                        if kline['datetime'] == item['datetime']:
                            close_price = kline['close']
                            break

                    hovertext = f"{item['origin']}"
                    if item['is_close_pos']:
                        hovertext = f"{hovertext}, {symbol}平{'空' if item['order_type'] == 'Buy' else '多'}限创"
                    else:
                        hovertext = f"{hovertext}, {symbol}开{'多' if item['order_type'] == 'Buy' else '空'}限创"
                    hovertext = f"{hovertext}, 订单ID: {item['order_id']}, 价格: {item['create_price']}, 数量: {item['create_size']}, 原因: {item['message']}"

                    annotations.append(
                        dict(
                            x=item['datetime'],
                            y=item['create_price'],
                            xref="x",
                            yref="y",
                            text="●",
                            showarrow=False,
                            font=dict(size=15, color="black"),
                            align="center",
                            hovertext=hovertext,
                        )
                    )

            # Handle Limit Order Cancellation
            for item in symbol_orders:
                if item['order_status'] == "Cancelled":
                    close_price = None
                    for kline in backtest_data["klines"][symbol]:
                        if kline['datetime'] == item['datetime']:
                            close_price = kline['close']
                            break

                    hovertext = f"{item['origin']}"
                    if item['is_close_pos']:
                        hovertext = f"{hovertext}, {symbol}平{'空' if item['order_type'] == 'Buy' else '多'}限消"
                    else:
                        hovertext = f"{hovertext}, {symbol}开{'多' if item['order_type'] == 'Buy' else '空'}限消"
                    hovertext = f"{hovertext}, 订单ID: {item['order_id']}, 价格: {item['create_price']}, 数量: {item['create_size']}, 原因: {item['message']}"

                    annotations.append(
                        dict(
                            x=item['datetime'],
                            y=item['create_price'],
                            xref="x",
                            yref="y",
                            text="●",
                            showarrow=False,
                            font=dict(size=15, color="gray"),
                            align="center",
                            hovertext=hovertext,
                        )
                    )

        # Add broker values line to the last row
        bvalue_data = {
            "datetimes": [],
            "values": []
        }
        for item in backtest_data["broker_values"]:
            bvalue_data['datetimes'].append(item["datetime"])
            bvalue_data['values'].append(item["value"])
        figure.add_trace(
            go.Scatter(
                x=bvalue_data['datetimes'],
                y=bvalue_data['values'],
                mode='lines',
                name='账户价值'
            ),
            row=1, col=1,
            secondary_y=True
        )
        figure.update_xaxes(
            type="category",
            showticklabels=False,
            row=1, col=1
        )
        figure.update_yaxes(
            title_text='账户价值',
            row=1, col=1,
            secondary_y=True
        )

        # Add indicator data to the second row
        indc_data = {
            "datetimes": bvalue_data['datetimes']
        }
        keys = list(backtest_data["indcs"].keys())
        for key in keys:
            if indc_data.get(key, None) is None:
                indc_data[key] = []

            for item in backtest_data["indcs"][key]:
                indc_data[key].append(item)

            # Add indicator line to the second row
            figure.add_trace(
                go.Scatter(
                    x=indc_data['datetimes'],
                    y=indc_data[key],
                    mode='lines',
                    name=key
                ),
                row=2, col=1  # Second row, first column
            )
        # Update Y-axis title for each indicator subplot
        figure.update_xaxes(
            type="category",
            showticklabels=False,
            row=2, col=1
        )
        figure.update_yaxes(
            title_text="Indicators",
            row=2, col=1
        )

        # Add position line
        for symbol in backtest_data["positions"].keys():
            symbol_positions = backtest_data["positions"][symbol]

            position_data = {
                "datetimes": [],
                "values": []
            }
            for item in symbol_positions:
                position_data['datetimes'].append(item["datetime"])
                position_data['values'].append(item["size"])
            figure.add_trace(
                go.Scatter(
                    x=position_data['datetimes'],
                    y=position_data['values'],
                    mode='lines',
                    name=f'{symbol} Position'
                ),
                row=3, col=1  # Last row, first column
            )
            figure.update_xaxes(
                type="category",
                showticklabels=False,
                row=3, col=1
            )
            figure.update_yaxes(
                title_text=f'{symbol} Position',
                row=3, col=1
            )

        # Add drawdown line
        drawdown_data = {
            "datetimes": [],
            "drawdowns": []
        }
        for item in backtest_data["drawdowns"]:
            drawdown_data['datetimes'].append(item["datetime"])
            drawdown_data['drawdowns'].append(item["drawdown"])
        figure.add_trace(
            go.Scatter(
                x=drawdown_data['datetimes'],
                y=drawdown_data['drawdowns'],
                mode='lines',
                name='Drawdown'
            ),
            row=4, col=1  # Last row, first column
        )
        figure.update_xaxes(
            type="category",
            showticklabels=False,
            row=4, col=1
        )
        figure.update_yaxes(
            title_text='Drawdown',
            row=4, col=1
        )

        # Add win rate line to the last row
        order_origin_dict = get_order_origin_stats(backtest_data["orders"], debug=debug)
        origins = list(order_origin_dict.keys())
        for origin in origins + ["ALL"]:
            win_rates = get_win_rates(origin=origin if origin != "ALL" else None, window_size=0, backtest_data=backtest_data)

            # 有一些origin只标记了开仓的订单 这样的origin对应的win_rates全部为None 这里要过滤掉
            if origin == "ALL" or sum(1 if item["win_rate"] is not None else 0 for item in win_rates.data) > 0:
                figure.add_trace(
                    go.Scatter(
                        x=[item["datetime"] for item in win_rates.data],
                        y=[item["win_rate"] for item in win_rates.data],
                        mode='lines',
                        name=f"{origin}胜率"
                    ),
                    row=5, col=1  # Second row, first column
                )
        # Update Y-axis title for each win rate subplot
        figure.update_xaxes(
            type="category",
            showticklabels=False,
            row=5, col=1
        )
        figure.update_yaxes(
            title_text="订单胜率",
            row=5, col=1
        )

        # Add annotations to the layout
        figure.update_layout(
            title={
                'text': "<span style='color:purple; font-weight:bold;'>紫色箭头: 市价单成交</span>, "
                        "<span style='color:orange; font-weight:bold;'>黄色箭头: 限价单成交</span>, "
                        "<span style='color:red; font-weight:bold;'>红色箭头: 亏损平仓单</span>, "
                        "<span style='color:green; font-weight:bold;'>绿色箭头: 盈利平仓单</span>, "
                        "<span style='color:black; font-weight:bold;'>黑色点: 限价单创建</span>, "
                        "<span style='color:gray; font-weight:bold;'>灰色点: 限价单取消</span>",
                'x': 0.5
            },
            xaxis=dict(type='category', showticklabels=False),
            yaxis=dict(title='价格'),
            height=400 * 6,
            annotations=annotations
        )

        return figure, backtest_data

def update_task_field(task_id, field_name, new_value):
    db_host = os.getenv('BACKTEST_MANAGE_MYSQL_HOST', default='192.168.25.92')
    db_user = os.getenv('BACKTEST_MANAGE_MYSQL_USER', default='backtest_manage')
    db_password = os.getenv('BACKTEST_MANAGE_MYSQL_PASSWORD', default='sd123456')
    db_name = os.getenv('BACKTEST_MANAGE_MYSQL_DB_NAME', default='backtest_manage')
    
    try:
        # 连接 MySQL 数据库
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor  # 返回字典类型的结果
        )
        
        with conn.cursor() as cursor:
            # 构建 SQL 查询
            sql_query = f"UPDATE tasks SET {field_name} = %s WHERE id = %s"
            cursor.execute(sql_query, (new_value, task_id))
            conn.commit()  # 提交事务

    except pymysql.MySQLError as e:
        stdout_log(f"MySQL error: {e}, traceback: {traceback.format_exc()}")
    finally:
        conn.close()  # 确保连接被关闭

def get_win_rates(origin=None, window_size=15, backtest_data=None):
    """
    Get a list of dictionaries that contains the datetime and win rate for each candlestick.

    Parameters
    ----------
    origin : str, optional
        Filter the orders by origin if specified. Default is None.
    window_size : int, optional
        The size of the window for calculating the win rate. 0 means no window. Default is 15.

    Returns
    -------
    list of dict
        A list of dictionaries that contains the datetime and win rate for each candlestick.
        Use `win_rates[0]` to access the most recent win rate. `win_rates[-1]` for the last win rate. etc
    """
    klines = backtest_data["klines"]
    positions = backtest_data["positions"]
    orders = backtest_data["orders"]

    symbols = list(klines.keys())
    win_rate_line = Line(maxlen=len(klines[symbols[0]]) if len(symbols) > 0 else 0)

    order_win_status_window = deque(maxlen=window_size if window_size > 0 else None)
    for symbol in symbols:
        symbol_klines = klines[symbol]
        for i in range(len(symbol_klines)):
            kline = symbol_klines[i]
            dt_str = kline['datetime']

            order_win_status_window.append(None)
            win_rate_line.append({"datetime": dt_str, "win_rate": None})
            # 判断有没有Completed的订单 如果有 那就找到对应的开仓成本价

            symbol_orders = dict(orders).get(symbol, [])
            for o in symbol_orders:
                if o['datetime'] < dt_str:
                    continue

                if o['datetime'] > dt_str:
                    break

                if origin is not None:
                    order_origin = o['origin']
                    if order_origin != origin:
                        continue

                if o['order_status'] == "Completed":
                    is_close_pos = o['is_close_pos']
                    if is_close_pos is not None and is_close_pos == True:
                        # 查找开仓成本价
                        last_pos = None
                        cur_pos = None
                        symbol_positions = positions[symbol]
                        for pos in symbol_positions:
                            cur_pos = pos

                            if cur_pos['datetime'] < dt_str:
                                last_pos = cur_pos
                                continue

                            if cur_pos['datetime'] > dt_str:
                                last_pos = cur_pos
                                break

                            if last_pos['price'] != 0:
                                if (o['execute_price'] - last_pos['price']) * last_pos['size'] > 0:
                                    order_win_status_window[len(order_win_status_window) - 1] = True
                                else:
                                    order_win_status_window[len(order_win_status_window) - 1] = False
                    break

            order_cnt = sum([1 if item is not None else 0 for item in order_win_status_window])
            win_order_cnt = sum([1 if item else 0 for item in order_win_status_window])
            if order_cnt > 0:
                win_rate_line[0] = {"datetime": dt_str, "win_rate": float(win_order_cnt) / order_cnt}

    return win_rate_line