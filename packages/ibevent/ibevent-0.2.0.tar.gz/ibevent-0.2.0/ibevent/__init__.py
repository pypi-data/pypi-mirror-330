"""Interactive Brokers Event System.

This module provides an event-driven framework for handling Interactive Brokers (IB) API events.
It allows you to easily subscribe to market data and handle events with priority-based handlers.

Key components:
- IBEventType: Enumeration of supported IB API event types.
- BaseEventRegistry: Base class for event registration and handling.
- IBEventRegistry: IB-specific event registry with automatic event binding.
- patch_ib: Function to add event system support to the IB class.

Example:
    Basic usage with real-time bar data:

    >>> from ib_async import IB
    >>> from ibevent.events import IBEventType
    >>> from ib_async.contract import Forex
    >>>
    >>> # Connect to IB
    >>> ib = IB()
    >>> ib.connect('127.0.0.1', 7497, clientId=1)
    >>>
    >>> # Create contract
    >>> usd_jpy = Forex('USDJPY')
    >>>
    >>> # Register event handler with data binding
    >>> @ib.events.register(
    ...     IBEventType.BAR_UPDATE,
    ...     bind_to=ib.reqRealTimeBars(
    ...         usd_jpy,
    ...         barSize=5,
    ...         whatToShow='MIDPOINT'
    ...     )
    ... )
    >>> def handle_bar(ib, bars, has_new_bar):
    ...     if has_new_bar:
    ...         print(bars[-1])
    >>>
    >>> # Run event loop
    >>> ib.run()

This module is designed to be extensible and easy to use, allowing developers to quickly
set up event-driven systems for trading applications using the Interactive Brokers API.

Note:
    This module requires the ib_async library and an active connection to
    Interactive Brokers TWS or IB Gateway.

See Also:
    ib_async: https://github.com/erdewit/ib_async
"""

__author__ = "shawndeng"
__email__ = "shawndeng1109@qq.com"
