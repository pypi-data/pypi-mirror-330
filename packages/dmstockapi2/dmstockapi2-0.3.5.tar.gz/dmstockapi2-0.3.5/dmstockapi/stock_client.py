import json
from typing import List

import requests
import pandas as pd

from requests.adapters import HTTPAdapter, Retry

from dmstockapi.constant import (
    TradeSideEnum,
    SellStypeEnum,
    PositionOrderEnum,
    CreditFlagEnum,
)
from dmstockapi.model import *
from dmstockapi.exceptions import DMStockAPIException, DMStockRequestException


class StockClient:

    def __init__(
        self,
        api_key="",
        api_base_url="",
        keep_alive=False,
        max_retry=5,
    ):
        self.api_base_url = api_base_url
        self.keep_alive = keep_alive
        self.max_retry = max_retry
        self._session = self._init_session(api_key)

    def _init_session(self, api_key):
        session = requests.Session()
        session.headers.update(
            {
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate,sdch",
                "User-Agent": "dmstockapi/python",
                "Content-Type": "application/json",
                "Apikey": api_key,
            }
        )
        if self.keep_alive:
            session.headers.update({"Connection": "keep-alive"})
            retries = Retry(
                total=self.max_retry, backoff_factor=1, status_forcelist=[502, 503, 504]
            )
            session.mount("http://", adapter=HTTPAdapter(max_retries=retries))

        return session

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def _request(self, method, path, **kwargs):
        url = f"{self.api_base_url}{path}"
        if method == "get":
            kwargs["params"] = self._format_params(kwargs.get("params", {}))
            # response = getattr(self._session, method)(url, **kwargs)
            response = self._session.get(url=url, **kwargs)
            return self._handle_response(response)

        elif method == "post":
            json_data = json.dumps(kwargs.get("params", {}))
            response = self._session.post(url=url, data=json_data)
            return self._handle_response(response)

        else:
            print(f"Invalid Method: {method}")
            raise DMStockRequestException(f"Invalid Method: {method}")

    @staticmethod
    def _handle_response(response):
        if not response.ok:
            raise DMStockAPIException(response)

        try:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            if "text/csv" in content_type:
                return response.text
            if "text/plain" in content_type:
                return response.text
            raise DMStockRequestException("Invalid Response: {}".format(response.text))
        except ValueError:
            raise DMStockRequestException("Invalid Response: {}".format(response.text))

    @staticmethod
    def _merge_two_dicts(first, second):
        result = first.copy()
        result.update(second)
        return result

    @staticmethod
    def _format_params(params):
        return {
            k: json.dumps(v) if isinstance(v, bool) else v for k, v in params.items()
        }

    def _get(self, path, **kwargs):
        if not kwargs["params"]["isdataframe"]:
            return self._request("get", path, **kwargs)
        else:
            response_json = self._request("get", path, **kwargs)
            return pd.DataFrame.from_dict(response_json["data"])

    def _post(self, path, **kwargs):
        if not kwargs["params"]["isdataframe"]:
            return self._request("post", path, **kwargs)
        else:
            response_json = self._request("post", path, **kwargs)
            return pd.DataFrame.from_dict(response_json["data"])

    @property
    def api_key(self):
        return self._session.params.get("api_key")

    @api_key.setter
    def api_key(self, api_key):
        self._session.params["api_key"] = api_key

    def query_algo(self, isdataframe=True, **kwargs) -> List[OrderModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-trade/orders", params=params)
        return r

    def query_algo_summary(self, isdataframe=True, **kwargs) -> List[OrderSummaryModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-trade/order-summary", params=params)
        return r

    def query_algo_netstat(self, isdataframe=True, **kwargs) -> List[OrderNetstatModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-trade/order-netstat", params=params)
        return r

    def query_account(self, isdataframe=True, **kwargs) -> List[InvestAccountModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/account-info/stock-accounts", params=params)
        return r

    def query_account_planning(
        self, params: QueryAccountPlans, isdataframe=True, **kwargs
    ) -> List[PlanModel]:
        if params.account == "":
            raise DMStockRequestException(f"Invalid Request Params: {params.__dict__}")

        req_params = self._merge_two_dicts(
            {
                "account": params.account,
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-plan/plans", params=req_params)
        return r

    def query_plan_position(
        self, params: QueryPlanPosition, isdataframe=True, **kwargs
    ):
        if params.planid == "":
            raise DMStockRequestException(f"Invalid Request Params: {params.__dict__}")

        req_params = self._merge_two_dicts(
            {
                "planId": params.planid,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/stock-plan/plan-position", params=req_params)
        return r

    def check_plan(self, account: str, portfolio: str, planid: str, sid: str):
        plans_resp = self.query_account_planning(
            QueryAccountPlans(account=account), isdataframe=False
        )
        if plans_resp["status"] == 200:
            for plan in plans_resp["data"]:
                if (
                    plan["portfolioid"] == portfolio
                    and plan["planid"] == planid
                    and plan["sym"] == sid
                ):
                    return True
        return False

    def stock_buy(self, params: StockTradeBuyModel, isdataframe=False, **kwargs):
        if params.amount <= 0:
            raise DMStockRequestException(
                f"Invalid Request Params: (amount), {params.__dict__}"
            )

        # if params.order_type in [OrderTypeEnum.DTO.value, OrderTypeEnum.GTD.value] and params.condition == "":
        #     raise DMStockRequestException(f"Invalid Request Params: (condition), {params.__dict__}")
        #
        # if params.strategy in [StrategyEnum.LIMITP.value, StrategyEnum.LIMITV.value, StrategyEnum.LIMITS.value] and params.price == 0.00:
        #     raise DMStockRequestException(f"Invalid Request Params: (price), {params.__dict__}")

        if not self.check_plan(
            params.account, params.portfolioid, params.planid, params.sym
        ):
            raise DMStockRequestException(
                f"交易计划不存在或填写错误: {params.__dict__}"
            )

        req_params = self._merge_two_dicts(
            {
                "mgrcode": params.mgrcode,
                "accountId": params.account,
                "portfolioId": params.portfolioid,
                "planId": params.planid,
                "stockCode": params.sym,
                "side": TradeSideEnum.Buy.value,
                "credit": params.credit,
                "amount": params.amount,
                "strategy": params.strategy,
                "price": params.price,
                "ordtype": params.order_type,
                "condition": params.condition,
                "remark": params.remark,
                "switchBuyStockCode": "",
                "switchBuyAmount": 0.0,
                "volume": 0,
                "positionId": "",
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/stock-trade/trade", params=req_params)
        return r

    def position_order(self, position: list, order_by: PositionOrderEnum):
        if order_by == PositionOrderEnum.VolumeAsc:
            position.sort(key=lambda x: x["vol"])
        elif order_by == PositionOrderEnum.VolumeDesc:
            position.sort(key=lambda x: x["vol"], reverse=True)
        elif order_by == PositionOrderEnum.DateDesc:
            position.sort(key=lambda x: f"{x['date']} {x['time']}", reverse=True)
        else:
            position.sort(key=lambda x: f"{x['date']} {x['time']}")

        return position

    def stock_sell(self, params: StockTradeSellModel, isdataframe=False, **kwargs):
        if params.volume <= 0:
            raise DMStockRequestException(
                f"Invalid Request Params: (amount), {params.__dict__}"
            )

        # if params.order_type in [OrderTypeEnum.DTO.value, OrderTypeEnum.GTD.value] and params.condition == "":
        #     raise DMStockRequestException(f"Invalid Request Params: (condition), {params.__dict__}")
        #
        # if params.strategy in [StrategyEnum.LIMITP.value, StrategyEnum.LIMITV.value, StrategyEnum.LIMITS.value] and params.price == 0.00:
        #     raise DMStockRequestException(f"Invalid Request Params: (price), {params.__dict__}")

        if not self.check_plan(
            params.account, params.portfolioid, params.planid, params.sym
        ):
            raise DMStockRequestException(
                f"交易计划不存在或填写错误: {params.__dict__}"
            )

        position_resp = self.query_plan_position(
            QueryPlanPosition(planid=params.planid), isdataframe=False
        )
        if position_resp["status"] == 200:
            positions = position_resp["data"]
        else:
            positions = []

        if len(positions) == 0:
            raise DMStockRequestException(f"交易计划暂无仓位: {params.__dict__}")

        positionids = []
        availablevol = 0
        if params.stype == SellStypeEnum.Positionid:
            if len(params.positionids) == 0:
                raise DMStockRequestException(
                    f"Invalid Request Params: (positionids), {params.__dict__}"
                )

            old_positionids = list(set(params.positionids))
            for position in positions:
                if position["id"] in old_positionids:
                    availablevol += position["availablevol"]
                    positionids.append(position["id"])
                    old_positionids.remove(position["id"])

                if len(old_positionids) == 0:
                    break

            if len(old_positionids) != 0:
                raise DMStockRequestException(
                    f"Invalid Request Params: (positionids), {old_positionids}"
                )

        else:
            if params.position_order not in PositionOrderEnum:
                raise DMStockRequestException(
                    f"Invalid Request Params: (position_order), {params.__dict__}"
                )
            new_positions = self.position_order(positions, params.position_order)
            for position in new_positions:
                availablevol += position["availablevol"]
                positionids.append(position["id"])

                if availablevol >= params.volume:
                    break

        if availablevol < params.volume:
            raise DMStockRequestException(
                f"可卖量不足: {availablevol} < {params.volume}"
            )

        req_params = self._merge_two_dicts(
            {
                "mgrcode": params.mgrcode,
                "accountId": params.account,
                "portfolioId": params.portfolioid,
                "planId": params.planid,
                "stockCode": params.sym,
                "side": TradeSideEnum.Sell.value,
                "credit": CreditFlagEnum.Cash.value,
                "amount": 0.00,
                "strategy": params.strategy,
                "price": params.price,
                "ordtype": params.order_type,
                "condition": params.condition,
                "remark": params.remark,
                "switchBuyStockCode": "",
                "switchBuyAmount": 0.0,
                "volume": params.volume,
                "positionId": ",".join(positionids),
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/stock-trade/trade", params=req_params)
        return r
