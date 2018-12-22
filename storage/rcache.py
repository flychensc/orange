"""
redis cache
"""

import redis


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

HASH_TIMESTAMP = "stock_database_info"

KEY_TS_BASIC_INFO = "basic_info"
KEY_TS_HISTORY = "history"
KEY_TS_TICK_DATA = "tick_data"
KEY_TS_REPORT_DATA = "report_data"
KEY_TS_PROFIT_DATA = "profit_data"
KEY_TS_OPERATION_DATA = "operation_data"
KEY_TS_GROWTH_DATA = "growth_data"
KEY_TS_DEBTPAYING_DATA = "debtpaying_data"
KEY_TS_CASHFLOW_DATA = "cashflow_data"


def set_timestamp(key, date):
    if key not in [
        KEY_TS_BASIC_INFO,
        KEY_TS_HISTORY,
        KEY_TS_TICK_DATA,

        KEY_TS_REPORT_DATA,
        KEY_TS_PROFIT_DATA,
        KEY_TS_OPERATION_DATA,
        KEY_TS_GROWTH_DATA,
        KEY_TS_DEBTPAYING_DATA,
        KEY_TS_CASHFLOW_DATA,
    ]:
        return
    r.hset(HASH_TIMESTAMP, "k1", "v1")


def get_timestamp(key):
    return r.hget(HASH_TIMESTAMP, key)
