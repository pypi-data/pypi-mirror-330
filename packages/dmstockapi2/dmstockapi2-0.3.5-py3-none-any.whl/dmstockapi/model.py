from typing import List

from pydantic import BaseModel, Field

from dmstockapi.constant import *


class OrderModel(BaseModel):
    # 指令 数据模型
    account: str = Field(
        "",
        title="投资账号",
    )
    accountname: str = Field("", title="投资账号名称")

    amount: float = Field(0.0, title="金额")
    amountHKD: float = Field(0.0, title="金额(HK)")

    condition: str = Field("", title="时间", description="指令类型为GTD、DTO时有效")
    credit: CreditFlagEnum = Field(0, title="是否是两融")

    date: str = Field("", title="下单日期", example="2024-07-03")
    time: str = Field("", title="下单时间", example="09:38:29.306")
    execamount: float = Field(0.0, title="已执行金额")
    execamountCNY: float = Field(0.0, title="已执行金额(CNY)")
    execdate: str = Field("", title="执行日期")
    exectime: str = Field("", title="执行时间")
    execvol: float = Field(0.0, title="已执行股数")
    mgrcode: str = Field("", title="用户ID", description="基金经理")

    non_order: bool = Field(False, title="是否是标准指令", example=False)
    oid: str = Field("", title="oid", example="202407030938291")
    ordstatus: OrdStatus = Field(-1, title="指令状态", example=-1)
    ordtype: OrderTypeEnum = Field(0.0, title="指令类型")
    portfolioid: str = Field("", title="持仓类型")
    price: float = Field(0.0, title="价格")
    productid: str = Field("", title="产品ID")
    productname: str = Field("", title="产品名称")
    refprice: float = Field(0.0, title="均价")
    refqty: float = Field(0.0, title="参考股数")
    remark: str = Field("", title="备注")
    riskmsg: str = Field("", title="风控", example="PASS")
    riskstatus: int = Field(0, title="风控", example=0)
    sid: str = Field("", title="股票代码", example="300017.SZ")
    side: TradeSideEnum = Field(0, title="买卖")
    sname: str = Field("", title="股票名称")
    strategy: StrategyEnum = Field(1, title="策略")
    switchId: str = Field("", title="换股ID")
    tradercode: str = Field("", title="交易员")
    volume: float = Field(0.0, title="指令股数")


class OrderSummaryModel(BaseModel):
    # 指令汇总模型
    account: str = Field("", title="投资账号")
    accountname: str = Field("", title="投资账号名称")
    execamount: float = Field(0.0, title="已执行金额")
    execamountCNY: float = Field(0.0, title="已执行金额(CNY)")
    execqty: float = Field(0.0, title="已执行股数")
    mgrcode: str = Field("", title="用户ID", description="基金经理")

    orderamount: float = Field(0.0, title="指令中金额")
    orderamountHKD: float = Field(0.0, title="指令中金额(HKD)")
    orderqty: float = Field(0.0, title="指令股数")

    sid: str = Field("", title="股票代码")
    side: TradeSideEnum = Field(0, title="买卖")
    sname: str = Field("", title="股票名称")
    productid: str = Field("", title="产品ID")
    productname: str = Field("", title="产品名称")


class OrderNetstatModel(BaseModel):
    account: str = Field("", title="投资账号")
    name: str = Field("", title="投资账号名称")
    investor: str = Field("", title="资金账号")

    pid: str = Field("", title="产品ID")
    pname: str = Field("", title="产品名称")
    execamount: float = Field(0.0, title="已执行金额")


