"""Async handler example with IBEvent.

This example demonstrates:
1. How to use async event handlers
2. How to handle real-time bar data asynchronously
3. Basic usage of asyncio with IBEvent
"""

from ib_async import IB
from ibevent.events import IBEventType
from ib_async.contract import Forex
import asyncio


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
async def handle_bar(ib, bars, has_new_bar):
    """Handle real-time bar updates asynchronously.
    
    This handler demonstrates how to use async/await with IBEvent.
    You can add your own async processing logic here.
    """
    if has_new_bar:
        # Simulate some async processing
        await asyncio.sleep(0.1)
        print(bars[-1])

# Run until interrupted
try:
    ib.run()
except KeyboardInterrupt:
    ib.disconnect()
    print("\nShutting down...")
