# маршрут.екатеринбург.рф
import hashlib
import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)


class EKBTransportAPI:
    base_url = "https://xn--80axnakf7a.xn--80acgfbsl1azdqr.xn--p1ai/api/rpc.php"
    ssl_verify = False
    request_sys_id = "ekt"

    def __init__(self):
        self._session = None
        self._counter = 0

    def _get_jsonrpc_id(self) -> int:
        self._counter += 1
        return self._counter

    @staticmethod
    def _get_timestamp() -> int:
        return int(datetime.utcnow().timestamp())

    @staticmethod
    def request_sign(method: str, jsonrpc_id: int, session_id: str, request_sys_id: str) -> tuple[str, str]:
        sign_string = f"{method}~{request_sys_id}~{jsonrpc_id}~{session_id}"
        hash_string = hashlib.sha1(sign_string.encode("utf-8")).hexdigest()
        guid = f"{hash_string[:8]}-{hash_string[8:12]}-{hash_string[12:16]}-{hash_string[24:28]}-{hash_string[28:40]}"
        magic_str = hash_string[16:24]
        return guid, magic_str

    def _request(self, method: str, params: dict) -> dict:
        jsonrpc_id = self._get_jsonrpc_id()
        query_params = None
        if params and "sid" in params:
            # Добавляет magic в payload запроса
            # Добавляет m в query запроса
            guid, magic_str = self.request_sign(
                method=method, jsonrpc_id=jsonrpc_id, session_id=params["sid"], request_sys_id=self.request_sys_id
            )
            query_params = {
                "m": guid,
            }
            params["magic"] = magic_str
        logger.debug(f"Отправка запроса в маршрут.екатеринбург.рф {method=} {params=}")
        logger.info(f"Отправка запроса в маршрут.екатеринбург.рф {method=}")
        response = requests.post(
            url=self.base_url,
            json={
                "jsonrpc": "2․2",
                "method": method,
                "ts": self._get_timestamp(),
                "params": params,
                "id": jsonrpc_id,
            },
            verify=self.ssl_verify,
            params=query_params,
        )
        result = response.json()
        logger.info(f"Получен ответ от маршрут.екатеринбург.рф {method=}")
        logger.debug(f"Получен ответ от маршрут.екатеринбург.рф {method=} {params=} {result=}")
        return result

    def start_session(self) -> dict:
        return self._request(
            method="startSession",
            params={},
        )

    def _get_sid_session(self) -> str:
        if self._session is None:
            self._session = self.start_session()
        return self._session["result"]["sid"]

    def get_trans_type_tree(self) -> dict:
        return self._request(
            method="getTransTypeTree",
            params={
                "sid": self._get_sid_session(),
                "ok_id": "",
            },
        )

    def get_route(self, mr_id: str) -> dict:
        return self._request(
            method="getRoute",
            params={
                "sid": self._get_sid_session(),
                "mr_id": mr_id,
            },
        )

    def get_stop_arrive(self, st_id: str):
        return self._request(
            method="getStopArrive",
            params={
                "sid": self._get_sid_session(),
                "st_id": st_id,
            },
        )
