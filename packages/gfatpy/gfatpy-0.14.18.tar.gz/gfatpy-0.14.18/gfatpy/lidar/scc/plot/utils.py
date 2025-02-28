from matplotlib.axes import Axes
import xarray as xr

from gfatpy.utils.plot import color_list
from gfatpy.lidar.scc.plot import SCC_PLOT_INFO, PLOT_INFO


def id2str(ID: int) -> str | None:
    """Convert any ID (channel or product) to string ID using information from SCC_PLOT_INFO.
    Args:
        hoi_configuration_ID (int): Lidar configuration ID (e.g., 783).
        ID (int): Channel or product ID (e.g., 2203).

    Returns:
        str | None: String ID (e.g., 1064fta). None means ID not found. Likely, the ID is not yet in the configuration. 
    """
    productIDs = SCC_PLOT_INFO.keys()
    if ID in productIDs:
        #Search in products
        string_ID = SCC_PLOT_INFO[ID]['string_ID']
    else:
        #Search in channels
        string_ID = None
        for productID_ in productIDs:
            channels_ = SCC_PLOT_INFO[productID_]['channels'].keys()
            if ID in channels_:
                string_ID = SCC_PLOT_INFO[productID_]['channels'][ID]
        if string_ID is None:
            raise Warning(f"ID {ID} not found in product {productID_} channels {channels_}.")
    return string_ID

def plot_angstrom(ae: dict[str: xr.DataArray], ax: Axes, ae_limits: tuple[float, float] | None = None, range_limits: tuple[float, float] | None = None) -> Axes:
    """Plot angstrom exponent.

    Args:
        ae (dict[str: xr.DataArray]): dict with angstrom exponents from `gfatpy.lidar.scc.retrieval.angstrom_exponent`
        ax (Axes): Axes handle.
        ae_limits (tuple[float, float] | None, optional): limits to the Angstrm exponent axis. Defaults to None means (-1,3).
        range_limits (tuple[float, float] | None, optional): Range limits. Defaults to None means (0,14).

    Raises:
        ValueError: Error plotting Angstrom exponent.
        ValueError: Error plotting Angstrom exponent.

    Returns:
        Axes: axis with the Angstrom exponent plots.
    """
    for ae_name in ae.keys():
        ae_da = ae[ae_name]
        ae_da['altitude'] = ae_da['altitude'] / 1e3
        if ae_da is None:
            print(f"Angstrom exponent {ae_name} is None.")
            continue
        if 'time' in ae_da.dims:
            colors = color_list(len(ae_da.time.values),cmap=PLOT_INFO['ae2cmaps'][ae_name]) 
            for idx, time_ in enumerate(ae_da.time.values):
                try:
                    ae_da.sel(time=time_).plot(y='altitude',ax=ax, label=ae_name, color=colors[idx])
                except:
                    raise ValueError(f"Error plotting Angstrom exponent")
        else:
            try:
                ae_da.plot(y='altitude',ax=ax, label=ae_name, color=PLOT_INFO['ae2color'][ae_name])
            except:
                raise ValueError(f"Error plotting Angstrom exponent")
             
    #plot vertical line at zero
    ax.axvline(x=1, color='k', linestyle='--', linewidth='0.5')
    if ae_limits is not None:
        ax.set_xlim(ae_limits)
    else:
        ax.set_xlim(-1, 3)
    if range_limits is not None:
        ax.set_ylim(range_limits)
    ax.legend()
    ax.grid()
    ax.set_xlabel(r'$AE_{\beta}$, [#]')
    return ax

     