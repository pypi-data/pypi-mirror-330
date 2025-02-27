# ────────────────────────────────── imports ───────────────────────────────── #
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Union, Optional, Sequence, Dict
from time import sleep
from pathlib import Path
from enum import Enum

from tqdm import tqdm
import requests
from pydantic import BaseSettings
from requests import Response, Request, Session

from evoml_client.conf.environment_conf import EnvironmentConf, environment_conf_factory, request_raw_config
from evoml_client.conf.conf_manager import conf_mgr
from evoml_client.models import Pipeline, ProcessInfo, Status

# ──────────────────────────────────────────────────────────────────────────── #

ServiceNameT = Literal["file-api", "enigma", "platform", "loki", "black-widow", "rocket", "hulk"]
EnvirontmentNameT = Literal["dev", "staging", "release"]

# ──────────────────────────────────────────────────────────────────────────── #


CONFIG: EnvironmentConf

AUTH_HEADER = None
DOWNLOAD_PATH = None
REQUEST_TIMEOUT = 60


# ──────────────────────────────── Exceptions ──────────────────────────────── #
class StatusCodeException(Exception): ...


# ────────────────────────────── General Helpers ───────────────────────────── #
def check_status_code(response: Response, expected_code: Union[int, Sequence[int]]) -> None:
    """Raises an exception if the status does not have the expected value"""
    if response.status_code == expected_code or (
        isinstance(expected_code, list) and response.status_code in expected_code
    ):
        return

    print(response.content)
    raise StatusCodeException(
        "Expected status code {expected}, received [{actual}] {message}".format(
            expected=expected_code,
            actual=response.status_code,
            message=response.reason,
        )
    )


def get_url(service: ServiceNameT) -> str:
    """Get the full url of a specific environment/service combination."""

    mappings: Dict[ServiceNameT, str] = {
        "file-api": f"{CONFIG.microservices.thor_api_url}/api",
        "enigma": f"{CONFIG.microservices.thanos_api_url}/api",
        "platform": f"{CONFIG.microservices.thanos_api_url}/platform",
        "loki": f"{CONFIG.microservices.loki_api_url}",
        "black-widow": f"{CONFIG.microservices.black_widow_api_url}/v1",
        "rocket": f"{CONFIG.microservices.rocket_api_url}",
        "hulk": f"{CONFIG.microservices.hulk_api_url}/api/v1",
    }

    return mappings[service]


def is_url_https(service: ServiceNameT) -> bool:

    service_url = get_url(service)

    return service_url.startswith("https")


def init(
    username: Optional[str] = None,
    password: Optional[str] = None,
    downloads_path: str = "/tmp/evoml-client",
    base_url: str = None,
) -> bool:
    """
    username & password - platform username and password - if not specified will
    try to load from EVOML_USER & EVOML_PASSWORD env vars
    environment - either: release, dev or beast4
    downloads_path - where to save downloaded model pipelines, default = /tmp/evoml-client/models
    """
    global CONFIG
    global DOWNLOAD_PATH
    DOWNLOAD_PATH = downloads_path

    environment_url = base_url or conf_mgr.client_conf.BASE_URL

    if not environment_url:
        raise ValueError("You need to either provide the base_url argument or set the BASE_URL env parameter.")

    username = username or conf_mgr.client_conf.USERNAME
    password = password or conf_mgr.client_conf.PASSWORD
    if not username or not password:
        raise ValueError("You need to provide username and password.")

    raw_config = request_raw_config(environment_url)
    CONFIG = environment_conf_factory(environment_url, raw_config)

    url = get_url("enigma")
    auth_url = f"{url}/auth/login"

    login_result = requests.post(
        url=auth_url,
        json={
            "client_id": CONFIG.auth.client_id,
            "client_secret": CONFIG.auth.client_secret,
            "grant_type": "password",
            "username": username,
            "password": password,
        },
        verify=is_url_https("enigma") if not base_url else True,
        timeout=REQUEST_TIMEOUT,
    )
    if login_result.status_code == 200:
        login_json = login_result.json()
    else:
        return False
    global AUTH_HEADER
    AUTH_HEADER = {"Authorization": "Bearer " + login_json["access_token"]}

    return True


