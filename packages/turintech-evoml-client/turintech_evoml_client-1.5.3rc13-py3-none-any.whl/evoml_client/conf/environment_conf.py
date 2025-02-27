import json
from typing import Any, Dict, Optional
from evoml_api_models import BaseModelWithAlias
from pydantic import root_validator
import requests

__all__ = ["EnvironmentConf", "request_raw_config", "environment_conf_factory"]


class OAuthClientConf(BaseModelWithAlias):
    client_id: str
    client_secret: str


class MicroservicesConf(BaseModelWithAlias):
    thanos_api_url: str
    thor_api_url: str
    tus_api_url: str
    hulk_api_url: str
    loki_api_url: str
    black_widow_api_url: str
    uppy_companion_host: str
    sockets_host: str
    rocket_api_url: str
    pipeline_deployer_api_url: str
    synthetic_data_generator_api_url: Optional[str] = None


class EcosystemConf(BaseModelWithAlias):
    environment: str


class FeaturesConf(BaseModelWithAlias):
    forecasting: Dict[str, Any]
    integrations: Dict[str, Any]
    pipeline_validation: Dict[str, Any]
    synthetic_data_generator_page: Dict[str, Any]


class EnvironmentConf(BaseModelWithAlias):
    base_url: str
    auth: OAuthClientConf
    microservices: MicroservicesConf
    ecosystem: EcosystemConf
    features: FeaturesConf

    @root_validator(pre=True)  # type: ignore
    @classmethod
    def sanitize_microservices_urls(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize the paylod for the microservices URLs.

        This method will convert the relative URLs to full URLs.
        """
        if "microservices" not in values:
            return values

        # URLs under the microservices can be either relative to the base_url or full URLs.
        # We need to make sure that they are all full URLs
        for microservice, url in values["microservices"].items():
            values["microservices"][microservice] = to_full_url(values["base_url"], url)

        return values


def environment_conf_factory(base_url: str, raw_config: str) -> EnvironmentConf:

    json_obj = json.loads(raw_config)

    # Add base_url to the json object
    json_obj["base_url"] = base_url

    environment = EnvironmentConf.parse_obj(json_obj)

    return environment


def to_full_url(base_url: str, url_or_path: str) -> str:
    """Conditionally convert a relative URL to a full URL."""

    is_full_url = url_or_path.startswith("http")
    normalized_base_url = strip_last_slash(base_url)

    return url_or_path if is_full_url else f"{normalized_base_url}{url_or_path}"


def strip_last_slash(url: str) -> str:
    """Strip the last slash from a URL."""

    return url[:-1] if url.endswith("/") else url


def request_raw_config(base_url: str) -> str:
    """Request the raw configuration from the server."""
    normalized_base_url = strip_last_slash(base_url)

    return requests.get(f"{normalized_base_url}/assets/environments/environment.json", timeout=30).text
