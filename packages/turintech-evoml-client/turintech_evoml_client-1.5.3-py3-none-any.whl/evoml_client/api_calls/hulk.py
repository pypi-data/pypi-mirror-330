# ───────────────────────────────── imports ────────────────────────────────── #
from typing import List, Tuple
from enum import Enum

import pandas as pd
import requests
from pydantic import BaseModel

from evoml_client.api_calls.utils import (
    get_auth,
    check_status_code,
    get_url,
    is_url_https,
    REQUEST_TIMEOUT,
)


# ──────────────────────────────────────────────────────────────────────────── #


class HulkTarget(Enum):
    sql = "sql"


class HulkConnectionInfo(BaseModel):
    type: str
    hostname: str
    port: int
    database: str
    user: str
    password: str


def get_tables(connection_info: HulkConnectionInfo) -> List[str]:
    """gives a list of all tables in the given database"""
    target_url = f"{get_url('hulk')}/sql/show-tables"
    request_json = connection_info.dict()
    response = requests.post(
        url=target_url,
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()["tables"]


def get_table(
    connection_info: HulkConnectionInfo,
    table: str,
) -> pd.DataFrame:
    """retreives a sample of a given table"""
    target_url = f"{get_url('hulk')}/sql/preview"
    request_json = connection_info.dict()
    request_json["table"] = table
    response = requests.post(
        url=target_url,
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("hulk"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    preview = pd.DataFrame(
        columns=response.json()["columnNames"],
        data=response.json()["columnValues"],
    )
    return preview


def upload_from_sql(connection_info: HulkConnectionInfo, table: str) -> Tuple[str, dict]:
    """triggers data ingestor and returns file id"""
    target_url = f"{get_url('hulk')}/sql/ingest"
    request_json = connection_info.dict()
    request_json["table"] = table
    response = requests.post(
        url=target_url,
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("hulk"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()["_id"], response.json()["analysis"]
