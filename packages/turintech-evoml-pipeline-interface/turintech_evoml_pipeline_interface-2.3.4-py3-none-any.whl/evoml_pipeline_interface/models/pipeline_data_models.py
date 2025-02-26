# pylint: disable=E0213
#       E0213: Method should have "self" as first argument (no-self-argument)
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import Field, validator

from evoml_api_models import BaseModelWithAlias, DatasetFileHeaders, MlTask

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["PipelineApiInfo", "PipelineInfoMetric", "PipelineConfig", "PipelineSettings", "PipelinePredictConfig"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                 PipelineDataConf.api_info_file_path file Data Models                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class PipelineApiInfo(BaseModelWithAlias):
    """Data structure with the basic information contained in the file PipelineDataConf.api_info_file_path of the
    ML Model.
    """

    encoding: str = Field(..., example="utf-8")
    dataset_id: str = Field(..., example="utf5f61c5ada9567d0048e0c2978")
    target_column: int = Field(..., example=13)
    dataset_name: str = Field(..., example="test_heart-8")
    label_mapping: Optional[List] = Field(None, example=["A", "B", "C"])
    ml_task: MlTask = Field(..., example="classification")
    trial_id: str = Field(..., example="5f68bb96a9567d0048e10bce")
    trial_name: str = Field(..., example="test_heart - target")


class PipelineInfoMetric(BaseModelWithAlias):
    """Data structure with a metrics information."""

    name: str
    value: float


class PipelineConfig(PipelineApiInfo):
    """Data structure with the information contained in the file PipelineDataConf.api_info_file_path of the ML Model."""

    time_of_deployment: Optional[str] = Field(None, example="2020-12-22T17:11:08")
    model_name: str = Field(..., example="GaussianNB-349d1b")
    metrics: List[PipelineInfoMetric] = Field(
        ..., example=[PipelineInfoMetric(name="accuracy", value=0.8398936170212765)]
    )


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                 PipelineDataConf.settings_file_path file Data Models                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class PipelineSettings(DatasetFileHeaders):
    """Data structure with the information contained in the file PipelineDataConf.settings_file_path of the ML Model"""


class PipelinePredictConfig(BaseModelWithAlias):
    """Data structure with the information contained in the file PipelineDataConf.predict_config_file_name of the
    ML Model.
    """

    file_path: Optional[Path] = Field(None)
    label_column: str = Field(...)
    is_time_series: bool = Field(...)
    ml_task: str = Field(...)
    index_column: Optional[Union[int, List]] = Field(False, alias="date_column")

    @validator("index_column")
    def date_column_validator(cls, value: Union[int, List], values: Dict):
        return value if values.get("is_time_series") else False
