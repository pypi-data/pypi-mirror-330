# -*- coding: UTF-8 -*-

import sys

from trader1x import utils, config, thinktrader, context, auto
from trader1x.log4py import logger

application = 'quant1x-qmt'


def main() -> int:
    """
    定时任务调用
    :return:
    """
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
    # 3. 交易流程
    auto.head_trading(ctx, trader)
    auto.positions_sell(ctx, trader)
    # 4. 关闭
    logger.info('{} stop...', application)
    trader.close()
    logger.info('{} stop...OK', application)
    logger.info('{} shutdown', application)
    return utils.errno_success


if __name__ == '__main__':
    sys.exit(main())
