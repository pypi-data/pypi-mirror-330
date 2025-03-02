# -*- coding: UTF-8 -*-

import os
import signal
import sys
import time

import base1x
import pandas
import pandas as pd
from base1x import market
from xtquant import xtdata

from trader1x import utils, context, thinktrader, config
from trader1x.log4py import logger

# 应用名称
application = 'quant1x-trader'


def handler_exit(signum, frame):
    """
    退出前操作
    :param signum:
    :param frame:
    :return:
    """
    global trader
    logger.info('{} shutdown...', application)
    trader.close()
    logger.info('{} shutdown...OK', application)
    sys.exit(0)


def auto_trader() -> int:
    """
    自动化交易入口
    """
    global trader
    signal.signal(signal.SIGINT, handler_exit)
    signal.signal(signal.SIGTERM, handler_exit)
    logger.info('{} start...', application)
    # 0. 加载配置文件
    logger.info('加载配置...')
    conf = config.load()
    logger.info('配置信息: {}', conf)
    logger.info('加载配置...OK')
    trader = thinktrader.ThinkTrader(conf)
    # 1. 连接miniQMT
    connect_result = trader.connect()
    if connect_result == 0:
        logger.info('connect miniQmt: success')
    else:
        logger.error('connect miniQmt: failed')
        return utils.errno_miniqmt_connect_failed
    logger.info('{} start...OK', application)
    # 2. 设置账号
    ctx = context.QmtContext(conf)
    trader.set_account(ctx.account_id)
    # # 2.1 测试 - 持仓列表
    # trader.profit_and_loss(ctx)
    # # 2.2 测试 - 刷新订单
    # trader.refresh_order()
    # # 2.3 测试 - 复盘
    # marker_review(ctx, trader)
    # # 2.4 测试 - 统计
    # stat(ctx, trader)
    # exit(0)
    # 3. 盘中交易流程
    # # 3.1 测试单一可用金额
    # stock_total = 6
    # single_funds_available = trader.available_amount(stock_total)
    # logger.info('single_funds_available= {}', single_funds_available)
    # # 3.2 测试手续费
    # single_funds_available = 10000.00
    # buy_price = 10.00
    # buy_num = trader.calculate_stock_volumes(single_funds_available, buy_price)
    # logger.info('single_funds_available={}, price={}, volume={}', single_funds_available, buy_price, buy_num)
    # exit(0)
    # 3.3 检测新增标的
    logger.info('订单路径: {}', ctx.order_path)
    date_updated = False
    while True:
        time.sleep(1)
        logger.info("检测[交易日]...")
        # 3.3.1 检测当前日期是否最后一个交易日
        (today, trade_date) = trader.current_date()
        if today != trade_date:
            logger.warning('today={}, trade_date={}, 非交易日', today, trade_date)
            date_updated = False
            continue
        elif not date_updated:
            # 如果状态还没调整
            logger.warning('today={}, trade_date={}, 当前日期为交易日', today, trade_date)
            ctx.switch_date()
            date_updated = True
            continue
        # 3.3.2 早盘策略
        head_trading(ctx, trader)
        # 3.3.3 盘中策略
        tick_trading(ctx, trader, 81)
        tick_trading(ctx, trader, 82)
        # 3.3.4 尾盘策略
        tail_trading(ctx, trader)
        # 3.3.5 盘中卖出
        positions_sell(ctx, trader)
        # 3.3.6 盘后复盘
        marker_review(ctx, trader)
        # break

    # 4. 关闭
    logger.info('{} stop...', application)
    trader.close()
    logger.info('{} stop...OK', application)
    logger.info('{} shutdown', application)
    return 0