class InvestAccountModel(BaseModel):
    userId: str = Field("", title="投资经理")
    account: str = Field("", title="投资账号")
    name: str = Field("", title="投资账号名称")

    creditused: float = Field(0.0, title="信用负债")
    avaCash: float = Field(0.0, title="可用现金")
    avaMargin: float = Field(0.0, title="可用融资额")
    frozenCash: float = Field(0.0, title="已冻结现金")
    frozenMargin: float = Field(0.0, title="已冻结保证金")
    totalCash: float = Field(0.0, title="totalCash")
    totalMargin: float = Field(0.0, title="totalMargin")

    stockEquity: float = Field(0.0, title="股票权益")
    stockMv: float = Field(0.0, title="股票市值")
    mvpct: float = Field(0.0, title="持仓比例")

    hispnl: float = Field(0.0, title="hispnl")
    maxdd: float = Field(0.0, title="当前回撤")
    nav: float = Field(0, title="净值")
    navdate: str = Field("", title="净值日期", example="2024-07-17")
    navpct: float = Field(0.0, title="navpct")

    pnl: float = Field(0, title="浮动盈亏")
    pnlpct: float = Field(0.0, title="盈亏比例")

    share: float = Field(0, title="份额")
    cost: float = Field(0.0, title="成本")

    ytdnavpct: float = Field(0.0, title="今年以来盈亏比例")
    ytdpnl: float = Field(0.0, title="今年以来盈亏")


class QueryAccountPlans(BaseModel):
    """
    根据投资账号查询交易计划
    """

    account: str = Field("", title="投资账号")

    class Config:
        str_strip_whitespace = True


class QueryPlanPosition(BaseModel):
    """
    查询交易计划的持仓明细
    """

    planid: str = Field("", title="交易计划ID")

    class Config:
        str_strip_whitespace = True


class PositionModel(BaseModel):
    # 仓位模型
    account: str = Field("", title="投资账号")
    sym: str = Field(0.0, title="股票代码")
    level: int = Field(2, title="层级", description="固定值", example=2)

    id: str = Field(
        0.0,
        title="Position ID",
    )
    indexId: str = Field(
        0.0,
        title="Position ID",
    )
    positionid: str = Field(
        0.0,
        title="Position ID",
    )
    planid: str = Field(
        0,
        title="Plan ID",
    )

    cost1: float = Field(0.0, title="摊薄成本")
    cost2: float = Field(0.0, title="买入成本")
    cost3: float = Field(0.0, title="严格摊薄成本")
    credit: CreditFlagEnum = Field(0, title="融资标志位")
    closeprofit: float = Field(0.0, title="平仓盈亏")

    mv: float = Field(0.0, title="市值")
    mvpct: float = Field(0.0, title="市值比例")

    pnl: float = Field(0, title="浮动盈亏")
    pnlpct: float = Field(0.0, title="盈亏比例")

    portfolioid: PortfolioEnum = Field("", title="持仓类型")

    price: float = Field(0.0, title="当前价格")
    date: str = Field("", title="建仓日期")
    time: str = Field(0.0, title="建仓时间")

    vol: float = Field(0.0, title="昨仓")
    volt: float = Field(0.0, title="今仓")
    availablevol: float = Field(0.0, title="可卖仓位")
    frozenvol: float = Field(0.0, title="冻结仓位")


class PlanModel(BaseModel):
    # 交易计划 模型
    account: str = Field("", title="投资账号", example="800048")
    attribute: str = Field("", title="投资账号", example="SELF")

    children: List[PositionModel] = Field([], title="仓位", example=[])
    ckeys: List[str] = Field([], title="仓位ID", example=[])

    sym: str = Field(0.0, title="股票代码", example="601127.SH")
    name: str = Field(0.0, title="股票代码", example="601127.SH")
    level: int = Field(0.0, title="层级", description="固定值", example=1)

    indexId: str = Field(
        0.0,
        title="Position ID",
    )

    planid: str = Field(
        0,
        title="Plan ID",
    )
    remark: str = Field(
        "",
        title="备注",
        example="风口龙头",
    )
    dkd: int = Field(1, title="日线多空", example=1)
    dkw: int = Field(-1, title="周线多空", example=1)
    cost1: float = Field(0.0, title="摊薄成本", example=1)
    credit: CreditFlagEnum = Field(0, title="融资标志位")
    closeprofit: float = Field(0.0, title="平仓盈亏")

    mv: float = Field(0.0, title="市值")
    mvpct: float = Field(0.0, title="市值比例")

    pnl: float = Field(0, title="浮动盈亏")
    pnlpct: float = Field(0.0, title="盈亏比例")

    portfolioid: str = Field(0, title="持仓类型")
    price: float = Field(0.0, title="价格")
    orderedamount: float = Field(0.0, title="指令中的金额")

    vol: float = Field(0.0, title="昨仓")
    volt: float = Field(0.0, title="今仓")
    frozenvol: float = Field(0.0, title="冻结仓位")


