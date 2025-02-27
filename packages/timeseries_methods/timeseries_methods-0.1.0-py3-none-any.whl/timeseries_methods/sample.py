import pathlib
from typing import Union

import pandas as pd

from . import compute, download


def wind_power(
    windfarms: pd.DataFrame,
    time_start: str,
    time_end: str,
    method: str = "Ninja",
    data_path: Union[str, pathlib.Path] = None,
) -> pd.DataFrame:
    """Get normalised wind power timeseries for specified wind farm locations.

    Arguments
    - windfarms: pandas.DataFrame - table with latitude, longitude, turbine_height. Index = wind farm identifier
    - time_start: str -start time, e.g. "2022-05-01"
    - time_end: str - end time, e.g. "2022-05-05"
    - method: str - method used for wind speed to power conversion.
        Availble: "Ninja", "Tradewind_offshore", "Tradewind_upland", "Tradewind_lowland"
    - data_path: str or pathlib.Path - data where downloaded wind speed data is kept
        If data has been downloaded before, it is read from local file.

    Returns
    - pandas.DataFrame - containing normalised wind power for all wind farm locations, index=time
    """

    if data_path is None:
        data_path = pathlib.Path("downloaded_nora3").mkdir(parents=True, exist_ok=True)
    else:
        data_path = pathlib.Path(data_path)

    wind_data = download.retrieve_nora3(windfarms, time_start, time_end, use_cache=True, data_path=data_path)

    if method == "Ninja":
        my_power_function = compute.func_ninja_compute_power
        my_args = {"turbine_power_curve": compute.get_power_curve(name="VestasV80")}
    elif method in ["Tradewind_offshore", "Tradewind_upland", "Tradewind_lowland"]:
        my_power_function = compute.func_power_curve(compute.get_power_curve(method))
        my_args = {}
    else:
        raise ValueError(f"Unknown power conversion method: {method}")

    # Compute power
    windpower = compute.compute_power(
        windfarms, wind_data, power_function=my_power_function, power_function_args=my_args
    )

    return windpower