def head_trading(ctx: context.QmtContext, trader: thinktrader.ThinkTrader):
    """
    早盘交易
    :param ctx: 上下文
    :param trader: 交易实例
    :return:
    """
    order_remark = 'head'
    logger.info("检测[交易时段 - head]...")
    # 1. 是否早盘交易时段
    if not trader.head_order_can_trade():
        logger.warning("[交易时段 - head]...skip")
        return
    # 2. 早盘订单是否自动交易
    if not ctx.head_order_is_auto():
        logger.info('早盘交易, 禁止自动交易...')
        return
    # 3. 早盘订单是否完成交易
    if ctx.head_order_buy_is_finished():
        logger.warning("[交易时段 - head]...订单已完成")
        return
    # 4. 买入订单未就绪, 退出
    if not ctx.head_order_is_ready():
        logger.warning("[交易时段 - head]...订单未就绪")
        return
    # 5. 资金是否满足交易条件
    if not trader.asset_can_trade():
        logger.warning("[交易时段 - head]...触及最低保留金额, 暂停交易")
        return
    # 6. 获取早盘订单的dataframe
    df = ctx.load_head_order()
    stock_total = len(df)
    if stock_total == 0:
        return
    logger.info('订单数量: {}', stock_total)
    # 7. 资金是否满足交易条件
    # total_asset, cash = trader.account_available()
    # 8. 遍历订单, 数据文件只需要code和open两个字段
    for idx, stock in df.iterrows():
        # 数据日期
        order_date = stock['date']
        # 证券代码
        code = stock['code']
        security_name = stock['name']
        # 检查买入成功标识
        if ctx.check_buy_order_done_status(code):
            logger.info("stock {}: buy done", code)
            continue
        # 评估可以委托买入的价格和数量
        # 查询计算单一标的可用资金
        single_funds_available = trader.available_amount(stock_total)
        if single_funds_available <= 0:
            logger.warning('!!!已满仓!!!')
            continue
        # 获取快照
        security_code = market.fix_security_code(code)
        snapshot = trader.get_snapshot(security_code)
        # 计算溢价
        last_price = snapshot['lastPrice']
        buy_price = trader.available_price(last_price)
        # 计算可买数量
        buy_num = trader.calculate_stock_volumes(single_funds_available, buy_price)
        if buy_num < 100:
            logger.warning('单一股价过高, 分仓购买力不足1手')
            stock_total = stock_total - 1
            # 设置执行下单完成状态
            ctx.push_buy_order_done_status(code)
            continue
        # 买入操作
        # strategy_code = stock['strategy_code']
        # strategy_name = stock['strategy_name']
        strategy_code = '0'
        strategy_name = '0号策略'
        logger.warning('{}: 证券名称={}, 证券代码={}, date={}, strategy_code={}, price={}, vol={}', strategy_code,
                       security_name, security_code, order_date, strategy_code, buy_price, buy_num)
        order_id = trader.buy(security_code, buy_price, buy_num, f'S{strategy_code}', order_remark)
        logger.warning('order id: {}', order_id)
        # 设置执行下单完成状态
        ctx.push_buy_order_done_status(code)
    # 设置已完成标志文件
    ctx.push_head_order_buy_completed()
    return


def tail_trading(ctx: context.QmtContext, trader: thinktrader.ThinkTrader):
    """
    尾盘交易
    :param ctx:
    :param trader:
    :return:
    """
    logger.info("检测[交易时段 - tail]...")
    return


