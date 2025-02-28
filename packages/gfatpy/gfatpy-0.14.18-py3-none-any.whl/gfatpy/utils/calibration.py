from datetime import datetime

import matplotlib.pyplot as plt
import numba
import numpy as np
import xarray as xr
from gfatpy.atmo.freudenthaler_molecular_properties import molecular_properties
from gfatpy.atmo.ecmwf import get_ecmwf_day
from gfatpy.utils.utils import moving_average, parse_datetime
from numba.typed import List
from scipy.signal import savgol_filter


def molecular_properties_2d(
    date: datetime | str,
    heights: np.ndarray,
    times: np.ndarray,
    wavelength: float = 532,
) -> xr.Dataset:
    """A function that request ECMWF temperatures and presures for a whole day.
    Then, pipes them to `gfatpy.atmo.atmo.molecular_properties`

    Args:
        date (datetime | str): date
        heights (np.ndarray): height ranges
        time (np.ndarray): time
        wavelength (float, optional): wavelength. Defaults to 532.

    Returns:
        xr.Dataset: it contains ["molecular_beta", "molecular_alpha", "attenuated_molecular_beta", "molecular_lidar_ratio"].
    """

    _date = parse_datetime(date)
    atmo_d = get_ecmwf_day(_date, heights=heights, times=times)

    mol_d = molecular_properties(
        wavelength,
        pressure=atmo_d.pressure.values,
        temperature=atmo_d.temperature.values,
        heights=atmo_d.range.values,
        times=atmo_d.time.values,
    )
    return mol_d


def iterative_fitting(
    rcs_profile: np.ndarray,
    attenuated_molecular_backscatter: np.ndarray,
    window_size_bins: int = 5,
    min_bin: int = 600,
    max_bin: int = 1000,
) -> np.ndarray:

    if rcs_profile.shape != attenuated_molecular_backscatter.shape:
        raise ValueError(f"RCS and Betta ranges must match")

    x_axis = np.arange(window_size_bins * 2)
    bool_matrix = np.full_like(rcs_profile, False, dtype=np.bool8)

    slope = []
    slope_mol = []

    for idx in np.arange(min_bin, max_bin):
        _rcs_norm = rcs_profile / rcs_profile[idx]
        _att_norm = (
            attenuated_molecular_backscatter / attenuated_molecular_backscatter[idx]
        )

        prof_slice = _rcs_norm[idx - window_size_bins : idx + window_size_bins]
        att_slice = _att_norm[idx - window_size_bins : idx + window_size_bins]

        coeff_prof = np.polyfit(np.arange(window_size_bins * 2), prof_slice, 1)
        coeff_att = np.polyfit(np.arange(window_size_bins * 2), att_slice, 1)

        slope.append(coeff_prof[0])
        slope_mol.append(coeff_att[0])

        # plt.scatter(x_axis, prof_slice, c="g")
        # plt.plot(x_axis, np.polyval(coeff_prof, x_axis), c="g")

        # plt.scatter(x_axis, att_slice, c="b")
        # plt.plot(x_axis, np.polyval(coeff_att, x_axis), c="b")

        # plt.show()

        att_data = np.polyval(coeff_att, x_axis)
        r2 = 1 - (
            ((prof_slice - att_data) ** 2).sum()
            / ((prof_slice - att_data.mean()) ** 2).sum()
        )

        # print(f'Mol m: {coeff_att[0]}')
        # print(f'Prof m: {coeff_prof[0]}')
        # if r2 > 0.25:
        #     print(f"R^2: {r2}")

    # plt.plot(slope)
    # plt.plot(slope_mol)
    # plt.close()
    return bool_matrix


def split_continous_measurements(
    time_array: np.ndarray, time_greater_than: float = 121 # Two minutest to avoid one profile search multiple DC
) -> list[np.ndarray]:
    """Groups times array into clusters with no more that `time_greater_than`

    Args:
        time_array (np.ndarray): Time

    Returns:
        list[np.ndarray]: list of lidar measurement slices
    """
    diffs = (time_array[1:] - time_array[0:-1]).astype("f") / 1e9  # type: ignore
    return np.split(time_array, np.where(diffs > time_greater_than)[0] + 1)


