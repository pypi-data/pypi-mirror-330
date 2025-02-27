from typing import List, Tuple, Iterable, Union, Optional
import numpy as np

from shyft.time_series import TsVector, TimeSeries, Calendar, time_series_to_bokeh_plot_data
from shyft.dashboard.time_series.state import Quantity


class DataUtilError(RuntimeError):
    pass


def calculate_dead_band_indices(ts_input: np.ndarray, eps: Optional[float] = 0.0005):
    """
    This function find all indices to reduce the data of a numpy array.
    The algorithm is a basic compression / dead band filter with eps being the dead band.
    It is tested for arrays with integer values.

    e.g.

    values:  1  1  1  2  3  3  3  3  4  3   3   3   3   3
    indices: 0  1  2  3  4  5  6  7  8  9  10  11  12  13

    would return:
        - np.array([[0, 2],
                    [4, 7],
                    [9, 13]])
        - [3, 8]

    Parameters
    ----------
    ts_input: np.ndarray which should be analysed for compression
    eps: deadband for integer set to a low value

    Returns
    -------
    - a numpy array with all indices which can compress one value
            e.g [[2,4]] meaning all values from index 2 to 4 can be compressed under the given eps
    - a list of single value indices
            e.g [5,6,7] meaning index 5 ,6, 7 cannot be compressed and are unique under the given eps
    """
    tc = np.hstack([ts_input[0], ts_input, ts_input[-1], ts_input[-1]])
    left_indices = set(np.where(tc[1:-1] - tc[0:-2] != 0)[0].tolist())
    right_indices = set(np.where(tc[1:-1] - tc[2::] != 0)[0].tolist())
    scatter_indices = set.intersection(left_indices, right_indices)
    if abs(ts_input[0] - ts_input[1]) > eps:
        scatter_indices = scatter_indices.union({0})
    if abs(ts_input[-1] - ts_input[-2]) > eps:
        scatter_indices = scatter_indices.union({len(ts_input) - 1})
    multi_line_indices = set.union(left_indices, right_indices, {0, len(ts_input) - 1}).difference(scatter_indices)
    multi_line_indices = sorted(multi_line_indices)

    return np.array(multi_line_indices).reshape(len(multi_line_indices)//2, 2), sorted(scatter_indices)


def data_to_patch_values(data1: np.ndarray, data2: np.ndarray,
                         non_nan_slices: Optional[Iterable[slice]] = None) -> List[np.ndarray]:
    """

    :param data1:
    :param data2:
    :param non_nan_slices:
    :return:
    """
    if non_nan_slices is None:
        non_nan_slices = np.ma.clump_unmasked(np.ma.masked_invalid(data1))
    if len(non_nan_slices) == 1:
        d1 = data1[non_nan_slices[0]]
        n = len(d1)
        res = np.empty(2*n, dtype=d1.dtype)
        res[:n] = d1
        res[n:] = data2[non_nan_slices[0]][::-1]
        return [res]
    else:
        resulting_patches = []
        for slicex in non_nan_slices:
            d1 = data1[slicex]
            n = len(d1)
            res = np.empty(2*n, dtype=d1.dtype)
            res[:n] = d1
            res[n:] = data2[slicex][::-1]
            resulting_patches.append(res)
        return resulting_patches


def convert_ts_to_plot_vectors(*, ts: TimeSeries, cal: Calendar, crop_nan: Optional[bool] = False, interpret_point_interpretation: Optional[bool] = False, time_scale: Optional[float] = 1000.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    This routine is about 30..100x faster than corresponding python code.

    :param ts: time-series to extract plot data from
    :param cal: containing time-zone offsets to apply to the time-points
    :param crop_nan: crop trailing nans from the time-series
    :param interpret_point_interpretation: interpret ts.point_interpretation, and if POINT_AVERAGE_VALUE make stair-step curve (2x+1 in size)
    :param time_scale: bokeh uses time as numbers in ms scale, so default multiply by 1000.0
    :return: tuple with times,values, where times is tz-offset with cal,and then multiplied by  time-scale, values

    """
    tv = time_series_to_bokeh_plot_data(ts=ts, calendar=cal, time_scale=time_scale, force_linear=not interpret_point_interpretation, crop_trailing_nans=crop_nan)
    return tv[0], tv[1]


def merge_convert_ts_vectors_to_numpy(*, ts_vectors: List[Quantity[TsVector]], time_scale: Optional[float] = 1.0,
                                      cal: Optional[Calendar] = None) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Merges a list of ts_vectors and converts them to numpy arrays

    Parameters
    ----------
    ts_vectors: list of ts_vectors to merge and convert
    time_scale: default 1.0, return time-vectors in seconds (utc)
    cal: Calendar, default None, specify if time-stamps should be tz-adjusted

    Returns
    -------
    aligned_time: Array of time points for the entire span of ts_vectors
    data_list: List of data for each time series in all ts_vectors. Example: a = data_list[i][j] is the numpy array with
        data of the time series j and vector i. The numpy array is filles with nan where a(t) does not have data.
    """
    if len(ts_vectors) == 0:
        return np.array([]), []

    tsv = TsVector()
    ix_map = [] # start index of `ts_vectors[i]` in tsv
    cal = cal or Calendar()
    t_max = -np.inf
    for qtsv in ts_vectors:
        ix_map.append(len(tsv))
        tsv.extend(qtsv.magnitude)

        # as extract label doesn't give end period
        t_max_all = [int(ts.time_axis.total_period().end) for ts in qtsv.m if len(ts) > 0]
        if len(t_max_all) > 0:
            t_max_tsv = max(t_max_all)
            t_max = max(t_max_tsv, t_max) # at least an approximation, not 100¤ sure e.g. for calander_dt

    ix_map.append(len(tsv))  # add last elem upper boundary.
    r = tsv.extract_as_table(cal=cal, time_scale=time_scale)

    if len(r) == 0 or len(r[0]) == 0:
        return np.array([]), []
    values = []
    for i in range(len(ts_vectors)):
        g = [r[j + 1] for j in range(ix_map[i], ix_map[i + 1])]
        values.append(g)

    times = np.empty(len(r[0])+1, dtype="float64")
    times[:-1] = r[0]
    times[-1] = t_max * time_scale
    return times, values


def find_nearest(array: np.ndarray, input_value: Union[float, int], smaller_equal: Optional[bool] = True):
    """
    Returns the index of the array value closest to input_value in the given array.
    The closest value will be chosen either the first one smaller_equal to input value if smaller_equal is True or
    larger equal if smaller_equal is False

    Find index of nearest value in array to input_value
    smaller_equal: bool to decide if search value <= input_value or value >= input_value
    """
    if len(array) == 0:
        raise DataUtilError('Empty array sent to find_nearest()')
    if smaller_equal:
        idx = np.searchsorted(array, input_value, side='right')
    else:
        idx = np.searchsorted(array, input_value, side='left')
    if idx == len(array) or (idx != 0 and smaller_equal):
        idx = idx - 1
    return idx


def convert_ts_to_numpy(ts: TimeSeries, crop_nan: Optional[bool] = False,
                        interpret_point_interpretation: Optional[bool] = False) -> Tuple[np.ndarray, np.ndarray]:
    """
    Backward compatibility ONLY:
    Convert shyft time series into nummpy array

    :param ts: shyft TimeSeries containing values and time points
    :param crop_nan: if True, strip away trailing nans and shorten result accordingly
    :param interpret_point_interpretation: interpret ts.point_interpretation, and if POINT_AVERAGE_VALUE make stair-step curve (2x+1 in size)
    :return: tuple of [ndarray, np.array] containing [time, values]
    """

    return convert_ts_to_plot_vectors(ts=ts, cal=Calendar(),
                                      crop_nan=crop_nan,
                                      interpret_point_interpretation=interpret_point_interpretation,
                                      time_scale=1.0)
