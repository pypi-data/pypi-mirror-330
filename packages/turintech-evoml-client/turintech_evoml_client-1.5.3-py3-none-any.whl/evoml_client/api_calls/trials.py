# ───────────────────────────────── imports ────────────────────────────────── #
from typing import List, Dict
import requests

from evoml_client.api_calls.utils import get_auth, check_status_code, get_url, is_url_https, REQUEST_TIMEOUT


# ──────────────────────────────────────────────────────────────────────────── #


# ────────────────────────────── Logging Config ────────────────────────────── #
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter("[%(levelname)s] %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel()


# ────────────────────────── Trial Manipulation ────────────────────────────── #
def trial_post(name: str, dataset_id: str, target_col: int, config: Dict, tags: List[str]) -> Dict:
    """Upload a trial to the platform without starting"""
    tag_ids = [find_trial_tag(tag) for tag in tags]
    request_json = {
        "datasetId": dataset_id,
        "options": config,
        "columnIndex": target_col,
        "name": name,
        "tags": tag_ids,
    }
    response = requests.post(
        url=f"{get_url('enigma')}/trials",
        headers=get_auth(),
        json=request_json,
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 201)
    return response.json()


def trial_get(trial_id: str) -> Dict:
    """Get all info on a trial on the platform"""
    response = requests.get(
        url=f"{get_url('enigma')}/trials/{trial_id}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()


def trial_start(trial_id: str) -> Dict:
    """Trigger the start of an optimization trial"""
    response = requests.post(
        url=f"{get_url('enigma')}/trials/{trial_id}/optimization",
        headers=get_auth(),
        json={"deployModel": False},
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 201)  # the docs lied - they say 200
    return response.json()


# ───────────────────────────────── Helpers ────────────────────────────────── #
def find_trial_tag(tag_name: str) -> str:
    """Convert human readable tag name to a tag_id"""
    response = requests.get(
        url=f"{get_url('enigma')}/trials-tags?name={tag_name}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    response = response.json()
    if len(response["docs"]) > 0:
        return response["docs"][0]["_id"]
    response = requests.post(
        url=f"{get_url('enigma')}/trials-tags",
        json={"name": tag_name},
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    return response.json()["_id"]


def find_loss_func(func_name: str, ml_task: str) -> str:
    """Convert human readable loss function into a loss func ID"""
    loss_funcs = []
    response = requests.get(
        url=f"{get_url('enigma')}/loss-functions",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    loss_funcs += response.json()["docs"]
    page = 2
    while response.json()["hasNextPage"]:
        response = requests.get(
            url=f"{get_url('enigma')}/loss-functions",
            headers=get_auth(),
            params={"page": page},
            verify=is_url_https("enigma"),
            timeout=REQUEST_TIMEOUT,
        )
        loss_funcs += response.json()["docs"]
        page = response.json()["nextPage"]
    search = lambda loss_func: (func_name in (loss_func["name"], loss_func["slug"])) and loss_func["mlTask"] == ml_task
    result = list(filter(search, loss_funcs))
    if len(result) == 0:
        raise Exception("no such loss function")
    return result[0]["_id"]


def get_loss_funcs(ml_task: str) -> List:
    """Return list of usable loss functions for a given ML task"""
    loss_funcs = []
    response = requests.get(
        url=f"{get_url('enigma')}/loss-functions",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    loss_funcs += response.json()["docs"]
    page = 2
    while response.json()["hasNextPage"]:
        response = requests.get(
            # get_url=f"http://enigma.westeurope.cloudapp.azure.com:8080/api/loss-functions",
            url=f"{get_url('enigma')}/loss-functions",
            headers=get_auth(),
            params={"page": page},
            verify=is_url_https("enigma"),
            timeout=REQUEST_TIMEOUT,
        )
        loss_funcs += response.json()["docs"]
        page += 1
    search = lambda loss_func: loss_func["mlTask"] == ml_task
    loss_funcs = list(filter(search, loss_funcs))
    return loss_funcs


def find_encoder(): ...


def get_encoders(): ...


def find_scalers(): ...


def get_scalers(): ...
