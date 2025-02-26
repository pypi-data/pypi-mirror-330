# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pandas import DataFrame

from evoml_pipeline_interface.models import PipelineDataConf, PipelinePredictConfig

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# Provisional data types until the corresponding interfaces are created
MLModelType = Any
PreprocessorType = Any


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                              Pipeline Handler Interface                                              #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class PipelineHandlerI(metaclass=ABCMeta):
    """Interface of the class that handles the loading of the ML model."""

    field_predictions: str = "predictions"
    field_probabilities: str = "probabilities"
    field_metrics: str = "metrics"

    def __init__(self, data_conf: PipelineDataConf):
        self.data_conf: PipelineDataConf = data_conf
        self._preprocessor: Optional[PreprocessorType] = None
        self._model: Optional[MLModelType] = None
        self._predict_conf: Optional[PipelinePredictConfig] = None

    # --------------------------------------------------------------------------------------------------

    @property
    def preprocessor(self) -> PreprocessorType:
        """Preprocessor instance."""
        raise NotImplementedError

    @property
    def model(self) -> MLModelType:
        """ML Model instance."""
        raise NotImplementedError

    @property
    def predict_conf(self) -> PipelinePredictConfig:
        """Configuration of the prediction process."""
        raise NotImplementedError

    @property
    def train_target(self) -> str:
        """Name of the target column"""
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------

    @abstractmethod
    def run_prediction(
        self,
        data: Union[str, Path, DataFrame],
        model: Optional[MLModelType] = None,
        preprocessor: Optional[PreprocessorType] = None,
        run_evaluate: bool = False,
        write_csv: bool = False,
        out_file: Optional[Path] = None,
    ) -> Dict:
        """Send user's input as a dataframe to the model and get a prediction.

        Args:
            data (Union[str, Path, pandas.DataFrame]): Input data to the model.
            model (Optional[MetaModel]): The model to use for prediction. If None, use the model from self.
            preprocessor (Optional[DataPreprocessor]): The preprocessor to use. If None, use the preprocessor from self.
            run_evaluate (bool): If True, run evaluate.
            write_csv (bool): If True, write the results to a CSV file.
            out_file (Optional[Path]): The path to the output file. If None, no file is written.

        Returns:
            prediction (Dict): The prediction and probabilities for each category.
        """
        raise NotImplementedError

    # --------------------------------------------------------------------------------------------------

    @abstractmethod
    def train(self, train_file: Optional[Path] = None, test_file: Optional[Path] = None, data: Optional[Path] = None):
        """Trains the ML model with the given file(s) data.

        Args:
            train_file (Optional[Path]): File containing the data used for training.
            test_file (Optional[Path]): File containing the data used to validate the training.
            data (Optional[Path]): Instead of indicating the 2 previous files, a single file
                can be provided, which must also contain the output column, from which the model
                training and validation data are obtained.
        """
        raise NotImplementedError

    # --------------------------------------------------------------------------------------------------

    def update_preprocessor(self, data: Path):
        """Updates preprocessor with the given data.

        Args:
            data (Optional[Path]): a single file which must contain the output column,
                which will be used to update the preprocessor object.
        """
        raise NotImplementedError

    def save_preprocessor(self, output_path: Path):
        """Save the current preprocessor joblib.

        Args:
            output_path (Path): output location where the current preprocessor object will be saved.
        """
        raise NotImplementedError
