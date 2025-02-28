"""Basic usage example of IBEvent.

This example demonstrates:
1. How to connect to Interactive Brokers
2. How to subscribe to real-time bar data for USD/JPY
3. How to handle bar updates using a simple event handler
"""

from ib_async import IB
from ibevent.events import IBEventType
from ib_async.contract import Forex


# Create IB connection
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Create USD/JPY contract
usd_jpy = Forex('USDJPY')

# Register bar update handler
@ib.events.register(
    IBEventType.BAR_UPDATE,
    bind_to=ib.reqRealTimeBars(
        usd_jpy,
        barSize=5,
        whatToShow='MIDPOINT',
        useRTH=True
    )
)
def handle_bar(ib, bars, has_new_bar):
    """Handle real-time bar updates for USD/JPY."""
    if has_new_bar:
        print(bars[-1])

# Run until interrupted
try:
    ib.run()
except KeyboardInterrupt:
    ib.disconnect()
    print("\nShutting down...")
