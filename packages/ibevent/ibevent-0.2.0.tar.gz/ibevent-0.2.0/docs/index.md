# ibevent

A library for simplifying event listening for Interactive Brokers (IBKR).

## Installation

```bash
pip install ibevent
```

## Quick Start

To get started with `ibevent`, follow these steps:

1. Connect to Interactive Brokers.
2. Create a contract for the asset you want to trade.
3. Register event handlers to listen for market data updates.

### Example

```python
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
    if has_new_bar:
        print(bars[-1])

# Run until interrupted
ib.run()
```

## Features

- Event-driven framework for handling IB API events.
- Support for asynchronous event handling.
- Priority-based event handlers for multiple data streams.

## IBEventType Enumeration

The `IBEventType` enumeration defines all supported IB API event types. Each event type corresponds to a specific event in the IB API that can be subscribed to and handled.

### Attributes:
- `BAR_UPDATE`: Real-time bar data update event.
- `ERROR`: Error event from IB API.
- `CONNECTED`: Connection established event.
- `DISCONNECTED`: Connection lost event.
- (Other attributes as needed)

### Example Usage:
```python
from ibevent.events import IBEventType

# Example of using IBEventType
event_type = IBEventType.BAR_UPDATE
print(event_type)
```

