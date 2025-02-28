# ibevent

一个用于简化Interactive Brokers (IBKR) 事件监听的库。

## 安装

```bash
pip install ibevent
```

## 快速开始

要开始使用 `ibevent`，请按照以下步骤操作：

1. 连接到Interactive Brokers。
2. 创建您想要交易的资产的合约。
3. 注册事件处理程序以监听市场数据更新。

### 示例

```python
from ib_async import IB
from ibevent.events import IBEventType
from ib_async.contract import Forex

# 创建IB连接
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# 创建USD/JPY合约
usd_jpy = Forex('USDJPY')

# 注册K线更新处理程序
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

# 运行直到中断
ib.run()
```

## 特性

- 事件驱动框架，用于处理IB API事件。
- 支持异步事件处理。
- 多数据流的优先级事件处理程序。

## API参考

有关详细的API文档，请参阅 [MkDocs文档](https://ShawnDen-coder.github.io/ibevent)。