def tick_trading(ctx: context.QmtContext, trader: thinktrader.ThinkTrader, strategy_no: int = 81):
    """
    盘中交易
    :param ctx: 上下文
    :param trader: 交易实例
    :param strategy_no: 策略编号
    :return:
    """
    order_remark = 'tick'
    logger.info("检测[交易时段 - tick]...")
    if not trader.tick_order_can_trade():
        logger.info('非盘中交易时段, waiting...')
        return
    if not ctx.tick_order_is_auto():
        logger.info('盘中订单, 禁止自动交易...')
        return
    if trader.total_strategy_orders(strategy_no) >= 6:
        logger.info('检测[交易时段 - tick]...已达到操作标的数量')
        return
    logger.warning('检测新增标的...')
    csv_stock_pool = ctx.order_path + '/stock_pool.csv'
    stat_stock_pool = ctx.order_path + '/stock_pool.stat'
    # 如果股票池状态文件不存在, 则创建
    if not os.path.isfile(stat_stock_pool):
        base1x.touch(stat_stock_pool)
    # 获取股票池csv文件的修改时间
    update_time = os.path.getmtime(csv_stock_pool)
    last_modified = os.path.getmtime(stat_stock_pool)
    if update_time < last_modified:
        logger.warning('检测新增标的...无变化')
        return
    else:
        # 同步股票池数据文件的修改时间给股票池状态文件
        os.utime(stat_stock_pool, (update_time, update_time))
    mtime = time.localtime(update_time)
    timestamp = time.strftime(utils.kFormatTimestamp, mtime)
    logger.info('{} last modify: {}', csv_stock_pool, timestamp)
    # 3.3.3 检查当日所有的订单
    df = pd.read_csv(csv_stock_pool)
    if len(df) == 0:
        return
    # 过滤条件: 当日订单, 策略编号为81且订单状态为1
    (today, trade_date) = trader.current_date()
    condition = (df['date'] == today) & (df['strategy_code'] == strategy_no) & (df['order_status'] == 1)
    tick_orders = df[condition]
    if len(tick_orders) == 0:
        return
    stock_total = len(tick_orders)
    logger.warning('盘中水位观测: {}', stock_total)
    # 遍历订单
    for idx, stock in tick_orders.iterrows():
        # print(stock)
        order_date = stock['date']
        code = stock['code']
        strategy_code = stock['strategy_code']
        strategy_name = stock['strategy_name']
        security_name = stock['name']
        security_code = market.fix_security_code(code)
        # 检查买入状态
        if ctx.check_buy_order_done_status(code):
            # 已经买入的票, 跳过
            continue
        # 评估可以委托买入的价格和数量
        # 查询计算单一标的可用资金
        single_funds_available = trader.available_amount_for_tick(stock_total)
        if single_funds_available <= 0.00:
            logger.warning('!!!已满仓!!!')
            # 设置执行下单完成状态
            ctx.push_buy_order_done_status(code)
            continue
        # 获取快照
        snapshot = trader.get_snapshot(security_code)
        # 计算溢价
        last_price = snapshot['lastPrice']
        buy_price = trader.available_price(last_price)
        # 计算可买数量
        buy_num = trader.calculate_stock_volumes(single_funds_available, buy_price)
        if buy_num < 100:
            logger.warning('单一股价过高, 分仓购买力不足1手')
            stock_total = stock_total - 1
            # 设置执行下单完成状态
            ctx.push_buy_order_done_status(code)
            continue
        logger.warning('{}: 证券名称={}, 证券代码={}, date={}, strategy_code={}, price={}, vol={}', strategy_code,
                       security_name, security_code, order_date, strategy_code, buy_price, buy_num)
        # 委托买入
        order_id = trader.buy(security_code, buy_price, buy_num, f'S{strategy_code}', order_remark)
        logger.warning('order id: {}', order_id)
        # 设置执行下单完成状态
        ctx.push_buy_order_done_status(code)


