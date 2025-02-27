# ───────────────────────────────── imports ────────────────────────────────── #
import os
import uuid
from enum import Enum
from typing import List, Dict, Tuple, Optional
from pathlib import Path

import pandas as pd
import requests

from evoml_client.api_calls.utils import (
    get_auth,
    check_status_code,
    get_url,
    download_file,
    download_path,
    upload_file,
    is_url_https,
    REQUEST_TIMEOUT,
)


# ───────────────────────────── Dataset Handling ───────────────────────────── #


def dataset_post(name: str, description: str, data: pd.DataFrame, tags: List[str]) -> Dict:
    """
    Upload a given dataframe to the env, targeted by the last init
    of the client
    """
    file_id, file_info = upload_dataframe(name, data)
    return dataset_from_file_id(
        name=name,
        description=description,
        tags=tags,
        file_id=file_id,
        file_info=file_info,
    )


def dataset_from_file_id(name: str, description: str, tags: List[str], file_id: str, file_info: dict) -> Dict:
    tag_ids = [find_dataset_tag(tag) for tag in tags]
    request_json = {
        "name": name,
        "fileId": file_id,
        "metadata": {
            "isTimeseries": False,
            "indexingColumnIndex": None,
            "columnsCount": int(file_info["totalColumns"]),
            "rowsCount": int(file_info["totalRows"]),
        },
        "description": description,
        "tags": tag_ids,
    }
    response = requests.post(
        url=f"{get_url('enigma')}/datasets",
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 201)
    return response.json()


