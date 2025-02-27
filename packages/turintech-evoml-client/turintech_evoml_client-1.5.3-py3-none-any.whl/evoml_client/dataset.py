# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

import mimetypes
from typing import List, Union, Optional
from enum import Enum
from pathlib import Path

import pandas as pd
import numpy as np

from evoml_client.api_calls import (
    dataset_get,
    dataset_post,
    get_url,
    poll_status,
    StatusCodeException,
    HulkConnectionInfo,
    upload_from_sql,
    dataset_from_file_id,
    get_analysis_info,
    AnalysisType,
)


# ──────────────────────────────────────────────────────────────────────────── #


class DatasetState(Enum):
    OFFLINE = 0
    ONLINE = 1


# ──────────────────────────────── Exceptions ──────────────────────────────── #
class IncompatibleDatasetState(Exception):
    def __init__(self, state: DatasetState, required: List[DatasetState], operation: str):
        super().__init__(
            f"Dataset is in incorrect state for this operation - "
            f"Dataset is {state}, must be in {required} to {operation}"
        )


class Dataset:
    """
    States:
        OFFLINE -- url and dataset_id are not initialised, interactive config step\n
        ONLINE -- mirror of platform entry\n
    Properties:
        url -- url to access dataset on the platform\n
        dataset_id -- id of the dataset on the platform\n
        analysis_id -- process id for the analysis of the dataset\n
        data -- pandas dataframe of the the raw data\n
    Actions:
        init(Raw) -- create Dataset in OFFLINE\n
        init(URL) -- create Dataset in ONLINE\n
        init(ID) -- create Dataset in ONLINE\n
        put() -- transition from OFFLINE to ONLINE\n
        fetch() -- transition from ONLINE to ONLINE\n
        to_X() -- if ONLINE ---> download dataset ---> return in required format
               -- if OFFLINE --> return dataset in required format\n
        get_state() -- if URL None then OFFLINE else ONLINE\n
    """

    # ──────────────────────────── Constructors ────────────────────────────── #
    def __init__(self):
        self.url: str = None
        self.dataset_id: str = None
        self.analysis_id: str = None
        self.name: str = None
        self.desc: str = None
        self.data: pd.DataFrame = None
        self.tags: List[str] = None
        self.analysis_type: Optional[AnalysisType] = None

    @classmethod
    def from_file(
        cls,
        fname: Union[Path, str],  # Must contain file type in form of suffix
        name: str = None,
        desc: str = None,
        tags: List[str] = None,
    ) -> Dataset:
        """
        Build a dataset object from a given: csv, zip, or parquet file path,
        along with name and description. File type is detected from extension,
        errors will occur if the extension doesn't match the underlying data
        """
        dataset = cls()
        target_file = Path(fname) if isinstance(fname, str) else fname
        file_type = mimetypes.guess_type(target_file, strict=True)
        if file_type[0] == "text/csv":
            dataset.data = pd.read_csv(filepath_or_buffer=target_file)
        elif file_type[0] == "application/zip":
            dataset.data = pd.read_csv(filepath_or_buffer=target_file, compression="zip")
        elif file_type[0] is None and file_type[1] == "xz":
            dataset.data = pd.read_csv(filepath_or_buffer=target_file, compression="xz")
        elif file_type[0] is None and file_type[1] == "gzip":
            dataset.data = pd.read_csv(filepath_or_buffer=target_file, compression="gzip")
        elif file_type[0] is None and target_file.suffix == ".parquet":
            dataset.data = pd.read_parquet(path=target_file)
        dataset.name = target_file.name.replace(target_file.suffix, "") if name is None else name
        dataset.desc = "" if desc is None else desc
        dataset.tags = tags
        return dataset

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame,
        name: str,
        desc: str = "",
        tags: List[str] = None,
    ) -> Dataset:
        """
        Build a dataset object from a given pandas dataframe, along with
        name and description. The dataframe should have column names set
        """
        dataset = cls()
        dataset.data = cls().data = data
        dataset.name = name.replace(" ", "_")
        dataset.desc = desc
        dataset.tags = tags
        return dataset

    @classmethod
    def from_numpy(
        cls,
        data: np.ndarray,
        name: str,
        desc: str = "",
        tags: List[str] = None,
    ) -> Dataset:
        """
        Build a dataset object from a given numpy array, along with
        name and description.
        """
        dataset = cls()
        data_width = 1 if data.ndim == 1 else data.shape[1]
        dataset.data = pd.DataFrame(data=data, columns=[f"col{i}" for i in range(data_width)])
        dataset.name = name.replace(" ", "_")
        dataset.desc = desc
        dataset.tags = tags
        return dataset

    @classmethod
    def from_numpy_xy(
        cls,
        data_x: np.ndarray,
        data_y: np.ndarray,
        name: str,
        desc: str = "",
        tags: List[str] = None,
    ) -> Dataset:
        """
        Build a dataset object from 2 numpy arrays, along with
        name and description. data_y will then be exposed as the final
        column of the dataset
        """
        y_width = 1 if data_y.ndim == 1 else data_y.shape[1]
        data = np.concatenate(
            (
                data_x,
                np.reshape(data_y, (data_y.shape[0], y_width)),
            ),
            axis=1,
        )
        return cls.from_numpy(data=data, name=name, desc=desc, tags=tags)

    @classmethod
    def from_pandas_x_y(
        cls,
        data_x: pd.DataFrame,
        data_y: pd.Series,
        name: str,
        desc: str = "",
        tags: List[str] = None,
    ) -> Dataset:
        """
        Build a dataset object from a dataframe and series, along with
        name and description. data_y will then be exposed as the final
        column of the dataset
        """
        data = pd.concat([data_x, data_y], axis=1)
        return cls.from_pandas(data=data, name=name, desc=desc, tags=tags)

    @classmethod
    def from_url(cls, url: str) -> Dataset:
        """
        Get a local representation of a dataset on the platform
        given a url ending /datasets/view/id - the url must point
        to the same environment set when initialising the client.
        Reinitialise if necessary before calling.
        """
        dataset = cls()
        if url.split("/")[-3:-1] == ["datasets", "view"]:
            dataset.url = url  # URL expected to be /datasets/view/id
        else:
            raise ValueError(f"{url} is invalid - must be <Platform>/datasets/view/<ID>")
        dataset.dataset_id = dataset.url.split("/")[-1]
        dataset.fetch()
        return dataset

    @classmethod
    def from_id(cls, dataset_id: str) -> Dataset:
        """
        Get a local representation of a dataset on the platform
        given an ID from the same environment as the one set with
        the most recent initialisation of the client.
        """
        dataset = cls()
        dataset.dataset_id = dataset_id
        dataset.url = f"{get_url('platform')}/datasets/view/{dataset_id}"
        try:
            dataset.fetch()
        except StatusCodeException as err:
            raise ValueError(f"{dataset_id} is not a valid dataset ID or connection failed: {str(err)}")
        return dataset

    @classmethod
    def from_db(
        cls,
        connection_info: HulkConnectionInfo,
        table: str,
        name: str,
        desc: str = "",
        tags: List[str] = None,
    ) -> Dataset:
        """
        Given a hulk connection configuration and a target table name
        create a dataset on the platform and form a local representation
        """
        tags = [] if tags is None else tags
        dataset = cls()
        file_id, file_info = upload_from_sql(connection_info=connection_info, table=table)
        raw_response = dataset_from_file_id(
            name=name,
            file_id=file_id,
            file_info=file_info,
            description=desc,
            tags=tags,
        )
        dataset.dataset_id = raw_response["_id"]
        dataset.url = f"{get_url('platform')}/datasets/view/{raw_response['_id']}"
        dataset.name = name
        dataset.desc = desc
        return dataset

    # ──────────────────────── Platform Interactions ───────────────────────── #
    def put(self) -> bool:
        """
        Upload the dataset to the platform, move from OFFLINE to ONLINE
        """
        valid_states = [DatasetState.OFFLINE]
        if self.get_state() not in valid_states:
            raise IncompatibleDatasetState(self.get_state(), valid_states, "put")
        result = dataset_post(
            self.name,
            self.desc,
            self.data,
            self.tags or ["evoml-client"],
        )
        self.analysis_id = result["analysisProcessId"]
        self.dataset_id = result["_id"]
        self.url = f"{get_url('platform')}/datasets/view/{self.dataset_id}"
        return True  # If the API was happy

    def fetch(self) -> None:
        """
        Retrieve the dataset from the platform, use when the name or similar
        has been changed on the platform
        """
        valid_states = [DatasetState.ONLINE]
        if self.get_state() not in valid_states:
            raise IncompatibleDatasetState(self.get_state(), valid_states, "get")
        result = dataset_get(self.dataset_id)
        self.data = pd.read_parquet(result["ds_path"])
        self.desc = result["response_json"]["description"]
        self.name = result["response_json"]["name"]
        self.analysis_id: str = result["response_json"]["analysisProcessId"]

    def wait(self, timeout: int = -1) -> bool:
        """
        Blocking call, to wait until the analysis of the dataset is
        complete and trials are allowed to be run against the dataset
        """
        valid_states = [DatasetState.ONLINE]
        if self.get_state() not in valid_states:
            raise IncompatibleDatasetState(self.get_state(), valid_states, "wait")
        if self.analysis_id is None:
            self.analysis_id, self.analysis_type = get_analysis_info(self.dataset_id)
        if timeout == -1:
            return poll_status(self.analysis_id, 2**63, 2)
        return poll_status(self.analysis_id, timeout, 2)

    # ──────────────────────── Data Extraction ─────────────────────────────── #
    # Mike: add file type to not export to csv by default
    def to_file(self, path: Union[str, Path]) -> None:
        """Save the contained data to a csv file at the target location"""
        if self.get_state() == DatasetState.ONLINE:
            self.fetch()
        self.data.to_csv(path, index=False)

    def to_numpy(self) -> np.ndarray:
        """Returns the dataset in the form of a numpy array"""
        if self.get_state() == DatasetState.ONLINE:
            self.fetch()
        return self.data.to_numpy()

    def to_pandas(self) -> pd.DataFrame:
        """Returns the dataset in the form of a pandas dataframe"""
        if self.get_state() == DatasetState.ONLINE:
            self.fetch()
        return self.data

    # ──────────────────────── State Management ────────────────────────────── #
    def get_state(self) -> DatasetState:
        if self.url is None:
            return DatasetState.OFFLINE
        return DatasetState.ONLINE

    # ──────────────────────────────── Helpers ─────────────────────────────── #
    def _find_column_by_name(self, column_name: str) -> int:
        try:
            target_col = self.data.columns.get_loc(column_name)
        except KeyError as err:
            raise KeyError(
                f"{column_name} could not be found in {self.name}\n" f"{self.name} columns are {self.data.columns}"
            )
        return target_col