def positions_sell(ctx: context.QmtContext, trader: thinktrader.ThinkTrader):
    """
    持仓卖出
    :param ctx:
    :param trader:
    :return:
    """
    # 1. 是否自动卖出
    if not ctx.sell_is_auto():
        logger.warning('sell: 非自动卖出, 需要人工干预')
        return
    # 2. 是否卖出时段
    if not ctx.sell_is_ready():
        logger.warning('sell: 非持仓卖出时段')
        return
    # 3. 检查是否已完成卖出操作
    if ctx.positions_sell_finished():
        logger.warning('sell: 持仓卖出操作已完成')
        return
    # 4. 查询当日所有的持仓
    positions = trader.query_positions()
    logger.info("sell: 当前持仓: {}", len(positions))
    for position in positions:
        if position.can_use_volume < 100:
            continue
        # print(repr(dt))
        security_code = position.stock_code
        snapshot = trader.get_snapshot(security_code)
        # 获取股票涨停价
        stock_detail = xtdata.get_instrument_detail(security_code)
        up_stop_price = stock_detail['UpStopPrice']
        last_price = snapshot['lastPrice']
        op_flag = 'Unknown'
        if last_price < up_stop_price:
            try:
                # 卖出操作
                order_id = trader.sell(position, 't89k_sell', '测试卖出')
            except Exception:
                order_id = -1
            print('order_id:', order_id)
            op_flag = 'ASKING'
        else:
            op_flag = 'WAITING - LimitUp'
        # 控制台输出持仓记录
        logger.warning("ask: code=%s, last_price=%f, up_stop_price=%f", security_code, last_price, up_stop_price)
        logger.warning(
            "sell: %s stock %s holding: %d can_ask: %d, open_price:%f, market_value: %f" % (op_flag, security_code,
                                                                                            position.volume,
                                                                                            position.can_use_volume,
                                                                                            position.open_price,
                                                                                            position.market_value))
    # 输出卖出完成操作标识
    ctx.push_positions_sell_completed()


def marker_review(ctx: context.QmtContext, trader: thinktrader.ThinkTrader):
    """
    盘后复盘
    :return:
    """
    if not ctx.can_review():
        return
    if ctx.orders_has_refreshed():
        logger.warning('复盘操作, 已完成')
        return
    # 盈亏统计
    trader.profit_and_loss(ctx)
    # 更新订单
    order_filename = ctx.qmt_order_filename
    df = trader.refresh_order()
    if df is not None:
        # old = pd.read_csv(order_filename, encoding='utf-8', index_col=0)
        old = pd.read_csv(order_filename, encoding='utf-8')
        if len(old) > 0:
            _, trade_date = trader.current_date()
            old.drop(old[old.order_time >= trade_date].index, inplace=True)
            old = trader.align_fields_for_order(old)
            df = pandas.concat([old, df])
        df.sort_values(by='order_id', inplace=True)
        df.to_csv(order_filename, encoding='utf-8', index=False)
        ctx.push_orders_refreshed()


def stat(ctx: context.QmtContext, trader: thinktrader.ThinkTrader):
    """
    统计
    :param ctx:
    :param trader:
    :return:
    """
    csv_stock_pool = ctx.order_path + '/stock_pool.csv'
    df = pd.read_csv(csv_stock_pool)
    if len(df) == 0:
        return
    # 过滤条件: 当日订单, 策略编号为81且订单状态为1
    (today, trade_date) = trader.current_date()
    # condition = (df['date'] == today) & (df['strategy_code'] == 81)
    condition = (df['date'] == trade_date) & (df['strategy_code'] == 81)
    tick_orders = df[condition].copy()
    tick_orders['sell'] = 0.00
    if len(tick_orders) == 0:
        return
    stock_total = len(tick_orders)
    print(stock_total)
    for idx, stock in tick_orders.iterrows():
        code = stock['code']
        security_code = market.fix_security_code(code)
        snapshot = trader.get_snapshot(security_code)
        last_price = snapshot['lastPrice']
        # stock['sell'] = last_price
        tick_orders.at[idx, 'sell'] = float(last_price)
    tick_orders['x'] = 100 * (tick_orders['sell'] - tick_orders['buy']) / tick_orders['buy']
    df = tick_orders[['code', 'name', 'buy', 'sell', 'x', 'speed', 'active']]
    print(df)
    df1 = df[df['x'] > 0]
    print(df1)
    print(df['x'].sum() / len(df))


if __name__ == '__main__':
    sys.exit(auto_trader())
