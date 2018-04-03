from zipline.api import order, record, symbol

def initialize(context):
    context.assets = symbol('ETH')
    
def before_trading_start(context, data):
    # Create a window
    window_1 = data.history(assets = context.assets,fields = 'open', bar_count = 10, frequency = '1d')
    print(window_1)