class StockTradeBuyModel(BaseModel):
    """
    股票买入
    """

    mgrcode: str = Field(..., title="用户ID")
    account: str = Field(..., title="投资账号")
    portfolioid: str = Field(..., title="持仓类型")
    planid: str = Field(..., title="计划ID")
    sym: str = Field(..., title="股票代码")
    credit: CreditFlagEnum = Field(..., title="是否融资买入")
    amount: float = Field(..., title="买入金额")
    strategy: StrategyEnum = Field(..., title="策略")
    price: float = Field(0.00, title="价格", description="strategy为限价时有效")
    order_type: OrderTypeEnum = Field(OrderTypeEnum.Normal.value, title="指令类型")
    condition: str = Field(
        "",
        title="时间",
        description="指令类型为GTD、DTO时有效, GTD的格式: YYYY-mm-DD (2024-09-20); DTO的格式: YYYY-mm-DD HH:MM (2024-09-20 10:30); ",
    )
    remark: str = Field("", title="备注")

    class Config:
        # Will remove whitespace from string and byte fields
        str_strip_whitespace = True


class StockTradeSellModel(BaseModel):
    """
    股票卖出
    """

    mgrcode: str = Field(..., title="用户ID")
    account: str = Field(..., title="投资账号")
    portfolioid: str = Field(..., title="持仓类型")
    planid: str = Field(..., title="计划ID")
    sym: str = Field(..., title="股票代码")
    volume: int = Field(..., title="卖出量")
    strategy: StrategyEnum = Field(..., title="策略")
    price: float = Field(0.00, title="价格", description="strategy为限价时有效")
    order_type: OrderTypeEnum = Field(OrderTypeEnum.Normal.value, title="指令类型")
    condition: str = Field(
        "",
        title="时间",
        description="指令类型为GTD、DTO时有效, GTD的格式: YYYY-mm-DD (2024-09-20); DTO的格式: YYYY-mm-DD HH:MM (2024-09-20 10:30); ",
    )
    remark: str = Field("", title="备注")

    stype: SellStypeEnum = Field(..., title="卖出仓位方式")
    positionids: list = Field(
        [],
        title="卖出的仓位ID, stype 为 SellStypeEnum.Positionid 有效, 手动选择仓位进行卖出",
    )
    position_order: PositionOrderEnum = Field(
        PositionOrderEnum.DateAsc.value,
        title="仓位排序, stype 为 SellStypeEnum.Volume 有效, 自动匹配仓位进行卖出",
    )

    class Config:
        # Will remove whitespace from string and byte fields
        str_strip_whitespace = True


class FutureOrderModel(BaseModel):
    account: str = Field(..., title="投资账号")
    portfolioid: str = Field(..., title="持仓类型")
    planid: str = Field(..., title="计划ID")
    sym: str = Field(..., title="期货代码")
    openclose: FutureOpenCloseEnum = Field(..., title="开平仓类型")
    ordtype: OrderTypeEnum = Field(OrderTypeEnum.Normal.value, title="指令类型")
    positionids: list = Field([], title="卖出的仓位ID")
    price: float = Field(..., title="价格", description="strategy为限价时有效")
    volume: float = Field(..., title="交易量", description="交易量")
    remark: str = Field("", title="备注")
    strategy: StrategyEnum = Field(..., title="策略")

    class Config:
        str_strip_whitespace = True
