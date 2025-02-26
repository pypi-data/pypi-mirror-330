from enum import Enum, IntEnum


class PortfolioEnum(str, Enum):
    """
    股票 组合类型
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | Trade | 交易型 |  trade  |
    | Valuelong | 价值型 |  valuelong  |
    """

    Trade = "trade"
    """交易型"""
    Valuelong = "valuelong"
    """价值型"""


PortfolioEnum.Trade.label = "交易型"
PortfolioEnum.Valuelong.label = "价值型"

PortfolioValues = [member.value for member in PortfolioEnum.__members__.values()]


class StrategyEnum(IntEnum):
    """
    交易策略
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | MARKETP | 价优市价 |  1  |
    | MARKETV | 量优市价 |  2  |
    | LIMITP | 价优限价 |  3  |
    | LIMITV | 量优限价 |  4  |
    | LIMITS | 标准限价 |  5  |
    """

    MARKETP = 1
    """价优市价"""
    MARKETV = 2
    """量优市价"""
    # LIMITP = 3
    # """价优限价"""
    # LIMITV = 4
    # """量优限价"""
    # LIMITS = 5
    # """标准限价"""


StrategyEnum.MARKETP.label = "价优市价"
StrategyEnum.MARKETV.label = "量优市价"


# StrategyEnum.LIMITP.label = "价优限价"
# StrategyEnum.LIMITV.label = "量优限价"
# StrategyEnum.LIMITS.label = "标准限价"


class OrderTypeEnum(IntEnum):
    """
    指令类型
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | Normal | 普通指令 |  0  |
    | GTC | 取消前有效(GTC) |  1  |
    | GTD | 到期前有效(GTD) |  2  |
    | DTO | 定时触发指令(DTO) |  3  |
    | Switch | 换股指令 |  5  |
    """

    Normal = 0
    """普通指令"""
    # GTC = 1
    # """取消前有效(GTC)"""
    # GTD = 2
    # """到期前有效(GTD)"""
    # DTO = 3
    # """到期前有效(GTD)"""
    # Switch = 5
    # """换股指令"""


OrderTypeEnum.Normal.label = "普通指令"


# OrderTypeEnum.GTC.label = "取消前有效(GTC)"
# OrderTypeEnum.GTD.label = "到期前有效(GTD)"
# OrderTypeEnum.DTO.label = "到期前有效(GTD)"
# OrderTypeEnum.Switch.label = "换股指令"


class TradeSideEnum(IntEnum):
    """
    买卖方向
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | Buy | 买入 |  1  |
    | Sell | 卖出 |  -1  |
    """

    Buy = 1
    Sell = -1


TradeSideEnum.Buy.label = "买入"
TradeSideEnum.Sell.label = "卖出"


class CreditFlagEnum(IntEnum):
    """
    买入标志
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | Cash | 现金买入 |  0  |
    | Credit | 两融买入 |  1  |
    """

    Cash = 0
    """现金买入"""
    Credit = 1
    """两融买入"""


CreditFlagEnum.Cash.label = "现金买入"
CreditFlagEnum.Credit.label = "两融买入"


class SellStypeEnum(IntEnum):
    """
    卖出仓位方式
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | Volume | 根据卖出量按顺序选择position卖出 |  1  |
    | Positionid | 根据已选的position进行卖出 |  2  |
    """

    Volume = 1
    """根据卖出量按顺序选择position卖出"""
    Positionid = 2
    """根据已选的position进行卖出"""


class PositionOrderEnum(IntEnum):
    """
    仓位排序
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | VolumeAsc | 持仓量升序 |  1  |
    | VolumeDesc | 持仓量降序 |  2  |
    | DateAsc | 时间升序 |  3  |
    | DateDesc | 时间降序 |  4  |
    """

    VolumeAsc = 1
    """持仓量升序"""
    VolumeDesc = 2
    """持仓量降序"""
    DateAsc = 3
    """时间升序"""
    DateDesc = 4
    """时间降序"""


PositionOrderValues = [
    member.value for member in PositionOrderEnum.__members__.values()
]


class OrdStatus(IntEnum):
    """
    指令状态
    | Name | Label | Value   |
    | :--: | :--: | :--:  |
    | PendingNew | 已下达 |  10  |
    | New | 已接受 |  0  |
    | Filled | 已成交 |  2  |
    | Rejected | 已拒绝 |  8  |
    | PartiallyFilled | 部分成交 |  1  |
    | PendingCancel | 撤单中 |  6  |
    | Canceled | 已撤单 |  4  |
    """

    PendingNew = 10
    """已下达"""
    New = 0
    """已接受"""
    Filled = 2
    """已成交"""
    Rejected = 8
    """已拒绝"""
    PartiallyFilled = 1
    """部分成交"""
    PendingCancel = 6
    """撤单中"""
    Canceled = 4
    """已撤单"""


class FutureOpenCloseEnum(IntEnum):
    OpenLong = 4
    OpenShort = 5
    CloseLong = 6
    CloseShort = 8


FutureOpenCloseEnum.OpenLong.label = "开多"
FutureOpenCloseEnum.OpenShort.label = "开空"
FutureOpenCloseEnum.CloseLong.label = "平多"
FutureOpenCloseEnum.CloseShort.label = "平空"
