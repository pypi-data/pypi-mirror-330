import numpy as np
import logging
from sktime.distances import distance
from typing import Callable, Union
from tqdm import tqdm
def pearson(x, y):
    """Custom Pearson correlation function to return the first value from the numpy's Pearson correlation function."""
    return np.corrcoef(x, y)[0][1]

def distance_sktime_interface(input_data_dictionary, metric, kwargs={}):
    result = np.array(
        [distance(input_data_dictionary["forecasted_window"][:, current_component],
                  input_data_dictionary["training_windows"][current_window, :, current_component],
                  metric, **kwargs)
         for current_window in tqdm(range(input_data_dictionary["windows_len"]), desc="Windows procesadas", position=0)
         for current_component in range(input_data_dictionary["components_len"])]
    ).reshape(-1, input_data_dictionary["components_len"])
    result = np.nan_to_num(result, nan=0)

    return result

def compute_distance_interface(input_data_dictionary,
                               metric: Union[str, Callable[[np.ndarray, np.ndarray], float]],
                               kwargs):
    correlation_per_window = np.array([])
    # correlation_per_window = metric(input_data_dictionary, **kwargs)
    try:
        # Attempt to use sktime's distance interface
        return distance_sktime_interface(input_data_dictionary, metric, kwargs)
    except Exception as sktime_error:
        logging.warning(f"Failed with sktime metric: {sktime_error}")

    # Fallback to custom callable
    try:
        if callable(metric):
            return metric(input_data_dictionary, **kwargs)
        else:
            raise TypeError(f"Metric must be callable or sktime-compatible, got: {type(metric).__name__}")
    except Exception as custom_error:
        logging.error("Custom callable execution failed", exc_info=True)
        raise


