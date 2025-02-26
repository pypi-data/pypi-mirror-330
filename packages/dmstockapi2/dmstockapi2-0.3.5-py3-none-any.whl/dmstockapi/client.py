import json
import requests
import pandas as pd

from dmstockapi.exceptions import DMStockAPIException, DMStockRequestException
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter, Retry


class Client:

    def __init__(
        self,
        api_key="",
        api_url="",
        keep_alive=False,
        max_retry=5,
    ):
        self.API_URL = api_url
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
            }
        )
        if self.keep_alive:
            session.headers.update({"Connection": "keep-alive"})
            retries = Retry(
                total=self.max_retry, backoff_factor=1, status_forcelist=[502, 503, 504]
            )
            session.mount("http://", adapter=HTTPAdapter(max_retries=retries))

        session.params["api_key"] = api_key
        return session

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def _request(self, method, path, **kwargs):
        url = f"{self.API_URL}{path}".format(self.API_URL, path)
        if method == "get":
            kwargs["params"] = self._format_params(kwargs.get("params", {}))
            # response = getattr(self._session, method)(url, **kwargs)
            response = self._session.get(url=url, **kwargs)
            return self._handle_response(response)
        if method == "post":
            json_data = json.dumps(kwargs.get("params", {}))
            response = self._session.post(url=url, json=json_data)
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
            return pd.read_json(response_json)

    def _post(self, path, **kwargs):
        if not kwargs["params"]["isdataframe"]:
            return self._request("post", path, **kwargs)
        else:
            response_json = self._request("post", path, **kwargs)
            return pd.read_json(response_json)

    @property
    def api_key(self):
        return self._session.params.get("api_key")

    @api_key.setter
    def api_key(self, api_key):
        self._session.params["api_key"] = api_key

    def stock_candles(
        self,
        symbol=None,
        interval="",
        start_date="",
        end_date="",
        adjust="",
        isdataframe=True,
        **kwargs,
    ):
        if start_date == "":
            start_date = datetime.strftime(datetime.now() - timedelta(30), "%Y-%m-%d")
        params = self._merge_two_dicts(
            {
                "interval": interval,
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "adjust": adjust,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/stock/china/candle", params=params)
        if "time" in r.columns:
            r["date"] = r.get("date") + pd.to_timedelta(r.get("time"))
            r = r.drop(columns=["time"])
        return r if r.empty else r.set_index("date")

    def index_candles(self, symbol=None, start_date="", isdataframe=True, **kwargs):
        if start_date == "":
            start_date = datetime.strftime(datetime.now() - timedelta(30), "%Y-%m-%d")
        params = self._merge_two_dicts(
            {"symbol": symbol, "start_date": start_date, "isdataframe": isdataframe},
            kwargs,
        )
        return self._get("/stock/china/indexcandle", params=params)

    def stock_profile(self, symbol=None, isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {"symbol": symbol, "isdataframe": isdataframe}, kwargs
        )
        return self._get("/stock/china/profile", params=params)

    def index_profile(self, symbol=None, isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {"symbol": symbol, "isdataframe": isdataframe}, kwargs
        )
        return self._get("/stock/china/index", params=params)

    def stock_sector(self, symbol=None, isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {"symbol": symbol, "isdataframe": isdataframe}, kwargs
        )
        return self._get("/stock/china/sector", params=params)

    def future_candles(
        self,
        symbol=None,
        interval="",
        start_date="",
        end_date="",
        isdataframe=True,
        **kwargs,
    ):
        if start_date == "":
            start_date = datetime.strftime(datetime.now() - timedelta(30), "%Y-%m-%d")
        params = self._merge_two_dicts(
            {
                "interval": interval,
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/future/china/candle", params=params)
        if "time" in r.columns:
            r["date"] = r.get("date") + pd.to_timedelta(r.get("time"))
            r = r.drop(columns=["time"])
        return r if r.empty else r.set_index("date")

    def future_realtime(self, symbol=None, interval="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {"interval": interval, "symbol": symbol, "isdataframe": isdataframe}, kwargs
        )
        r = self._get("/future/china/realtime", params=params)
        if "time" in r.columns:
            r["date"] = r.get("date") + pd.to_timedelta(r.get("time"))
            r = r.drop(columns=["time"])
        return r if r.empty else r.set_index("date")

    def stock_realtime(self, symbol=None, interval="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {"interval": interval, "symbol": symbol, "isdataframe": isdataframe}, kwargs
        )
        r = self._get("/stock/china/realtime", params=params)
        if "time" in r.columns:
            r["date"] = r.get("date") + pd.to_timedelta(r.get("time"))
            r = r.drop(columns=["time"])
        return r if r.empty else r.set_index("date")

    def future_trade_instrument(self, symbol="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {"symbol": symbol, "isdataframe": isdataframe}, kwargs
        )
        r = self._get("/future/china/trade/instrument", params=params)
        return r

    def future_trade_idxpara(self, symbol="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {"symbol": symbol, "isdataframe": isdataframe}, kwargs
        )
        r = self._get("/future/china/trade/idxpara", params=params)
        return r
