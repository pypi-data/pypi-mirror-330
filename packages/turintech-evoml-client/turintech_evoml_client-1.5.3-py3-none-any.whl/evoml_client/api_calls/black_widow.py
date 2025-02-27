# ───────────────────────────────── imports ────────────────────────────────── #
from typing import Optional

import requests

from evoml_client.api_calls.utils import get_auth, check_status_code, get_url, is_url_https, REQUEST_TIMEOUT


# ──────────────────────────────────────────────────────────────────────────── #


def trial_id_to_optimization_id(trial_id: str) -> Optional[str]:
    """
    Maps a thanos Trial ID to the latest Black Widow Optimization ID
    associated to it.
    """
    service_url = get_url(service="black-widow")
    target_url = f"{service_url}/legacy/trials/{trial_id}/optimization"
    response = requests.get(
        url=target_url, headers=get_auth(), verify=is_url_https("black-widow"), timeout=REQUEST_TIMEOUT
    )
    check_status_code(response, 200)

    return response.json().get("optimizationId", None)
