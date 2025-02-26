# pylint: disable=E0213
#       E0213: Method should have "self" as first argument (no-self-argument)
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from pathlib import Path
from typing import Dict, Final

from pydantic import Field, root_validator

from evoml_api_models import PropertyBaseModel

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


__all__ = [
    "DATA_DIR_NAME",
    "DEPLOY_DIR_NAME",
    "DOCS_DIR_NAME",
    "NOTEBOOKS_DIR_NAME",
    "SETUP_DIR_NAME",
    "SRC_DIR_NAME",
    "PipelineDataConf",
    "PipelineSrcCodeConf",
    "PipelineRootProjectConf",
    "PipelineProjectConf",
    "PipelineProjectExtendedConf",
]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      Constants                                                       #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

DEPLOY_DIR_NAME: Final[str] = "deploy"
DOCS_DIR_NAME: Final[str] = "docs"
NOTEBOOKS_DIR_NAME: Final[str] = "notebooks"
DATA_DIR_NAME: Final[str] = "data"
SETUP_DIR_NAME: Final[str] = "setup"
SRC_DIR_NAME: Final[str] = "src"


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                 Configuration Model                                                  #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class PipelineDataConf(PropertyBaseModel):
    """
    Data model that specifies the data folder structure expected to be found
    in the pipeline project of an EvoML ML model
        .
        ├── final.json
        ├── predict.config.json
        ├── prediction_results.csv
        ├── data_raw.csv
        ├── model_artifacts
        └── infos.json
    """

    pipeline_data_path: Path

    # --------------------------------------------------------------------------------------------------

    final_file_name: str = Field(
        "final.json", description="File containing information regarding the pipeline and its performance"
    )
    predict_config_file_name: str = Field(
        "predict.config.json", description="Configuration file for the prediction process"
    )
    sample_file_name: str = Field("sample.csv", description="Sample file name of the preprocessed dataset")
    prediction_results_file_name: str = Field(
        "prediction_results.csv", description="Prediction results for the dataset provided"
    )
    raw_data_file_name: str = Field(
        "data_raw.csv", description="Name of the default file specify in the predict config file"
    )
    model_artifacts_dir_name: str = Field(
        "model_artifacts", desciption="Folder containing all artifacts providing a " "pre-trained version of the model"
    )
    preprocessor_job_lib_name: str = Field(
        "prepro.joblib", desciption="File containing a ready-to-run version of the " "preprocessing technique"
    )
    api_info_name: str = Field("infos.json", desciption="File containing information for API deployment")

    # --------------------------------------------------------------------------------------------------

    @property
    def final_file_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.final_file_name)

    @property
    def predict_config_file_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.predict_config_file_name)

    @property
    def sample_file_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.sample_file_name)

    @property
    def prediction_results_file_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.prediction_results_file_name)

    @property
    def raw_data_file_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.raw_data_file_name)

    @property
    def model_artifacts_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.model_artifacts_dir_name)

    @property
    def preprocessor_job_lib_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.preprocessor_job_lib_name)

    @property
    def api_info_path(self) -> Path:
        return self.pipeline_data_path.joinpath(self.api_info_name)

    # --------------------------------------------------------------------------------------------------

    @staticmethod
    def __init_paths(pipeline_data_path: Path):
        return dict(pipeline_data_path=pipeline_data_path)

    @root_validator
    def validate_pipeline_data_path(cls, values: Dict):
        values.update(cls.__init_paths(values["pipeline_data_path"]))
        return values

    def __init__(self, pipeline_data_path: Path, **kwargs):
        kwargs.update(self.__init_paths(pipeline_data_path))
        super().__init__(**kwargs)


class PipelineSrcCodeConf(PropertyBaseModel):
    """Data model that specifies the source code folder structure expected to be
    found in the pipeline project of an EvoML ML model
        pipeline                       # package name by default
        ├── ......
        ├── pipeline_handler.py
        ├── predict.py
        ├── train.py
        ├── __about__.py
        └── __init__.py
    """

    pipeline_code_path: Path

    # --------------------------------------------------------------------------------------------------

    pipeline_handler_py_name: str = Field(
        "pipeline_handler.py", description="This module contains the class that handles the loading of the ML model"
    )
    train_py_name: str = Field("train.py", description="This script assists in training a model")
    predict_py_name: str = Field(
        "predict.py", description="This script assists in performing predictions based on a saved model"
    )

    # --------------------------------------------------------------------------------------------------

    @property
    def pipeline_handler_py_path(self) -> Path:
        return self.pipeline_code_path.joinpath(self.pipeline_handler_py_name)

    @property
    def train_py_path(self) -> Path:
        return self.pipeline_code_path.joinpath(self.train_py_name)

    @property
    def predict_py_path(self) -> Path:
        return self.pipeline_code_path.joinpath(self.predict_py_name)

    @property
    def pipeline_module_py_path(self) -> Path:
        return self.pipeline_code_path.joinpath("__init__.py")

    @property
    def pipeline_about_py_path(self) -> Path:
        return self.pipeline_code_path.joinpath("__about__.py")


