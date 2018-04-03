import pandas as pd
from zipline_poloniex import create_bundle, Pairs, register

start_session = pd.Timestamp('2017-03-11', tz='utc')
end_session = pd.Timestamp('2018-03-21', tz='utc')
assets = [Pairs.usdt_eth, Pairs.usdt_btc, Pairs.usdt_ltc, Pairs.usdt_rep]

register(
    'poloniex',
    create_bundle(
        assets,
        start_session,
        end_session,
    ),
    calendar_name='POLONIEX',
    minutes_per_day=24*60,
    start_session=start_session,
    end_session=end_session
)

