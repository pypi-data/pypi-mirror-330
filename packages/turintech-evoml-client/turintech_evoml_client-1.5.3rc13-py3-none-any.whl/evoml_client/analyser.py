# ───────────────────────────────── imports ────────────────────────────────── #
from typing import List, Dict, Tuple

from evoml_client.dataset import Dataset, DatasetState
from evoml_client.api_calls.datasets import (
    get_data_info,
    gen_multi_cols,
    get_graph,
    get_multi_col_graphs,
)


# ──────────────────────────────────────────────────────────────────────────── #


class Analyser:
    """
    Actions:
        get_stats(Dataset)        -- return stats from the platform\n
        get_graphs(Dataset)       -- return graphs from the platform (NYI)\n
        get_multi_graphs(Dataset) -- return multi graphs from the platform (NYI)\n
    """

    def get_stats(self, dataset: Dataset) -> Dict:
        if dataset.get_state() is DatasetState.OFFLINE:
            dataset.put()
        dataset.wait()
        result = get_data_info(dataset.dataset_id)
        dataset_stats = {
            col["columnIndex"]: {
                **{
                    "column_name": col["name"],
                    "detected_type": col["detectedType"],
                    "unique_values_ratio": col["statsUniqueValuesRatio"],
                    "unique_values_count": col["statsUniqueValuesCount"],
                    "missing_values_ratio": col["statsMissingValuesRatio"],
                    "missing_values_count": col["statsMissingValuesCount"],
                },
                **{stat["name"]: stat["value"] for stat in col["statistics"]},
            }
            for col in result
        }
        return dataset_stats

    def get_graphs(self, dataset: Dataset) -> Dict:
        """NYI"""
        if dataset.get_state() is DatasetState.OFFLINE:
            dataset.put()
        dataset.wait()
        result = get_data_info(dataset.dataset_id)
        dataset_graphs = {
            col["columnIndex"]: {
                "column_name": col["name"],
                "detected_type": col["detectedType"],
                "graphs": [
                    {
                        "type": get_graph(graph_id)["type"],
                        "data": get_graph(graph_id)["data"],
                    }
                    for graph_id in col["graphIds"]
                ],
            }
            for col in result
        }
        return dataset_graphs

    def get_multi_graphs(self, dataset: Dataset, col_pairs: List[Tuple[int]] = None) -> List:
        """NYI"""
        if dataset.get_state() is DatasetState.OFFLINE:
            dataset.put()
        result = gen_multi_cols(dataset.dataset_id, col_pairs)
        target_graphs = []
        for mc_id in result:
            for graph in get_multi_col_graphs(mc_id)["graphs"]:
                target_graphs.append(
                    {
                        "column_pair": tuple(col["index"] for col in graph["context"]["columns"]),
                        "type": graph["context"]["generatedBy"],
                        "format": graph["type"],
                        "data": graph["data"],
                    }
                )
        return target_graphs
