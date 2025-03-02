from thsdk import BaseThsQuote
from thsdk.constants import zhu_addr, fu_addr, info_addr, block_addr


class ZhuThsQuote(BaseThsQuote):
    """
        ZhuThsQuote 主行情数据
        """

    def __init__(self, ops: dict = None):
        if ops is None:
            ops = {}
        if 'addr' not in ops:
            ops['addr'] = zhu_addr
        super().__init__(ops)


class FuThsQuote(BaseThsQuote):
    """
    FuThsQuote 副行情数据
    """

    def __init__(self, ops: dict = None):
        if ops is None:
            ops = {}
        if 'addr' not in ops:
            ops['addr'] = fu_addr
        super().__init__(ops)


class InfoThsQuote(BaseThsQuote):
    """
    InfoThsQuote 获取资讯信息类型数据
    """

    def __init__(self, ops: dict = None):
        if ops is None:
            ops = {}
        if 'addr' not in ops:
            ops['addr'] = info_addr
        super().__init__(ops)


class BlockThsQuote(BaseThsQuote):
    """
    BlockThsQuote 获取板块类型数据
    """

    def __init__(self, ops: dict = None):
        if ops is None:
            ops = {}
        if 'addr' not in ops:
            ops['addr'] = block_addr
        super().__init__(ops)
