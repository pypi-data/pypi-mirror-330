# thsdata


# Installation
```bash
pip install --upgrade thsdata
```

# Usage

```python

from thsdata import ZhuThsQuote, FuquanNo, KlineDay
import pandas as pd


def main():
    # 初始化
    quote = ZhuThsQuote()

    try:
        # 连接到行情服务器
        login_reply = quote.connect()
        if login_reply.err_code != 0:
            print(f"登录错误:{login_reply.err_code}, 信息:{login_reply.err_message}")
            return
        else:
            print("Connected to the server.")

        # 获取历史日级别数据
        reply = quote.security_bars("USHA600519", 20240101, 20250228, FuquanNo, KlineDay)

        if reply.err_code != 0:
            print(f"查询错误:{reply.err_code}, 信息:{reply.err_message}")
            return

        resp = reply.resp
        df = pd.DataFrame(resp.data)
        print(df)

        print("查询成功 数量:", len(resp.data))

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 断开连接
        quote.disconnect()
        print("Disconnected from the server.")


if __name__ == "__main__":
    main()

```
result:
```
Connected to the server.
          time    close   volume    turnover     open     high      low
0   2024-01-02  1685.01  3215644  5440082500  1715.00  1718.19  1678.10
1   2024-01-03  1694.00  2022929  3411400700  1681.11  1695.22  1676.33
2   2024-01-04  1669.00  2155107  3603970100  1693.00  1693.00  1662.93
3   2024-01-05  1663.36  2024286  3373155600  1661.33  1678.66  1652.11
4   2024-01-08  1643.99  2558620  4211918600  1661.00  1662.00  1640.01
..         ...      ...      ...         ...      ...      ...      ...
273 2025-02-24  1479.07  3474373  5157907300  1488.00  1499.52  1474.00
274 2025-02-25  1454.00  2838743  4142814500  1470.01  1473.39  1452.00
275 2025-02-26  1460.01  2636609  3835949000  1455.45  1464.96  1445.00
276 2025-02-27  1485.56  4976217  7368002400  1460.02  1489.90  1454.00
277 2025-02-28  1500.79  5612895  8475738200  1485.50  1528.38  1482.00

[278 rows x 7 columns]
查询成功 数量: 278
Disconnected from the server.
```

```python
from thsdata import BlockThsQuote
import pandas as pd


def main():
    # 初始化
    quote = BlockThsQuote()

    try:
        # 连接到行情服务器
        login_reply = quote.connect()
        if login_reply.err_code != 0:
            print(f"登录错误:{login_reply.err_code}, 信息:{login_reply.err_message}")
            return
        else:
            print("Connected to the server.")

        # 获取历史日级别数据
        reply = quote.get_block_data(0xCE5F)
        if reply.err_code != 0:
            print(f"查询错误:{reply.err_code}, 信息:{reply.err_message}")
            return

        resp = reply.resp
        df = pd.DataFrame(resp.data)
        print(df)

        print("查询成功 数量:", len(resp.data))

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 断开连接
        quote.disconnect()
        print("Disconnected from the server.")


if __name__ == "__main__":
    main()

```
result:
```
Connected to the server.
          code   name
0   URFI881165     综合
1   URFI881171  自动化设备
2   URFI881118   专用设备
3   URFI881141     中药
4   URFI881157     证券
..         ...    ...
85  URFI881138   包装印刷
86  URFI881121    半导体
87  URFI881131   白色家电
88  URFI881273     白酒
89  URFI881271   IT服务

[90 rows x 2 columns]
查询成功 数量: 90
Disconnected from the server.
```