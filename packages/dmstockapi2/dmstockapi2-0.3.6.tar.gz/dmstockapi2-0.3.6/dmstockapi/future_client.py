import json
import requests
import pandas as pd

from requests.adapters import HTTPAdapter, Retry
from dmstockapi.exceptions import DMStockAPIException, DMStockRequestException
from dmstockapi.future_model import FutureOrderModel


class FutureClient:

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
        if method == "post":
            json_data = json.dumps(kwargs.get("params", {}))
            response = self._session.post(url=url, data=json_data)
            return self._handle_response(response)

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
            data = response_json["data"]
            if isinstance(data, (list, tuple)):
                df = pd.DataFrame.from_dict(data)
            else:
                df = pd.DataFrame.from_dict([data])
            return df

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

    def future_trade_planning(
        self, account_id="", portfolio_id="", isdataframe=True, **kwargs
    ):
        params = self._merge_two_dicts(
            {
                "account": account_id,
                "portfolioid": portfolio_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-plan/plans", params=params)
        return r

    def future_trade_portfolio(self, account_id="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {
                "account": account_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-plan/account-portfolios", params=params)
        return r

    def future_trade_accountinfo(self, account_id="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {
                "account": account_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/account-info/future-accounts", params=params)
        return r

    def future_trade_order(self, params: FutureOrderModel, isdataframe=False, **kwargs):
        if params.volume <= 0:
            raise DMStockRequestException(
                f"Invalid Request Params: (volume), {params.__dict__}"
            )

        req_params = self._merge_two_dicts(
            {
                "account": params.account,
                "openclose": params.openclose,
                "ordtype": params.ordtype,
                "planid": params.planid,
                "portfolioid": params.portfolioid,
                "position_ids": ",".join(params.positionids),
                "price": params.price,
                "remark": params.remark,
                "sid": params.sym,
                "strategy": params.strategy,
                "volume": params.volume,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/future-trade/trade", params=req_params)
        return r

    def future_trade_singleorder(self, order_id="", isdataframe=False, **kwargs):
        params = self._merge_two_dicts(
            {
                "oid": order_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-trade/single-order", params=params)
        return r
