from datetime import datetime
from pathlib import Path
import xarray as xr 

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import numpy as np

from gfatpy.radar.rpg_nc import rpg
from gfatpy.utils.utils import parse_datetime


class nebula():
    def __init__(self, ka_nc_path: Path, ww_nc_path: Path):
        self.ka = rpg(ka_nc_path)
        self.ww = rpg(ww_nc_path)        
        self._level = None
        self.nb = self.ka
        self.nb._data = None

    @property
    def level(self) -> int:
        if self.ka.level != self.ww.level:
            raise ValueError("Ka- and W-band measurement levels do not match.")        
        self._level = self.ka.level
        return self._level

    @property
    def data(self) -> xr.Dataset:
        if self.level == 1:
            if self.nb._data is None:
                _data = self.ka.data.copy()
                _data["DWR"] = 10 * np.log10(self.ka.data["Ze"] / self.ww.data["Ze"])
                _data["DWR"].attrs["units"] = "dB"
                _data["DWR"].attrs["long_name"] = "Ka-W DWR"

                _data["DDV"] = self.ka.data["v"] - self.ww.data["v"]
                _data["DDV"].attrs["units"] = "m/s"
                _data["DDV"].attrs["long_name"] = "Ka-W DDV"
            else:
                _data = self.nb._data
        return _data

    def quicklook(self, variable: str | list[str] | None = None, **kwargs):
        self.ka.quicklook(variable, **kwargs)
        self.ww.quicklook(variable, **kwargs)

    def plot_profile(
        self,
        target_time: datetime | np.datetime64,
        range_limits: tuple[float, float],
        variable: str | list[str] | None = None,
        **kwargs,
    ) -> tuple[Figure, Path | None]:
        _kwargs = kwargs.copy()        
        _kwargs["savefig"] = False
        _kwargs["color_list"] = [kwargs.get("ka_color", "red")]

        if variable is None:
            variables = [str(var) for var in self.ka.data.variables.keys()]
        if isinstance(variable, str):
            variables = [variable]
        elif isinstance(variable, list):
            variables = variable

        for variable_ in variables:
            fig1, _ = self.ka.plot_profile(
                target_times=target_time,
                range_limits=range_limits,
                variable=variable_,
                **_kwargs,
            )

            _kwargs["fig"] = fig1
            _kwargs["color_list"] = [kwargs.get("w_color", "blue")]
            
            fig, _ = self.ww.plot_profile(
                target_times=target_time,
                range_limits=range_limits,
                variable=variable_,
                **_kwargs,
            )

            ka_line, w_line = fig.findobj(Line2D)[0], fig.findobj(Line2D)[1]
            ka_line.set_label(f"Ka-band")
            w_line.set_label(f"W-band")

            ax = fig.get_axes()[0]
            ax.legend()

            if kwargs.get("savefig", False):
                filepath = (
                    kwargs.get("output_dir", Path.cwd())
                    / f"profile_{variable_}_{target_time:%Y%m%dT%H%M%S}.png"
                )
                fig.savefig(filepath, dpi=kwargs.get("dpi", 300))
        return fig, filepath

    def plot_timeseries(
        self,
        target_range: float,
        time_limits: tuple[datetime | np.datetime64, datetime | np.datetime64] | None = None,
        variable: str | None = None,
        **kwargs,
    ) -> tuple[Figure, Path | None]:
        
        _kwargs = kwargs.copy()        
        _kwargs["savefig"] = False
        _kwargs["color_list"] = [kwargs.get("ka_color", "red")]

        if  time_limits is None:
            time_limits = (parse_datetime(self.ka.data.time[0].values), parse_datetime(self.ka.data.time[-1].values))

        fig1, _ = self.ka.plot_timeseries(
            target_ranges=target_range,
            time_limits=time_limits,
            variable=variable,
            **_kwargs,
        )

        _kwargs["fig"] = fig1
        _kwargs["color_list"] = [kwargs.get("w_color", "blue")]
        fig, _ = self.ww.plot_timeseries(
            target_ranges=target_range,
            time_limits=time_limits,
            variable=variable,
            **_kwargs,
        )

        ka_line, w_line = fig.findobj(Line2D)[0], fig.findobj(Line2D)[1]
        ka_line.set_label(f"Ka-band")
        w_line.set_label(f"W-band")

        ax = fig.get_axes()[0]
        variable_string = self.ka.data[variable].attrs['long_name'].replace('W-band','').replace("Ka-band",'')
        ax.set_ylabel(f"{variable_string}, [{self.ka.data[variable].attrs['units']}]")
        ax.legend()

        if kwargs.get("savefig", False):
            filepath = (
                kwargs.get("output_dir", Path.cwd())
                / f"timeseries_{variable}_{time_limits[0]:%Y%m%dT%H%M%S}_{time_limits[-1]:%Y%m%dT%H%M%S}_{target_range}.png"
            )
            fig.savefig(filepath, dpi=kwargs.get("dpi", 300))
        return fig, filepath


    def plot_spectrum(
        self, target_time: datetime | np.datetime64, target_range: float, **kwargs
    ) -> tuple[Figure, Path | None]:
        _kwargs = kwargs.copy()
        _kwargs.pop("output_dir")
        _kwargs.pop("savefig")
        _kwargs["color"] = kwargs.get("ka_color", "red")
        fig, _ = self.ka.plot_spectrum(target_time, target_range, **_kwargs)

        _kwargs["fig"] = fig
        _kwargs["color"] = kwargs.get("w_color", "blue")
        fig, _ = self.ww.plot_spectrum(target_time, target_range, **_kwargs)
        ka_line, w_line = fig.findobj(Line2D)[0], fig.findobj(Line2D)[2]
        ka_line.set_label(f"Ka-band {ka_line.get_label()}")
        w_line.set_label(f"W-band {w_line.get_label()}")

        ax = fig.get_axes()[0]
        ax.legend()

        if kwargs.get("savefig", False):
            filepath = (
                kwargs.get("output_dir", Path.cwd())
                / f"{target_time:%Y%m%dT%H%M%S}_{target_range:.0f}_spectrum.png"
            )
            fig.savefig(filepath, dpi=kwargs.get("dpi", 300))

        return fig, filepath