def mask_by_slope(
    rcs: xr.DataArray,
    att_beta: xr.DataArray,
    min_height: float = 4000,
    max_height: float = 7000,
    window_size: float = 1000,
    window_time: float = 30,
    max_rel_error: float = 0.15,
    plot_profile: int | None = None,
) -> xr.DataArray:
    rcs_sel = rcs.sel(range=slice(min_height, max_height))
    beta_sel = att_beta.sel(range=slice(min_height, max_height))

    rcs_sel = xr.apply_ufunc(
        moving_average, rcs_sel, kwargs={"window_size": window_time}, dask="allowed"
    )
    rcs_sel = xr.apply_ufunc(
        smooth_profiles, rcs_sel, kwargs={"window_size": 200}, dask="allowed"
    )

    result = np.full_like(beta_sel.values, False, dtype=bool)

    for idx, height in enumerate(rcs_sel.range):
        valid_ranges = rcs_sel.range[
            (height - window_size / 2 <= rcs_sel.range)
            & (height + window_size / 2 >= rcs_sel.range)
        ]
        height_rcs = rcs_sel.loc[dict(range=valid_ranges)]
        height_rcs /= height_rcs.isel(range=0)

        height_beta = beta_sel.loc[dict(range=valid_ranges)]
        height_beta /= height_beta.isel(range=0)

        x = np.arange(height_rcs.shape[1])

        slopes_rcs = np.polyfit(x, height_rcs.values.T, 1)[0]
        slopes_beta = np.polyfit(x, height_beta.values.T, 1)[0]

        result[:, idx] = (
            np.abs((slopes_rcs - slopes_beta) / slopes_beta) <= max_rel_error
        )

    result_data_array = xr.full_like(rcs, False)
    result_data_array.loc[dict(range=slice(min_height, max_height))] = result

    if plot_profile is not None:
        md = (max_height + min_height) / 2
        n_rcs = rcs[plot_profile] / rcs[plot_profile].sel(range=md, method="nearest")
        n_rcs_smth = rcs_sel[plot_profile] / rcs_sel[plot_profile].sel(
            range=md, method="nearest"
        )
        n_beta = att_beta[plot_profile] / att_beta[plot_profile].sel(
            range=md, method="nearest"
        )
        plt.plot(rcs.range, n_rcs)
        plt.plot(att_beta.range, n_beta)
        plt.plot(n_rcs_smth.range, n_rcs_smth)

        results = np.where(result_data_array[plot_profile], n_beta, np.nan)

        plt.plot(result_data_array.range, results, c="r", lw=2)

        plt.yscale("log")
        plt.show()

    return result_data_array


def mask_by_corrcoef(
    rcs: xr.DataArray,
    att_beta: xr.DataArray,
    min_height: float = 1000,
    max_height: float = 15000,
    window_size: float = 500,
    window_time: float = 15,
    min_corr: float = 0.95,
):

    rcs_sel = rcs.sel(range=slice(min_height, max_height))
    beta_sel = att_beta.sel(range=slice(min_height, max_height))

    rcs_sel = xr.apply_ufunc(smooth_profiles, rcs_sel, kwargs={"window_size": 170})
    rcs_sel = xr.apply_ufunc(
        moving_average, rcs_sel, kwargs={"window_size": window_time}
    )

    result = np.full_like(beta_sel.values, False, dtype=bool)
    ranges = rcs_sel.range.values

    lim_indexes = List()
    range_mask_limits = [
        np.where((h - window_size / 2 <= ranges) & (h + window_size / 2 >= ranges))[0]
        for h in ranges
    ]

    for idx in range(len(range_mask_limits)):
        c_list = List()
        c_list.append(range_mask_limits[idx][0])
        c_list.append(range_mask_limits[idx][-1])

        lim_indexes.append(c_list)

    result_array = windowed_correlation(
        rcs_sel.values,
        beta_sel.values,
        range_mask_limits=lim_indexes,
        min_corr=min_corr,
    )

    result_data_array = xr.full_like(rcs, False)
    result_data_array.loc[dict(range=slice(min_height, max_height))] = result_array

    return result_data_array
    # TODO:Finish function


def smooth_profiles(
    arr: np.ndarray, /, *, window_size: int = 11, polyorder: int = 3
) -> np.ndarray:
    def smooth_profile(_x: np.ndarray) -> np.ndarray:
        return savgol_filter(_x, window_size, 3)

    return np.apply_along_axis(smooth_profile, 1, arr)


@numba.njit(parallel=True)
def windowed_correlation(
    rcs: np.ndarray,
    att_beta: np.ndarray,
    /,
    *,
    range_mask_limits: list[list[int]],
    min_corr: float,
) -> np.ndarray:

    result_array = np.full(rcs.shape, np.nan)

    for t_idx in numba.prange(rcs.shape[0]):
        for r_idx in numba.prange(rcs.shape[1]):
            r_masks = range_mask_limits[r_idx]

            rcs_masked = rcs[t_idx][r_masks[0] : r_masks[1]]
            beta_masked = att_beta[t_idx][r_masks[0] : r_masks[1]]

            rcs_masked /= beta_masked[0]

            corr = np.corrcoef(rcs_masked, beta_masked)[0, 1]
            # set_trace()
            result_array[t_idx, r_idx] = corr >= min_corr

    return result_array


def cluster_value(arr: np.ndarray, /, *, value=1) -> list[list[tuple[int, int]]]:
    def cluster_1d(row) -> list[tuple[int, int]]:
        _i: int = 0
        count: int = 0
        clusters: list[tuple[int, int]] = []  # list[position, count]
        for (_i, *_), _v in np.ndenumerate(row):
            if _v == value and count == 0:
                count += 1
            elif _v == value and count != 0:
                count += 1
            elif _v != value and count == 0:
                continue
            elif _v != value and count != 0:
                clusters.append((_i - (1 + count), count))
                count = 0

        if count != 0:
            clusters.append((_i - (1 + count), count))

        return clusters

    time_cluster: list[list[tuple[int, int]]] = []

    for time_row in arr:
        time_cluster.append(cluster_1d(time_row))

    return time_cluster


def cluster_at_least(
    clusters: list[list[tuple[int, int]]], n_min: int = 5, /
) -> np.ndarray:
    result = np.full((len(clusters), 2), np.nan, dtype=float)

    for idx, prof_clust in enumerate(clusters):
        filtered = list(filter(lambda t: t[1] >= n_min, prof_clust))

        if len(filtered) == 0:
            continue

        selected = sorted(filtered, key=lambda t: t[1], reverse=True)[0]
        result[idx] = np.array([selected[0], selected[0] + selected[1]])

    return result

