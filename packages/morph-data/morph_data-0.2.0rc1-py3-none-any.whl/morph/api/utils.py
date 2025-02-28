import sys
from typing import Any, Dict, Literal, Optional, Union

import pandas as pd


def convert_file_output(
    type: Literal["json", "html", "markdown"],
    output_path: str,
    ext: str,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
) -> Union[str, Dict[str, Any]]:
    if type == "json":
        if ext == "csv":
            chunks = []
            for chunk in pd.read_csv(
                output_path,
                header=0,
                chunksize=1_000_000,
                encoding_errors="replace",
                sep=",",
            ):
                chunks.append(chunk)
            df = pd.concat(chunks, axis=0)
        elif ext == "parquet":
            df = pd.read_parquet(output_path)
        count = len(df)
        limit = limit if limit is not None else len(df)
        skip = skip if skip is not None else 0
        df = df.iloc[skip : skip + limit]
        df = df.replace({float("nan"): None, pd.NaT: None}).to_dict(orient="records")
        return {"count": count, "items": df}
    elif type == "html" or type == "markdown":
        with open(output_path, "r") as f:
            return f.read()


def convert_variables_values(variables: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if variables is None:
        return {}
    variables_: Dict[str, Any] = {}
    for k, v in variables.items():
        if isinstance(v, str):
            if v.isdigit():
                variables_[k] = int(v)
                continue
            try:
                f_v = float(v)
                variables_[k] = f_v
                continue
            except ValueError:
                pass
        variables_[k] = v
    return variables_


def set_command_args():
    if len(sys.argv) < 2:
        sys.argv = ["", "serve"]