def dataset_get(dataset_id: str) -> Dict:
    """
    Given an ID on the same env as that targeted by the last client init, get
    the most recent version in  the form of a csv file
    """
    response = requests.get(
        url=f"{get_url('enigma')}/datasets/{dataset_id}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    # file_type = get_file_type(file_id=response.json()["fileId"])
    target = Path(
        download_path(),
        "datasets",
        f"{response.json()['name']}_{response.json()['_id']}",
    )
    if not target.exists():
        ds_path = download_dataset(
            response.json()["fileId"],
            response.json()["name"],
            response.json()["_id"],
        )
    else:
        ds_path = target
    result = {"ds_path": ds_path, "response_json": response.json()}
    return result


# ─────────────────────────────── File Handling ────────────────────────────── #
def upload_dataframe(name: str, data_frame: pd.DataFrame) -> Tuple[str, dict]:
    """Send the given data fram the pandas datafram to the fileAPI"""
    temp_location = Path(f"/tmp/{name}-{uuid.uuid4()}.parquet")
    data_frame.to_parquet(temp_location, index=False)
    response = upload_file("datasets", temp_location)
    check_status_code(response, 201)
    temp_location.unlink()
    file_id = response.json()["_id"]
    return file_id, response.json()["analysis"]


def download_dataset(file_id: str, dataset_name: str, dataset_id: str) -> Path:
    """Download the dataset given a dataset ID and name along with fileAPI file id"""
    temp_path = Path(download_path(), "datasets", f"{dataset_name}_{dataset_id}")
    if not Path(download_path(), "datasets").exists():
        os.makedirs(Path(download_path(), "datasets"))
    response = download_file("datasets", file_id, temp_path)
    return response


# ────────────────────────────────── Helpers ───────────────────────────────── #


class AnalysisType(str, Enum):
    SAMPLE = "sample"
    FULL = "full"


def get_file_type(file_id: str) -> str:
    file_type_url = f"{get_url('file-api')}/datasets/{file_id}"
    file_type = requests.get(
        url=file_type_url,
        headers=get_auth(),
        verify=is_url_https("file-api"),
        stream=True,
        timeout=REQUEST_TIMEOUT,
    ).json()["analysis"]["originalType"]
    return file_type


def get_analysis_info(full_data_id: str) -> Tuple[str, AnalysisType]:
    """
    Gets the process ID and type of the initial analysis for a dataset, if
    dataset is big it'll be for a sample, else it'll be for the whole thing
    """
    params = {"populate": "sample"}
    response = requests.get(
        url=f"{get_url('enigma')}/datasets/{full_data_id}",
        headers=get_auth(),
        params=params,
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code != 200:
        return None
    response_data = response.json()
    if response_data["analysisProcessId"] is not None:
        return (response_data["analysisProcessId"], AnalysisType.FULL)
    elif response_data["sample"] is not None:
        return (response_data["sample"]["analysisProcessId"], AnalysisType.SAMPLE)
    return None


def get_sample_id(full_data_id: str) -> Optional[str]:
    """Gets the ID of the sample on which analysis has been called"""
    params = {"populate": "sample._id"}
    response = requests.get(
        url=f"{get_url('enigma')}/datasets/{full_data_id}",
        headers=get_auth(),
        params=params,
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code != 200:
        return None
    response_data = response.json()
    if response_data["sample"] is None:
        return None
    sample_id = response_data["sample"]["_id"]
    return sample_id


def get_data_info(dataset_id: str) -> List:
    """Gather info on all columns in a dataset."""
    column_infos = []
    sample_id = get_sample_id(dataset_id)
    if sample_id is None:
        response = requests.get(
            url=f"{get_url('enigma')}/datasets/{dataset_id}/columns-info",
            headers=get_auth(),
            verify=is_url_https("enigma"),
            timeout=REQUEST_TIMEOUT,
        )
    else:
        response = requests.get(
            url=f"{get_url('enigma')}/datasets/{sample_id}/columns-info",
            headers=get_auth(),
            verify=is_url_https("enigma"),
            timeout=REQUEST_TIMEOUT,
        )
    check_status_code(response, 200)
    column_infos += response.json()["docs"]
    page = 2
    while response.json()["hasNextPage"]:
        response = requests.get(
            url=f"{get_url('enigma')}/datasets/{dataset_id}/columns-info",
            headers=get_auth(),
            params={"page": page},
            verify=is_url_https("enigma"),
            timeout=REQUEST_TIMEOUT,
        )
        column_infos += response.json()["docs"]
        page += 1
    return column_infos


def col_index_to_id(dataset_id: str, column_index: int) -> str:
    """Get the unique column ID from the column index and the Dataset ID"""
    response = requests.get(
        url=f"{get_url('enigma')}/datasets/{dataset_id}/columns-info/{column_index}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()["_id"]


def find_dataset_tag(tag_name: str) -> str:
    """Convert human readable tag name to a tag_id"""
    response = requests.get(
        url=f"{get_url('enigma')}/datasets-tags?name={tag_name}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    response = response.json()
    if len(response["docs"]) > 0:
        return response["docs"][0]["_id"]
    response = requests.post(
        url=f"{get_url('enigma')}/datasets-tags",
        json={"name": tag_name},
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    return response.json()["_id"]


def get_file_id(dataset_id: str) -> str:
    """Returns the Thor file ID that maps to the dataset ID"""
    response = requests.get(
        url=f"{get_url('enigma')}/datasets/{dataset_id}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()["fileId"]


# ────────────────────────────── Graph Handling ────────────────────────────── #
def get_correlations(dataset_id: str, correlation_type: str) -> Dict:
    """DO NOT USE"""
    # Use: /api/datasets/{dataset_id}/columns-info/correlations
    # What can correlation_type be?
    request_json = {
        "correlationType": correlation_type,
        "correlationFields": [{"name": "string", "values": [0]}],
    }
    response = requests.post(
        url=f"{get_url('enigma')}/datasets/{dataset_id}/columns-info/correlations",
        json=request_json,
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 401)
    return response.json()


def get_graph(graph_id: str) -> Dict:
    """Get the graph json for a given graph ID - Likely broken by JIT graph gen"""
    response = requests.get(
        url=f"{get_url('enigma')}/graphs/{graph_id}",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()


def gen_multi_cols(dataset_id: str, column_pairs: List[Tuple[int]] = None) -> List:
    """
    Get the graphs for the given interesting column pairs.
    Likely broken by JIT graph gen
    """
    if column_pairs is None:
        response = requests.get(
            url=f"{get_url('enigma')}/datasets/{dataset_id}/multi-column-graphs-pairs",
            headers=get_auth(),
            verify=is_url_https("enigma"),
            timeout=REQUEST_TIMEOUT,
        )
        check_status_code(response, 200)
        interesting_columns = [
            [pair["featureOne"]["_id"], pair["featureTwo"]["_id"]] for pair in response.json()["pairs"]
        ]
    else:
        interesting_columns = [[col_index_to_id(dataset_id, indx) for indx in pair] for pair in column_pairs]

    responses = [
        requests.post(
            url=f"{get_url('enigma')}/multi-column-graphs",
            json={"datasetId": dataset_id, "columnIds": list(target_pair)},
            headers=get_auth(),
            verify=is_url_https("enigma"),
            timeout=REQUEST_TIMEOUT,
        )
        for target_pair in interesting_columns
    ]
    multi_col_ids = []
    for response in responses:
        check_status_code(response, 201)
        multi_col_ids.append(response.json()["_id"])
    return multi_col_ids


def get_multi_col_graphs(multi_col_id: str) -> dict:
    """
    Given a multicol graph id, return the graph JSON.
    Likely broken by JIT graph gen
    """
    response = requests.get(
        url=f"{get_url('enigma')}/multi-column-graphs/{multi_col_id}/graphs",
        headers=get_auth(),
        verify=is_url_https("enigma"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()
