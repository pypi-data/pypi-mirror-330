from pydantic import BaseModel, Field

from dmstockapi.constant import FutureOpenCloseEnum, OrderTypeEnum, StrategyEnum


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
