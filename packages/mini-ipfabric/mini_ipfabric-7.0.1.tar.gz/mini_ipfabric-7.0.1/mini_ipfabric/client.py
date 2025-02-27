import json
import re
from collections import OrderedDict

from typing import Union, Tuple, Dict, List
from urllib.parse import urljoin, urlparse

from requests import Session
from requests.auth import HTTPBasicAuth

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

OAS_DIR = files("mini_ipfabric.oas")
RE_PATH = re.compile(r"^/?(api/)?v\d(\.\d)?/")


class IPFClient(Session):
    def __init__(
        self,
        base_url: str,
        auth: Union[str, Tuple[str, str]],
        snapshot_id: str = "$last",
        verify: bool = True,
        timeout: float = None,
    ):
        super().__init__()
        self.verify = verify
        self.base_url = base_url
        self.timeout = timeout
        self.headers["User-Agent"] = (
            f'mini-ipfabric-sdk/{metadata.version("mini_ipfabric")}'
        )
        if isinstance(auth, str):
            self.headers["X-API-Token"] = auth
        elif isinstance(auth, tuple):
            self.auth = HTTPBasicAuth(auth[0], auth[1])
        else:
            self.auth = auth

        resp = self.get(urljoin(self.base_url, "/api/version"))
        resp.raise_for_status()
        self.version = resp.json()["apiVersion"]
        self.oas = self._load_oas()
        self.base_url = urljoin(self.base_url, f"/api/{self.version}/")
        self.snapshots = self.get_loaded_snapshots()
        self._snapshot_id, self.snapshot = None, None
        self.snapshot_id = snapshot_id

    def _load_oas(self):
        try:
            return json.loads(OAS_DIR.joinpath(self.version + ".json").read_text())
        except FileNotFoundError:
            paths = self.get(
                urljoin(self.base_url, "/api/static/oas/openapi-internal.json")
            ).json()["paths"]
            oas = dict()
            for path, methods in paths.items():
                oas[path[1:]] = {"full_api_endpoint": path}
                for method in ["get", "post"]:
                    if method not in methods:
                        oas[path[1:]][method] = None
                        continue
                    spec = methods[method]
                    try:
                        web_endpoint = spec["x-table"]["webPath"]
                    except KeyError:
                        web_endpoint = None
                    try:
                        columns = list(
                            set(
                                spec["requestBody"]["content"]["application/json"][
                                    "schema"
                                ]["properties"]["columns"]["items"]["enum"]
                            )
                        )
                    except KeyError:
                        columns = None
                    oas[path[1:]][method] = {
                        "full_api_endpoint": path,
                        "summary": spec["summary"],
                        "description": spec["description"],
                        "web_endpoint": web_endpoint,
                        "columns": columns,
                    }
            return oas

    @property
    def snapshot_id(self) -> str:
        return self._snapshot_id

    @snapshot_id.setter
    def snapshot_id(self, v):
        self.snapshot = self.snapshots[v]
        self._snapshot_id = self.snapshot["id"]

    @property
    def web_path(self) -> Dict[str, dict]:
        return {
            v["post"]["web_endpoint"]: v["post"]
            for v in self.oas.values()
            if v["post"] and v["post"]["web_endpoint"]
        }

    def _check_url(self, url) -> str:
        path = urlparse(url).path
        path = path if path[0] == "/" else "/" + path
        if path in self.web_path:
            return self.web_path[path]["full_api_endpoint"][1:]
        r = RE_PATH.search(path)
        url = path[r.end():] if r else path  # fmt: skip
        url = url[1:] if url[0] == "/" else url
        return url

    @property
    def technology(self) -> Dict[str, dict]:
        return {k: v for k, v in self.web_path.items() if k.startswith("/technology")}

    @property
    def inventory(self) -> Dict[str, dict]:
        return {k: v for k, v in self.web_path.items() if k.startswith("/inventory")}

    def fetch_all(
        self,
        endpoint: str,
        columns: list = None,
        reports: bool = False,
        filters: dict = None,
    ) -> List[dict]:
        path = self._check_url(endpoint)
        data = self.oas[path]["post"]
        payload = {
            "columns": columns or data["columns"],
            "snapshot": self.snapshot_id,
        }
        if reports:
            payload["reports"] = data["web_endpoint"]
        if filters:
            payload["filters"] = filters
        return self._ipf_pager(
            urljoin(self.base_url, data["full_api_endpoint"][1:]), payload=payload
        )

    def get_intents(self) -> List[dict]:
        resp = self.get(
            urljoin(self.base_url, "reports"), params=dict(snapshot=self.snapshot_id)
        )
        resp.raise_for_status()
        intents = resp.json()
        for intent in intents:
            for _ in ["0", "10", "20", "30"]:
                if _ not in intent["result"]["checks"]:
                    intent["result"]["checks"][_] = None
        return intents

    def get_loaded_snapshots(self):
        payload = {
            "columns": self.oas["tables/management/snapshots"]["post"]["columns"],
            "sort": {"order": "desc", "column": "tsEnd"},
            "filters": {
                "and": [{"status": ["eq", "done"]}, {"finishStatus": ["eq", "done"]}]
            },
        }
        resp = self.post(
            urljoin(self.base_url, "tables/management/snapshots"),
            json=payload,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        snap_dict = OrderedDict()
        for snap in resp.json()["data"]:
            snap_dict[snap["id"]] = snap
            if "$lastLocked" not in snap_dict and snap["locked"]:
                snap_dict["$lastLocked"] = snap
            if "$last" not in snap_dict:
                snap_dict["$last"] = snap
                continue
            if "$prev" not in snap_dict:
                snap_dict["$prev"] = snap
        return snap_dict

    def _ipf_pager(
        self,
        url: str,
        payload: dict,
        limit: int = 1000,
        start: int = 0,
    ):
        """
        Loops through and collects all the data from the tables
        :param url: str: Full URL to post to
        :param payload: dict: Data to submit to IP Fabric
        :param start: int: Where to start for the data
        :return: list: List of dictionaries
        """
        payload["pagination"] = dict(limit=limit)
        data = list()

        def page(s):
            payload["pagination"]["start"] = s
            r = self.post(url, json=payload, timeout=self.timeout)
            r.raise_for_status()
            return r.json()["data"]

        r_data = page(start)
        data.extend(r_data)
        while limit == len(r_data):
            start = start + limit
            r_data = page(start)
            data.extend(r_data)
        return data
