from pathlib import Path
from gfatpy.utils.io import read_yaml

SCC_PLOT_INFO = read_yaml(Path(__file__).parent.absolute() / "info.yml")
PLOT_INFO = read_yaml(Path(__file__).parent.parent.parent.absolute() / "plot" / "info.yml")

__all__ = ["SCC_PLOT_INFO", "PLOT_INFO"]
