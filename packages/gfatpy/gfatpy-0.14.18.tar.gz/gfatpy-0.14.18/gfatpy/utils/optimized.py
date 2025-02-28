import numpy as np
from numpy.polynomial.polynomial import polyfit

import numba

from gfatpy.utils.utils import linear_fit


def best_slope_fit(mat1: np.ndarray, mat2: np.ndarray, window: int) -> np.ndarray:

    assert mat1.shape == mat2.shape, "Matrices shape must match"
    assert isinstance(window, int), "Window argument must be an integer"

    x = np.arange(window)
    res = np.array([])

    # Iter in first dimension, equivalent to time in lidar case
    for idx in range(mat1.shape[0]):
        windowed1 = rolling(mat1[idx], window)
        windowed2 = rolling(mat2[idx], window)

        slopes1 = polyfit(x, windowed1.T, 1)[0]
        slopes2 = polyfit(x, windowed2.T, 1)[0]
        chosen_group = np.argmin(np.abs(slopes1 - slopes2) / slopes1)
        res = np.hstack([res, chosen_group + np.floor(window / 2)])  # Append chosen bin

    return res.astype(int)


@numba.njit(parallel=True)
def windowed_corrcoefs(arr1: np.ndarray, arr2: np.ndarray, w_size: int):
    range_shape = arr1.shape[1] - (w_size - 1)
    _corrcoefs = np.empty((arr1.shape[0], range_shape))
    for t_idx in numba.prange(arr1.shape[0]):
        w1 = rolling(arr1[t_idx], w_size)
        w2 = rolling(arr2[t_idx], w_size)
        for idx in numba.prange(range_shape):
            _w1 = w1[idx]
            _w2 = w2[idx]
            coeff = np.corrcoef(_w1, _w2)[1, 0]
            _corrcoefs[t_idx][idx] = coeff
    return _corrcoefs


@numba.njit(parallel=True)
def windowed_proportional(arr1: np.ndarray, arr2: np.ndarray, /, *, w_size: int):

    assert arr1.shape == arr2.shape, "Matrices shape must match"
    # assert isinstance(w_size, int), "Window argument must be an integer"

    range_shape = arr1.shape[1] - (w_size - 1)
    _proportional = np.full((arr1.shape[0], range_shape), np.nan)
    _factor = np.full((arr1.shape[0], range_shape), np.nan)

    for t_idx in numba.prange(arr1.shape[0]):
        w1 = rolling(arr1[t_idx], w_size)
        w2 = rolling(arr2[t_idx], w_size)

        for idx in numba.prange(range_shape):
            _w1 = w1[idx]
            _w2 = w2[idx]

            ratio = np.mean(_w2 / _w1)
            adj = _w1 * ratio
            _factor[t_idx][idx] = ratio
            _proportional[t_idx][idx] = (np.abs(adj - _w2) / _w2).mean()

    return _factor, _proportional


@numba.njit()
def rolling(a, window):
    shape = (a.size - window + 1, window)
    strides = (a.itemsize, a.itemsize)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


@numba.njit
def correlate_vector_to_matrix(vector, matrix):
    """Correlate a vector to a matrix

    Args:
        vector (np.ndarray): Vector to correlate
        matrix (np.ndarray): Matrix to correlate

    Returns:
        np.ndarray: Correlation result
    """
    corr = np.zeros(matrix.shape[1])
    for i in range(matrix.shape[1]):
        corr[i] = np.corrcoef(vector, matrix[:, i])[0, 1]
    return corr


def rolling_window_test(a, window):
    shp = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shp, strides=strides)

def moving_linear_fit(x_array, y_array, window_size, **kwargs):
    """ Moving polyfit 
    """
    xdata = rolling_window_test(x_array, window_size).T
    ydata = rolling_window_test(y_array, window_size).T
    
    d, slope = np.nan*np.ones(len(x_array)), np.nan*np.ones(len(x_array))
    mrse, anderson_coef = np.nan*np.ones(len(x_array)), np.nan*np.ones(len(x_array))
    for idx in range(ydata.shape[1]):
        # fit_parameters = np.polyfit(xdata[:,idx], ydata[:,idx], deg = degree, full=False)
        stats = linear_fit(xdata[:,idx], ydata[:,idx])
        slope[idx]  = stats["parameters"][1] 
        std_slope = stats["standard_deviation_parameters"][1]
        d[idx] = stats["durbin_watson"]
        mrse[idx] = stats["msre"]
        anderson_coef[idx] = stats["anderson"][0]
        # if idx in  [1100, 1300, 1600, 1900]:
        #     import matplotlib.pyplot as plt
        #     fig, ax = plt.subplots()
        #     ax.plot(xdata[:,idx], ydata[:,idx], linewidth=0, marker='o', label=f'{ranges[idx]}')
        #     ax.plot(xdata[:,idx],np.polyval(np.flip(parameters), xdata[:,idx]), label='fit')
        #     fig.savefig(f'test_dws_{idx}.png', dpi=300)
        #     plt.close(fig)
    results = {"slope": slope, "std_slope": std_slope ,"durbin_watson": d, "mrse": mrse, "anderson": anderson_coef}
    return results
