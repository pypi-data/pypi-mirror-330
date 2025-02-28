"""Interactive Brokers Event System.

This module provides an event-driven framework for handling Interactive Brokers (IB) API events.
It allows you to easily subscribe to market data and handle events with priority-based handlers.

Example:
    Basic usage with real-time bar data:

    >>> from ib_async import IB
    >>> from ibevent.events import IBEventType
    >>> from ib_async.contract import Forex
    >>> # Connect to IB
    >>> ib = IB()
    >>> ib.connect('127.0.0.1', 7497, clientId=1)
    >>> # Create contract    >>>
    >>> usd_jpy = Forex('USDJPY')
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
    >>> # Run event loop
    >>> ib.run()
"""

import asyncio
from enum import Enum
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

from loguru import logger


class IBEventType(Enum):
    """Interactive Brokers event type enumeration.

    This enum defines all supported IB API event types. Each event type corresponds
    to a specific event in the IB API that can be subscribed to and handled.

    Attributes:
        BAR_UPDATE: Real-time bar data update event.
        ERROR: Error event from IB API.
        CONNECTED: Connection established event.
        DISCONNECTED: Connection lost event.
    """

    # Common events
    CONNECTED = "connectedEvent"  # 连接成功事件
    DISCONNECTED = "disconnectedEvent"  # 连接断开事件
    ERROR = "errorEvent"  # 错误事件
    TIMEOUT = "timeoutEvent"  # 超时事件
    UPDATE = "updateEvent"  # 数据更新事件

    # Market data events
    PENDING_TICKERS = "pendingTickersEvent"  # 待处理的Tick数据事件
    BAR_UPDATE = "barUpdateEvent"  # K线数据更新事件

    # Order management events
    NEW_ORDER = "newOrderEvent"  # 新订单事件
    ORDER_MODIFY = "orderModifyEvent"  # 订单修改事件
    CANCEL_ORDER = "cancelOrderEvent"  # 订单取消事件
    OPEN_ORDER = "openOrderEvent"  # 开放订单事件
    ORDER_STATUS = "orderStatusEvent"  # 订单状态更新事件
    EXEC_DETAILS = "execDetailsEvent"  # 订单执行详情事件
    COMMISSION_REPORT = "commissionReportEvent"  # 佣金报告事件

    # Portfolio and position events
    UPDATE_PORTFOLIO = "updatePortfolioEvent"  # 投资组合更新事件
    POSITION = "positionEvent"  # 持仓变动事件
    ACCOUNT_VALUE = "accountValueEvent"  # 账户价值更新事件
    ACCOUNT_SUMMARY = "accountSummaryEvent"  # 账户摘要更新事件
    PNL = "pnlEvent"  # 总体盈亏更新事件
    PNL_SINGLE = "pnlSingleEvent"  # 单个持仓盈亏更新事件

    # Market scanning and news events
    SCANNER_DATA = "scannerDataEvent"  # 市场扫描数据事件
    TICK_NEWS = "tickNewsEvent"  # 新闻Tick事件
    NEWS_BULLETIN = "newsBulletinEvent"  # 新闻公告事件

    # WSH（Wall Street Horizon）events
    WSH_META = "wshMetaEvent"  # WSH元数据事件
    WSH = "wshEvent"  # WSH数据事件（如财报日期、分红日期等）


class BaseEventRegistry:
    """event registration base class."""

    def __init__(self):
        """Initialize the event registry."""
        self._handlers: Dict[Any, List[Tuple[int, Callable]]] = {}

    def register(self, event_type: IBEventType, *, bind_to: Any = None, priority: int = 0):
        """Register event handler.

        This decorator registers a function as a handler for a specific event type.
        Handlers can be either synchronous or asynchronous functions.

        Args:
            event_type: The type of event to handle.
            bind_to: Optional data source to bind to (e.g., ib.reqRealTimeBars(...)).
            priority: Handler priority. Higher numbers execute first. Defaults to 0.

        Returns:
            A decorator function that registers the handler.

        Example:
            >>> @registry.register(IBEventType.BAR_UPDATE, priority=10)
            >>> def handle_bar(ib, bars, has_new_bar):
            ...     if has_new_bar:
            ...         print(bars[-1])
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append((priority, wrapper))
            self._handlers[event_type].sort(key=lambda x: x[0], reverse=True)

            return wrapper

        return decorator


class IBEventRegistry(BaseEventRegistry):
    """A registry for Interactive Brokers (IB) API events.

    This class extends BaseEventRegistry to provide specific functionality
    for handling IB API events. It sets up handlers for various IB API events
    and manages their execution.

    Attributes:
        ib: An instance of the IB API client.

    Example:
        >>> from ib_async import IB
        >>> ib = IB()
        >>> registry = IBEventRegistry(ib)
        >>> @registry.register(IBEventType.BAR_UPDATE, priority=10)
        ... def handle_bar(ib, bars, has_new_bar):
        ...     if has_new_bar:
        ...         print(bars[-1])
        >>> ib.connect('127.0.0.1', 7497, clientId=1)
        >>> ib.run()
    """

    def __init__(self, ib):
        """Initialize the IB event registry.

        Args:
            ib: The IB API instance to register events with.
        """
        super().__init__()
        self.ib = ib
        self._setup_ib_handlers()

    def _setup_ib_handlers(self):
        """Set up handlers for IB API events.

        This method is called during initialization to set up the connection
        between IB API events and our event handling system.
        """
        for event_type in IBEventType:
            if hasattr(self.ib, event_type.value):
                event = getattr(self.ib, event_type.value)
                event += lambda *args, et=event_type: self._handle_event(et, *args)

    def _handle_event(self, event_type: IBEventType, *args):
        """Handle an IB API event.

        This method is called when an IB API event occurs. It dispatches the event
        to all registered handlers in priority order.

        Args:
            event_type: The type of event that occurred.
            *args: Arguments from the IB API event.
        """
        if event_type in self._handlers:
            for _, handler in self._handlers[event_type]:
                try:
                    result = handler(self.ib, *args)
                    if asyncio.iscoroutine(result):
                        asyncio.create_task(result)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")


def patch_ib():
    """Patch the IB class to add event system support.

    This function adds an 'events' property to the IB class, which provides
    access to the event system. The event registry is created lazily when first accessed.
    """
    from ib_async import IB

    def _get_events(self):
        if not hasattr(self, "_events"):
            self._events = IBEventRegistry(self)
        return self._events

    IB.events = property(_get_events)


# Apply the IB patch
patch_ib()
