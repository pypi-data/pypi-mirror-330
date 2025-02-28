"""Multiple data streams example with IBEvent.

This example demonstrates:
1. How to subscribe to multiple data streams (EUR/USD and USD/JPY)
2. How to use priority-based event handlers
3. How to format output for different data streams
"""

from ib_async import IB
from ibevent.events import IBEventType
from ib_async.contract import Forex


# Create IB connection
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Create contracts
eur_usd = Forex('EURUSD')
usd_jpy = Forex('USDJPY')

# Register EUR/USD handler with high priority
@ib.events.register(
    IBEventType.BAR_UPDATE,
    bind_to=ib.reqRealTimeBars(
        eur_usd,
        barSize=5,
        whatToShow='MIDPOINT',
        useRTH=True
    ),
    priority=10
)
def handle_eurusd(ib, bars, has_new_bar):
    """Handle real-time bar updates for EUR/USD with high priority."""
    if has_new_bar:
        print(f"[EUR/USD] {bars[-1]}")

# Register USD/JPY handler with normal priority
@ib.events.register(
    IBEventType.BAR_UPDATE,
    bind_to=ib.reqRealTimeBars(
        usd_jpy,
        barSize=5,
        whatToShow='MIDPOINT',
        useRTH=True
    )
)
def handle_usdjpy(ib, bars, has_new_bar):
    """Handle real-time bar updates for USD/JPY with normal priority."""
    if has_new_bar:
        print(f"[USD/JPY] {bars[-1]}")

# Run until interrupted
try:
    ib.run()
except KeyboardInterrupt:
    ib.disconnect()
    print("\nShutting down...")