def get_process_info(process_id: str) -> ProcessInfo:
    """Get all info on a given process ID held by enigma"""
    result = requests.get(
        url=f"{get_url('enigma')}/processes/{process_id}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(result, 200)
    return ProcessInfo(**result.json())


def get_trial_pipelines(trial_id: str) -> List[Pipeline]:
    """Gets all pipelines for a given trial id

    Args:
        trial_id (str): The trial id

    Returns:
        List[Pipeline]: The list of pipelines
    """
    response = requests.get(
        url=f"{get_url('enigma')}/trials/{trial_id}?populate=pipelines&select=pipelines",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)

    return [Pipeline(**data) for data in response.json()["pipelines"] or []]


def get_trial_pipeline_by_id(optimization_id: str, pipeline_id: str) -> Pipeline:
    """Gets a specific pipeline by its id for a given trial id

    Args:
        optimization_id (str): The optimization id on bw
        pipeline_id (str): The pipeline id

    Returns:
        Pipeline: The detail of the pipeline
    """
    response = requests.get(
        url=f"{get_url('black-widow')}/optimization/{optimization_id}/pipelines",
        headers=get_auth(),
        verify=is_url_https("black-widow"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)

    pipelines: List[Pipeline] = [Pipeline(**data) for data in response.json()["pipelines"] or []]
    pipeline: Pipeline = [x for x in pipelines if x.id == pipeline_id][0]

    return pipeline


def get_task_status(task_id: str) -> dict:
    status = requests.get(
        url=f"{get_url('loki')}/tasks/{task_id}/status",
        headers=get_auth(),
        verify=is_url_https("loki"),
        timeout=REQUEST_TIMEOUT,
    ).json()
    return status


def poll_status(process_id: str, timeout: int, standoff: int, interval_limit: int = 30) -> bool:
    """
    Blocking. poll a process until complete with an increasing
    standoff time to avoid spamming.
    """
    TERMINAL_STATES = [Status.SUCCESS, Status.FAILED, Status.CANCELLED]

    interval = 4
    total = 0
    while True:
        if total > timeout:
            return False
        process = get_process_info(process_id)
        if process.status in TERMINAL_STATES:
            return process.status == Status.SUCCESS
        sleep(interval)
        total += interval
        if interval < interval_limit:
            interval += standoff


def poll_status_task(task_id: str, timeout: int, standoff: int) -> bool:
    """
    Blocking. poll a process until complete with an increasing
    standoff time to avoid spamming.
    """
    TERMINAL_STATES = [Status.SUCCESS, Status.FAILED, Status.CANCELLED]

    interval = 4
    total = 0
    task = get_task_status(task_id)
    while total < timeout and task["status"] not in TERMINAL_STATES:
        task = get_task_status(task_id)
        sleep(interval)
        total += interval
        interval += standoff

    return get_task_status(task_id)["status"] == Status.SUCCESS


# ─────────────────────────────── File Helpers ─────────────────────────────── #
def get_file_infos(endpoint: str, file_id: str) -> Dict:
    """Get all info held by the file api on a given file"""
    response = requests.get(
        url=f"{get_url('file-api')}/{endpoint}/{file_id}",
        headers=get_auth(),
        verify=is_url_https("file-api"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()


def get_file_size(endpoint: str, file_id: str) -> int:
    """Get the size of a file represented by a file id"""
    file_infos = get_file_infos(endpoint, file_id)
    return file_infos.get("sizeInBytes")


def download_file(endpoint: str, file_id: str, target_path: Path) -> Path:
    """
    Download a file from the file api to a target location.
    Returns location of resulting file
    """
    return download_file_auth(endpoint=endpoint, file_id=file_id, auth=get_auth(), target_path=target_path)


def download_file_auth(endpoint: str, file_id: str, auth: Dict, target_path: Path) -> Path:
    """
    Download a file from the file api to a target location.
    Returns location of resulting file
    """
    response = requests.get(
        url=f"{get_url('file-api')}/{endpoint}/{file_id}/download?type=parquet",
        headers=auth,
        verify=is_url_https("file-api"),
        stream=True,
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    bytes_size = get_file_size(endpoint, file_id)
    with target_path.open("wb") as fobj:
        if bytes_size is not None:
            total_length = int(response.headers.get("Content-Length", bytes_size))
            iterator = tqdm(
                response.iter_content(chunk_size=1024),
                total=int((total_length / 1024) + 1),
                unit="kb",
                unit_divisor=1024,
            )
        else:
            iterator = response.iter_content(chunk_size=1024)
        for chunk in iterator:
            if chunk:
                fobj.write(chunk)
                fobj.flush()
    return target_path


def upload_file(endpoint: str, local_path: Path) -> Response:
    response = requests.post(
        url=f"{get_url('file-api')}/{endpoint}",
        files={"file": (local_path.name, open(local_path, "rb"))},
        headers=get_auth(),
        verify=is_url_https("file-api"),
        timeout=REQUEST_TIMEOUT,
    )
    return response


def check_file_hash(target: Path, known_md5: str) -> bool:
    """Not Yet Implemented"""
    # TODO: Check the hash of the file against file apis hash
    # Currently hash is 'minioFilename' in /files/{file_id}
    return True


# ─────────────────────────── Library wide getters ─────────────────────────── #
def get_auth() -> Dict[str, str]:
    """Expose the auth header for repeat use"""
    global AUTH_HEADER
    return AUTH_HEADER


def download_path() -> str:
    """Expose the target download path for repeat use"""
    global DOWNLOAD_PATH
    return DOWNLOAD_PATH


# ───────────────────────────── Request wrapping ───────────────────────────── #


def _request(
    method: HttpMethod,
    url: str,
    valid_response: List[int],
    retry_policy: RetryPolicy = None,
    json: dict = None,
    params: dict = None,
) -> Response:
    """Wraps web request logic to provide a more robust client"""
    tries = 0
    session = Session()
    request = Request(method=method, url=url, headers=get_auth(), json=json, params=params)
    prepared = session.prepare_request(request)
    response = session.send(prepared)
    tries += 1
    while response.status_code in [500, 502, 504, 507, 429, 425, 408] and tries < retry_policy.max_retry:
        print(f"request failed with {response.status_code}. Retrying in " f"{retry_policy.backoff * tries}s")
        sleep(retry_policy.backoff * tries)
        session.send(prepared)
    check_status_code(response, valid_response)
    return response


def post(
    url: str,
    payload: dict = None,
    json: dict = None,
    expected_codes: List[int] = None,
):
    """Wraps post method for request"""
    expected_codes = [201] if expected_codes is None else expected_codes
    return _request(
        method=HttpMethod("post"),
        url=url,
        valid_response=expected_codes,
        params=payload,
        json=json,
    )


def get(
    url: str,
    payload: dict = None,
    json: dict = None,
    expected_codes: List[int] = None,
):
    """Wraps get method for request"""
    expected_codes = [200] if expected_codes is None else expected_codes
    return _request(
        method=HttpMethod("get"),
        url=url,
        valid_response=expected_codes,
        params=payload,
        json=json,
    )


def put(
    url: str,
    payload: dict = None,
    json: dict = None,
    expected_codes: List[int] = None,
):
    """Wraps put method for request"""
    expected_codes = [201] if expected_codes is None else expected_codes
    return _request(
        method=HttpMethod("put"),
        url=url,
        valid_response=expected_codes,
        params=payload,
        json=json,
    )


def patch(
    url: str,
    payload: dict = None,
    json: dict = None,
    expected_codes: List[int] = None,
):
    """Wraps patch method for request"""
    expected_codes = [200] if expected_codes is None else expected_codes
    return _request(
        method=HttpMethod("patch"),
        url=url,
        valid_response=expected_codes,
        params=payload,
        json=json,
    )


def delete(
    url: str,
    payload: dict = None,
    json: dict = None,
    expected_codes: List[int] = None,
):
    """Wraps delete method for request"""
    expected_codes = [200] if expected_codes is None else expected_codes
    return _request(
        method=HttpMethod("delete"),
        url=url,
        valid_response=expected_codes,
        params=payload,
        json=json,
    )


# ────────────────────────────── Request models ────────────────────────────── #


class ClientProtocol(str, Enum):
    """Enum of supported protocols"""

    https = "https"
    http = "http"


class HttpMethod(str, Enum):
    """Enum of HTTP methods"""

    post = "post"
    get = "get"
    put = "put"
    patch = "patch"
    delete = "delete"


@dataclass
class RetryPolicy:
    """
    Number of times to retry and number of seconds to increase wait between
    requests each retry
    """

    max_retry: int = 5
    backoff: int = 1
