import asyncio
import importlib.metadata
import os
import time
from enum import Enum
from typing import Optional, Union

import httpx


from .config import read_config_file, get_env

env_settings = get_env()
BASE_URL = env_settings["REASONER_API_BASE_URL"]
REASONER_SDK = "reasoner-1-pro"

try:
    REASONER_SDK_VERSION = importlib.metadata.version("reasonercli")
except:
    print("Failed to resolve SDK version from from installed packages...")
    REASONER_SDK_VERSION = ""

MAX_QUERY_TIMEOUT_SECS = 600  # 10 mins
CHECK_SDK_UPDATE_INTERVAL_SECS = 3600.0  # 1 hour


class TraceStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


def try_get_api_key_from_config_file():
    try:
        config = read_config_file()
        api_key = config.get("API_KEY")
        return api_key
    except Exception:
        pass


class Reasoner:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        from .registry import set_installed_sdk_version, register_reasoner_instance

        register_reasoner_instance(instance)
        set_installed_sdk_version(REASONER_SDK_VERSION)
        return instance

    def __init__(self, api_key: Optional[str] = None, base_url=BASE_URL):
        self.client = None
        self.base_url = base_url

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = try_get_api_key_from_config_file()

        if not self.api_key:
            raise KeyError(
                "API key was not set. It must be set in ~/.reasoner/config or passed into Reasoner(api_key). "
                + "Please run 'reasoner auth' to set up auth config."
            )

        self.client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-REASONER-SDK": REASONER_SDK,
                "X-REASONER-SDK-VERSION": REASONER_SDK_VERSION,
            },
            timeout=300.0,
        )

        self._check_for_updates_if_stale()

    @staticmethod
    def update_last_checked_for_updates(timestamp: float):
        from .registry import set_last_checked_for_updates

        set_last_checked_for_updates(timestamp)

    def _check_for_updates_if_stale(self):
        now = time.time()

        from .registry import get_last_checked_for_updates

        last_checked_for_updates = get_last_checked_for_updates()

        if (
            not last_checked_for_updates
            or now - last_checked_for_updates > CHECK_SDK_UPDATE_INTERVAL_SECS
        ):
            self._sdk_updater.check_for_updates()

    @property
    def _sdk_updater(self):
        from .sdk_updater import SDKUpdater

        return SDKUpdater(self.client, self.base_url, self)

    @property
    def auth(self):
        self._check_for_updates_if_stale()

        from .auth import Auth

        return Auth(self.client, self.base_url)

    @property
    def indexes(self):
        self._check_for_updates_if_stale()

        from .indexes import Indexes

        return Indexes(self.client, self.base_url)

    def trace(
        self, query: str, index_uid: str, options: Union[dict, None] = None, wait=True
    ):
        self._check_for_updates_if_stale()

        data = {"index_uid": index_uid, "query": query}
        if options:
            data["options"] = options

        response = self.client.post(
            f"{self.base_url}/public/v1/trace",
            json=data,
        )
        response.raise_for_status()
        response_json = response.json() or {}
        response_uid = response_json.get("response_uid")
        if not response_uid:
            raise ValueError("Invalid query response")

        if wait:
            return self._poll_for_trace_response(response_uid)
        else:
            return response_uid

    def recall(self, query: str, index_uid: str, source_uid: str, wait=True):
        data = {"index_uid": index_uid, "source_uid": source_uid, "query": query}

        response = self.client.post(
            f"{self.base_url}/public/v1/recall",
            json=data,
        )
        response.raise_for_status()
        response_json = response.json() or {}
        response_uid = response_json.get("response_uid")
        if not response_uid:
            raise ValueError("Invalid recall response")

        if wait:
            return self._poll_for_trace_response(response_uid)
        else:
            return response_uid

    def get_trace_response(self, response_uid: str):
        self._check_for_updates_if_stale()

        response = self.client.get(
            f"{self.base_url}/public/v1/trace/status/{response_uid}",
        )
        response.raise_for_status()
        response_json = response.json() or {}
        return response_json

    def _poll_for_trace_response(self, response_uid: str):
        # Poll for response until it's complete
        start_time = time.time()
        while True:
            response_json = self.get_trace_response(response_uid)
            status = response_json.get("status")

            if status == TraceStatus.SUCCESS.value:
                return response_json.get("response")
            elif status == TraceStatus.ERROR.value:
                raise ValueError("Query processing failed")

            if time.time() - start_time > MAX_QUERY_TIMEOUT_SECS:
                raise TimeoutError(
                    f"Query processing timed out after {MAX_QUERY_TIMEOUT_SECS}s"
                )

            time.sleep(5)