class PipelineRootProjectConf(PropertyBaseModel):
    """Data model that specifies the files expected to be found in the root
    folder of the pipeline project of an EvoML ML model
        .
        ├── ......                     # PipelineDataConf
        ├── ......                     # PipelineSrcCodeConf
        ├── deploy/
        │   └── .env
        ├── docs/
        ├── setup
        │   ├── requirements.txt
        │   ├── requirements_ipynb.txt
        │   └── ......                 # PreprocessorSetupStructureConf
        ├── notebooks
        │   └── notebook.ipynb
        └── README.md
    """

    pipeline_path: Path

    # --------------------------------------------------------------------------------------------------

    @property
    def deploy_path(self) -> Path:
        return self.pipeline_path.joinpath(DEPLOY_DIR_NAME)

    @property
    def env_file_path(self) -> Path:
        return self.deploy_path.joinpath(".env")

    @property
    def docs_path(self) -> Path:
        return self.pipeline_path.joinpath(DOCS_DIR_NAME)

    @property
    def setup_path(self) -> Path:
        return self.pipeline_path.joinpath(SETUP_DIR_NAME)

    @property
    def notebooks_path(self) -> Path:
        return self.pipeline_path.joinpath(NOTEBOOKS_DIR_NAME)

    @property
    def requirements_path(self) -> Path:
        return self.setup_path.joinpath("requirements.txt")

    @property
    def notebook_requirements_path(self) -> Path:
        return self.setup_path.joinpath("requirements_ipynb.txt")

    @property
    def readme_path(self) -> Path:
        return self.pipeline_path.joinpath("README.md")

    # --------------------------------------------------------------------------------------------------

    @staticmethod
    def __init_paths(pipeline_path: Path):
        return dict(
            pipeline_path=pipeline_path,
            setup_path=pipeline_path.joinpath(SETUP_DIR_NAME),
        )

    @root_validator
    def validate_pipeline_root_path(cls, values: Dict):
        values.update(cls.__init_paths(values["pipeline_path"]))
        return values

    def __init__(self, pipeline_path: Path, **kwargs):
        kwargs.update(self.__init_paths(pipeline_path))
        super().__init__(**kwargs)


class PipelineProjectConf(PipelineRootProjectConf):
    """Data model that specifies the structure expected to be found in the
    pipeline project of an EvoML ML model
        .
        ├── data
        │   └── ......                 # PipelineDataConf
        ├── src
        │   └── pipeline
        │       └── ......             # PipelineSrcCodeConf
        └── ......                     # PipelineRootProjectConf
    """

    @property
    def data(self) -> PipelineDataConf:
        return PipelineDataConf(pipeline_data_path=self.pipeline_path.joinpath(DATA_DIR_NAME))

    @property
    def pipeline_source_code(self) -> PipelineSrcCodeConf:
        return PipelineSrcCodeConf(pipeline_code_path=self.pipeline_path.joinpath(*[SRC_DIR_NAME, "pipeline"]))


class PipelineProjectExtendedConf(PipelineRootProjectConf, PipelineDataConf, PipelineSrcCodeConf):
    """Data model that specifies the structure expected to be found in the pipeline project of an EvoML ML model.
    The difference with the PipelineProjectConf data model is that in this case there is no distinction between
    data configuration and source code configuration.
        .
        ├── data
        │   └── ......                 # PipelineDataConf
        ├── src
        │   └── pipeline
        │       └── ......             # PipelineSrcCodeConf
        └── ......                     # PipelineRootProjectConf
    """

    @staticmethod
    def __init_paths(pipeline_path: Path):
        return dict(
            pipeline_path=pipeline_path,
            pipeline_data_path=pipeline_path.joinpath(DATA_DIR_NAME),
            pipeline_code_path=pipeline_path.joinpath(*[SRC_DIR_NAME, "pipeline"]),
        )

    @root_validator
    def validate_path(cls, values: Dict):
        values.update(cls.__init_paths(values["pipeline_path"]))
        values = cls.validate_pipeline_data_path(values=values)
        values = cls.validate_pipeline_root_path(values=values)
        return values

    def __init__(self, pipeline_path: Path, **kwargs):
        kwargs.update(self.__init_paths(pipeline_path))
        super().__init__(**kwargs)
