__all__ = ["get_model", "get_model_types_i", "get_models"]

from base64 import b64encode
from pathlib import Path

import pandas as pd
import tabeline as tl

from .._sdk.job import Job
from .._sdk.ode_model import OdeModelFromBytes, OdeModelFromText, OdeModelTypes
from .get_table import get_table
from .helper import DataFrameLike, PathLike


def get_models(model: DataFrameLike | PathLike) -> tl.DataFrame:
    match model:
        case str() | Path():
            models_path = Path(model)
            if not models_path.is_file():
                raise FileNotFoundError(f"{models_path} is not a file")

            if models_path.suffix == ".csv":
                return get_table(models_path)
            else:
                return get_table(pd.DataFrame(columns=["model"], data=[str(models_path)]))
        case tl.DataFrame() | pd.DataFrame():
            return get_table(model)
        case _:
            raise NotImplementedError(f"{type(model).__name__} is not a supported type for models")


def get_model(path: PathLike) -> OdeModelFromText | OdeModelFromBytes:
    path = Path(path)
    match path.suffix:
        case ".txt" | ".model":
            return OdeModelFromText(text=Path(path).read_text(encoding="utf-8"), format="reaction")
        case ".sbml":
            return OdeModelFromText(text=Path(path).read_text(encoding="utf-8"), format="sbml")
        case ".qsp":
            base64_content = b64encode(Path(path).read_bytes()).decode("utf-8")
            return OdeModelFromBytes(base64_content=base64_content, format="qsp_designer")
        case _:
            raise NotImplementedError(f"File extension {path.suffix} is not supported")


def get_model_types_i(
    models: list[dict],
    model_map: dict[str, Job[None, OdeModelTypes]],
    labels: dict[str, str | float | int | bool],
) -> tuple[str, OdeModelTypes]:
    unique_models = {value["model"] for dictionary in models for value in dictionary.values()}

    # make sure that there is only one model for each simulation
    if len(models) > 1:
        if len(labels) == 0:
            raise ValueError(
                f"Multiple models found while there is no simulation table: {', '.join(sorted(unique_models))}"
            )
        else:
            raise ValueError(
                f"Multiple models found for label(s) {', '.join([f'{key}={value}' for key, value in labels.items()])}:"
                f" {', '.join(sorted(unique_models))}"
            )

    model_path = next(iter(models[0].values()))["model"]
    model = model_map[model_path]
    return model.id, model.types