class ReasonerAsync:
    LAST_CHECKED_FOR_UPDATES = None

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        from .registry import set_installed_sdk_version, register_reasoner_instance

        register_reasoner_instance(instance)
        set_installed_sdk_version(REASONER_SDK_VERSION)

        return instance

    def __init__(self, api_key: Optional[str] = None, base_url=BASE_URL):
        self.api_key = api_key
        self.client = None
        self.base_url = base_url

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = try_get_api_key_from_config_file()

        if not self.api_key:
            raise KeyError(
                "API key was not set. It must be set in ~/.reasoner/config or passed into Reasoner(api_key). "
                + "Please run 'reasoner auth' to set up auth config."
            )

        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-REASONER-SDK": REASONER_SDK,
                "X-REASONER-SDK-VERSION": REASONER_SDK_VERSION,
            },
            timeout=300.0,
        )

        self._sync_client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-REASONER-SDK": REASONER_SDK,
                "X-REASONER-SDK-VERSION": REASONER_SDK_VERSION,
            },
            timeout=300.0,
        )

        self._check_for_updates_if_stale()

    @staticmethod
    def update_last_checked_for_updates(timestamp: float):
        from .registry import set_last_checked_for_updates

        set_last_checked_for_updates(timestamp)

    def _check_for_updates_if_stale(self):
        now = time.time()

        from .registry import get_last_checked_for_updates

        last_checked_for_updates = get_last_checked_for_updates()

        if (
            not last_checked_for_updates
            or now - last_checked_for_updates > CHECK_SDK_UPDATE_INTERVAL_SECS
        ):
            try:
                from .sdk_updater import SDKUpdater

                SDKUpdater(self._sync_client, self.base_url, self).check_for_updates()
            except Exception:
                pass

    @property
    def _sdk_updater(self):
        from .sdk_updater import SDKUpdaterAsync

        return SDKUpdaterAsync(self.client, self.base_url, self)

    @property
    def auth(self):
        self._check_for_updates_if_stale()

        from .auth import AuthAsync

        return AuthAsync(self.client, self.base_url)

    @property
    def indexes(self):
        self._check_for_updates_if_stale()

        from .indexes import IndexesAsync

        return IndexesAsync(self.client, self.base_url)

    async def trace(
        self, query: str, index_uid: str, options: Union[dict, None] = None, wait=True
    ):
        self._check_for_updates_if_stale()

        data = {"index_uid": index_uid, "query": query}
        if options:
            data["options"] = options

        response = await self.client.post(
            f"{self.base_url}/public/v1/trace",
            json=data,
        )
        response.raise_for_status()
        response_json = response.json() or {}
        response_uid = response_json.get("response_uid")
        if not response_uid:
            raise ValueError("Invalid query response")

        if wait:
            return await self._poll_for_trace_response(response_uid)
        else:
            return response_uid

    async def recall(self, query: str, index_uid: str, source_uid: str, wait=True):
        data = {"index_uid": index_uid, "source_uid": source_uid, "query": query}

        response = await self.client.post(
            f"{self.base_url}/public/v1/recall",
            json=data,
        )
        response.raise_for_status()
        response_json = response.json() or {}
        response_uid = response_json.get("response_uid")
        if not response_uid:
            raise ValueError("Invalid recall response")

        if wait:
            return await self._poll_for_trace_response(response_uid)
        else:
            return response_uid

    async def get_trace_response(self, response_uid: str):
        self._check_for_updates_if_stale()

        response = await self.client.get(
            f"{self.base_url}/public/v1/trace/status/{response_uid}",
        )
        response.raise_for_status()
        response_json = response.json() or {}
        return response_json

    async def _poll_for_trace_response(self, response_uid: str):
        # Poll for response until it's complete
        start_time = time.time()
        while True:
            response_json = await self.get_trace_response(response_uid)
            status = response_json.get("status")

            if status == TraceStatus.SUCCESS.value:
                return response_json.get("response")
            elif status == TraceStatus.ERROR.value:
                raise ValueError("Query processing failed")

            if time.time() - start_time > MAX_QUERY_TIMEOUT_SECS:
                raise TimeoutError(
                    f"Query processing timed out after {MAX_QUERY_TIMEOUT_SECS}s"
                )

            await asyncio.sleep(5)
