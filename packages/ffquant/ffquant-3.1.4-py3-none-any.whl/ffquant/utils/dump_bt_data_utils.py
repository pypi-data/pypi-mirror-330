import os
import pickle
import backtrader as bt
from ffquant.utils.Logger import stdout_log
from pathlib import Path
import ffquant.utils.global_backtest_data as global_backtest_data

def wash_order_info(order_info, pickle_dict):
    order_list = list()
    for item in order_info:
        tmp_order_dict = dict()
        tmp_order_dict['datetime'] = item['datetime']
        tmp_order_dict['order_id'] = item['data'].ref
        tmp_order_dict['exec_type'] = "Market" if item['data'].exectype == bt.Order.Market else "Limit"
        tmp_order_dict['order_type'] = "Buy" if item['data'].ordtype == bt.Order.Buy else "Sell"
        order_status = ""
        if item['data'].status == bt.Order.Submitted:
            order_status = "Submitted"
        elif item['data'].status == bt.Order.Completed:
            order_status = "Completed"
        elif item['data'].status == bt.Order.Cancelled:
            order_status = "Cancelled"
        tmp_order_dict['order_status'] = order_status
        tmp_order_dict['execute_price'] = item['data'].executed.price
        tmp_order_dict['execute_size'] = abs(item['data'].executed.size)
        tmp_order_dict['create_price'] = item['data'].created.price
        tmp_order_dict['create_size'] = abs(item['data'].created.size)
        tmp_order_dict['position_after'] = item['position_after']
        tmp_order_dict['origin'] = item['data'].info["origin"] if item['data'].info["origin"] is not None and not isinstance(item['data'].info["origin"], dict) else "Unknown"
        tmp_order_dict['message'] = item['data'].info["message"] if item['data'].info["message"] is not None and not isinstance(item['data'].info["message"], dict) else None
        tmp_order_dict['is_close_pos'] = item['data'].info["is_close_pos"] if item['data'].info["is_close_pos"] is not None and not isinstance(item['data'].info["is_close_pos"], dict) else False
        order_list.append(tmp_order_dict)
    
    pickle_dict['order_info'] = order_list
    return pickle_dict

# 实时和回测都把数据序列化为pickle
def prepare_data_for_pickle(strategy_name, riskfree_rate=0.01, use_local_dash_url=False, version="1.0.0", debug=False):
    pickle_dict = {}
    pickle_dict["version"] = version
    pickle_dict["strategy_name"] = strategy_name
    pickle_dict["use_local_dash_url"] = use_local_dash_url
    pickle_dict["riskfree_rate"] = riskfree_rate
    pickle_dict['treturn'] = global_backtest_data.treturns
    pickle_dict['portfolio'] = global_backtest_data.broker_values
    pickle_dict['buysell'] = global_backtest_data.buysells
    pickle_dict['drawdown'] = global_backtest_data.drawdowns
    pickle_dict['kline'] = global_backtest_data.klines
    pickle_dict['position'] = global_backtest_data.positions
    pickle_dict['ind_data'] = global_backtest_data.indcs

    # repack order info because it is not serializable
    pickle_dict = wash_order_info(global_backtest_data.orders, pickle_dict)

    return pickle_dict

def format_datetime(datetime_str):
    return datetime_str.replace(" ", "_").replace(":", "-")

def serialize_backtest_data(strategy_name, riskfree_rate=0.01, use_local_dash_url=False, version="1.0.0", backtest_data_dir=None, debug=False):
    pickle_dict = prepare_data_for_pickle(strategy_name, riskfree_rate, use_local_dash_url, version)

    pkl_data_dir = f"{Path.home()}/backtest_data/"
    if backtest_data_dir is not None:
        pkl_data_dir = backtest_data_dir

    if not os.path.exists(pkl_data_dir):
        os.makedirs(pkl_data_dir)

    pkl_file_name = f"{strategy_name}_{format_datetime(global_backtest_data.klines[0]['datetime'])}_to_{format_datetime(global_backtest_data.klines[-1]['datetime'])}.pkl"
    pkl_file_path = os.path.join(pkl_data_dir, pkl_file_name)

    if os.path.exists(pkl_file_path):
        os.remove(pkl_file_path)

    with open(pkl_file_path, 'wb') as pkl_file:
        pickle.dump(pickle_dict, pkl_file)

    return pkl_file_path
