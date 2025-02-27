# ───────────────────────────────── imports ────────────────────────────────── #
import os
from pathlib import Path
from typing import Dict, List

import requests

from evoml_client.api_calls import get_data_info, get_file_type
from evoml_client.api_calls.utils import (
    get_auth,
    check_status_code,
    get_url,
    is_url_https,
    download_file,
    download_path,
    REQUEST_TIMEOUT,
)
from evoml_client.trial_conf_models import (
    ColumnFilter,
    Impute,
    TransformationOption,
    ColumnTransformationOptions,
    ColumnDetectedType,
    EncoderDetails,
    ScalerDetails,
    FeatureOverrides,
    column_type_mapping,
    MlTask,
)
from evoml_client.trial_conf_detection_types import AutoEncoder, EncoderType


# ──────────────────────────────────────────────────────────────────────────── #


# ────────────────────────────── Logging Config ────────────────────────────── #
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter("[%(levelname)s] %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel()


# ────────────────────────────────── Helpers ───────────────────────────────── #
def get_permitted_models(task: str) -> Dict:
    """Gets all models supported for a given ML task"""
    response = requests.get(
        url=f"{get_url('loki')}/processes/info/evoml/models/{task}",
        headers=get_auth(),
        verify=is_url_https("loki"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()


def get_algorithm_models(task: str) -> Dict:
    """Gets all algorithm models supported for a given ML task"""
    response = requests.get(
        url=f"{get_url('loki')}/ml-tasks/{task}/algorithm-models",
        headers=get_auth(),
        verify=is_url_https("loki"),
        timeout=REQUEST_TIMEOUT,
    )
    check_status_code(response, 200)
    return response.json()


# ─────────────────────────────── File Handling ────────────────────────────── #
def download_pipeline(pipeline_zip_id, model_name: str, pipeline_id: str) -> Path:
    """Downloads pipeline.zip for a given ML pipeline"""
    target_path = Path(
        download_path(),
        "models",
        f"{model_name}_{pipeline_id}.zip".replace("-", "_"),
    )
    if not Path(download_path(), "models").exists():
        os.makedirs(Path(download_path(), "models"))
    result = download_file("files", pipeline_zip_id, target_path)
    return result


def download_predictions(trial_id: str, model_id: str, task_id: str, file_id: str) -> Path:
    file_type = get_file_type(file_id=file_id)
    temp_path = Path(download_path(), "predictions", f"{trial_id}_{model_id}_{task_id}.{file_type}")
    if not Path(download_path(), "predictions").exists():
        os.makedirs(Path(download_path(), "predictions"))
    response = download_file("datasets", file_id, temp_path)
    return response


# ───────────────────────────────── Transformation Options ─────────────────────────────────────── #
def validate_column_detected_type_encoder(detected_type: str, encoder: EncoderType) -> bool:
    """Validates if the encoder is supported for the detected type"""
    return encoder in column_type_mapping[detected_type]


def get_encoder_slug_by_detected_type(
    detected_type_name: str,
    encoder_details: List[EncoderDetails] = None,
) -> List[str]:
    if encoder_details is None:
        encoder_details = []
    for encoder in encoder_details:
        if encoder.name == detected_type_name:
            encoder_slugs = []
            for encoder_type in encoder.type:
                if not validate_column_detected_type_encoder(detected_type_name, encoder_type):
                    raise ValueError(f"Encoder {encoder_type.value.slug} is not supported for {detected_type_name}")
                encoder_slugs.append(encoder_type.value.slug)
            return encoder_slugs
    return [AutoEncoder.AUTO.value.slug]


def get_scaler_slug_by_detected_type(
    detected_type_name: str,
    scaler_details: List[ScalerDetails] = None,
) -> List[str]:
    if scaler_details is None:
        scaler_details = []
    for scaler in scaler_details:
        if scaler.name == detected_type_name:
            return [x.value.slug for x in scaler.type]
    return ["auto"]


def get_feature_override(
    feature: FeatureOverrides,
) -> ColumnTransformationOptions:
    return ColumnTransformationOptions(
        columnIndex=feature.column_index,
        encoderSlugs={feature.encoder_details.name: [x.value.slug for x in feature.encoder_details.type]},
        scalerSlugs={feature.scaler_details.name: [x.value.slug for x in feature.scaler_details.type]},
        covariate=feature.covariate,
        filter=feature.filter,
        impute=Impute(strategy="auto"),
    )


def get_custom_transformation_options(
    dataset_id: str,
    encoder_details: List[EncoderDetails] = None,
    scaler_details: List[ScalerDetails] = None,
    feature_overrides: List[FeatureOverrides] = None,
    impute: Impute = None,
) -> List[TransformationOption]:
    column_info = get_data_info(dataset_id)
    transformation_options: List[TransformationOption] = []
    column_detected_types = set([x["detectedType"] for x in column_info])
    feature_overrides_input = {}
    if feature_overrides is not None:
        for feature in feature_overrides:
            feature_detected_type = [x for x in column_info if x["columnIndex"] == feature.column_index][0][
                "detectedType"
            ]
            if feature_detected_type not in feature_overrides_input:
                feature_overrides_input[feature_detected_type] = [feature]
            else:
                feature_overrides_input[feature_detected_type].append(feature)

    for column_type in column_detected_types:
        transformation_options.append(
            TransformationOption(
                detectedType=column_type,
                encoderSlugs={column_type: get_encoder_slug_by_detected_type(column_type, encoder_details)},
                scalerSlugs={column_type: get_scaler_slug_by_detected_type(column_type, scaler_details)},
                featureOverrides=(
                    [get_feature_override(x) for x in feature_overrides_input[column_type]]
                    if column_type in feature_overrides_input
                    else []
                ),
                impute=impute if impute else Impute(strategy="auto"),
            )
        )

    return transformation_options


def get_transformation_options(dataset_id: str = None) -> List[TransformationOption]:
    if dataset_id is None:
        return [
            TransformationOption(
                detectedType=ColumnDetectedType.BASIC_INTEGER.value,
                encoderSlugs={ColumnDetectedType.BASIC_INTEGER.value: ["auto"]},
                scalerSlugs={ColumnDetectedType.BASIC_INTEGER.value: ["auto"]},
                featureOverrides=[
                    ColumnTransformationOptions(
                        columnIndex=0,
                        filter=ColumnFilter.auto,
                        encoderSlugs={ColumnDetectedType.BASIC_INTEGER.value: ["auto"]},
                        scalerSlugs={ColumnDetectedType.BASIC_INTEGER.value: ["auto"]},
                    )
                ],
                impute=Impute(strategy="auto"),
            )
        ]
    output = get_custom_transformation_options(dataset_id)
    return output


# ──────────────────────────────────── Utils ──────────────────────────────────────── #
def get_default_models(task: MlTask) -> List:
    defaults = [
        model["name"]
        for model in get_permitted_models(task)["models"]
        if ("fast" in model["groups"] and model["enabled"] is True)
    ]
    all_models = get_permitted_models(task)["models"]
    return [model for model in all_models if model["name"] in defaults]
