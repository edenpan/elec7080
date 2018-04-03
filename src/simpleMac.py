import logging

from zipline.api import order, record, symbol,order_target
from zipline_poloniex.utils import setup_logging
import matplotlib.pyplot as plt

# setup logging and all
setup_logging(logging.INFO)
_logger = logging.getLogger(__name__)
_logger.info("Dummy agent loaded")

def initialize(context):
    _logger.info("Initializing agent...")
    # There seems no "nice" way to set the emission rate to minute
    #context.sim_params._emission_rate = 'day'
    context.asset = symbol('ETH')
    context.i = 0;


def handle_data(context, data):
    _logger.debug("Handling data...")
    context.i += 1
    if context.i < 30*24*60 or (context.i- 8*60) % (24*60) != 0:
        return
        
    short_mavg = data.history(symbol('ETH'), 'price', bar_count=10*24*60, frequency='1m').mean()
    long_mavg = data.history(symbol('ETH'), 'price', bar_count=30*24*60, frequency='1m').mean()

	# Trading logic
    if short_mavg > long_mavg:
        order_target(context.asset, 10)

    elif short_mavg < long_mavg:
        order_target(context.asset, -10)    	
    record(ETH=data.current(context.asset, 'price'),
       short_mavg=short_mavg,
       long_mavg=long_mavg)        

def analyze(context = None, results = None):
    import matplotlib.pyplot as plt
    import logbook
    logbook.StderrHandler().push_application()
    log = logbook.Logger('Algorithm')

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')

    ax2 = fig.add_subplot(212)
    ax2.set_ylabel('Price (USD)')
    if ('ETH' in results and 'short_mavg' in results and
            'long_mavg' in results):
        results['ETH'].plot(ax=ax2)
        results[['short_mavg', 'long_mavg']].plot(ax=ax2)

        trans = results.ix[[t != [] for t in results.transactions]]
        buys = trans.ix[[t[0]['amount'] > 0 for t in
                         trans.transactions]]
        sells = trans.ix[
            [t[0]['amount'] < 0 for t in trans.transactions]]
        ax2.plot(buys.index, results.short_mavg.ix[buys.index],
                 '^', markersize=10, color='m')
        ax2.plot(sells.index, results.short_mavg.ix[sells.index],
                 'v', markersize=10, color='k')
        plt.legend(loc=0)
    else:
        msg = 'ETH, short_mavg & long_mavg data not captured using record().'
        ax2.annotate(msg, xy=(0.1, 0.5))
        log.info(msg)

    plt.show()


