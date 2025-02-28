import numpy as np
import xarray as xr
from scipy.constants import Boltzmann

from gfatpy.atmo import atmo, ecmwf
from gfatpy.atmo.rayleigh import molecular_properties
from gfatpy.lidar.utils.types import ParamsDict
from gfatpy.lidar.utils.utils import extrapolate_beta_with_angstrom
from gfatpy.lidar.utils.utils import sigmoid


def generate_particle_properties(
    ranges: np.ndarray,
    wavelength: float,
    ae: float | tuple[float, float] = (1.5, 0),
    lr: float | tuple[float, float] = (75, 45),
    synthetic_beta: float | tuple[float, float] = (2.5e-6, 2.0e-6),
    sigmoid_edge: float | tuple[float, float] = (2500, 5000),
) -> np.ndarray:
    """_summary_

    Args:
        ranges (np.ndarray): ranges
        wavelength (float): wavelength
        fine_ae (float): fine-mode Angstrom exponent
        coarse_ae (float): coarse-mode Angstrom exponent
        fine_beta532 (float, optional): fine-mode backscatter coefficient at 532 nm. Defaults to 2.5e-6.
        coarse_beta532 (float, optional): coarse-mode backscatter coefficient at 532 nm. Defaults to 2.0e-6.

    Returns:
        np.ndarray: particle backscatter coefficient profile
    """
    if isinstance(ae, tuple):
        fine_ae = ae[0]
        coarse_ae = ae[1]
    else:
        fine_ae = ae
        coarse_ae = ae

    if isinstance(lr, tuple):
        fine_lr = lr[0]
        coarse_lr = lr[1]
    else:
        fine_lr = lr
        coarse_lr = lr

    if isinstance(sigmoid_edge, tuple):
        sigmoid_edge_fine = sigmoid_edge[0]
        sigmoid_edge_coarse = sigmoid_edge[1]
    else:
        sigmoid_edge_fine = sigmoid_edge
        sigmoid_edge_coarse = sigmoid_edge

    if isinstance(synthetic_beta, tuple):
        fine_beta532 = synthetic_beta[0]
        coarse_beta532 = synthetic_beta[1]
    else:
        fine_beta532 = synthetic_beta
        coarse_beta532 = synthetic_beta

    beta_part_fine_532 = sigmoid(
        ranges, sigmoid_edge_fine, 1 / 60, coeff=-fine_beta532, offset=fine_beta532
    )
    beta_part_coarse_532 = sigmoid(
        ranges,
        sigmoid_edge_coarse,
        1 / 60,
        coeff=-coarse_beta532,
        offset=coarse_beta532,
    )

    beta_part_fine = extrapolate_beta_with_angstrom(
        beta_part_fine_532, 532, wavelength, fine_ae
    )

    beta_part_coarse = extrapolate_beta_with_angstrom(
        beta_part_coarse_532, 532, wavelength, coarse_ae
    )

    beta_total = beta_part_fine + beta_part_coarse

    alpha_part_fine = fine_lr * beta_part_fine
    alpha_part_coarse = coarse_lr * beta_part_coarse

    alpha_total = alpha_part_fine + alpha_part_coarse

    return (
        beta_part_fine,
        beta_part_coarse,
        beta_total,
        alpha_part_fine,
        alpha_part_coarse,
        alpha_total,
    ) # type: ignore


def synthetic_signals(
    ranges: np.ndarray,
    wavelengths: float | tuple[float, float] = 532,
    overlap_midpoint: float = 800,
    k_lidar: float | tuple[float, float] = (1e10, 1e9),
    ae: float | tuple[float, float] = (1.5, 0),
    lr: float | tuple[float, float] = (75, 45),
    synthetic_beta: float | tuple[float, float] = (2.5e-6, 2.0e-6),
    sigmoid_edge: float | tuple[float, float] = (2500, 5000),
    force_zero_aer_after_bin: int | None = None,
    paralell_perpendicular_ratio: float = 0.33,
    meteo_profiles: tuple[np.ndarray, np.ndarray] | None = None,
    apply_overlap: bool = True,
) -> tuple[np.ndarray, np.ndarray | None, ParamsDict]:
    """It generates synthetic lidar signal.

    Args:
        ranges (np.ndarray): Range
        wavelength (float, optional): Wavelength. Defaults to 532.
        overlap_midpoint (float, optional): _description_. Defaults to 600.
        k_lidar (float, optional): Lidar constant calibration. Defaults to 4e9.
        wavelength_raman (float | None, optional): Raman wavelength. Defaults to None. If None, signal is elastic.
        paralell_perpendicular_ratio (float, optional): _description_. Defaults to 0.33.
        particle_lratio (float, optional): _description_. Defaults to 45.
        force_zero_aer_after_bin (int | None, optional): _description_. Defaults to None.

    Returns:
        tuple[np.ndarray, ParamsDict]: _description_
    """

    z = ranges.astype(np.float64)

    # Overlap
    if apply_overlap:
        overlap = sigmoid(
            z.astype(np.float64),
            overlap_midpoint,
            1 / 150.,
            offset=0.,
        )

        # overlap[overlap < 9e-3] = 0
        # overlap[overlap > 0.999] = 1
    else:
        overlap = np.ones_like(z)

    if isinstance(lr, float):
        lr = (lr, lr)
    if isinstance(ae, float):
        ae = (ae, ae)
    if isinstance(synthetic_beta, float):
        synthetic_beta = (synthetic_beta, synthetic_beta)

    if isinstance(k_lidar, float):
        k_lidar_elastic = k_lidar
    else:
        k_lidar_elastic, k_lidar_raman = k_lidar

    # Check temperature and pressure profiles
    if meteo_profiles is None:
        # ecmwf_data = ecmwf.get_ecmwf_temperature_pressure(datetime(2022, 9, 3), heights=z)
        # P = ecmwf_data.pressure.values
        # T = ecmwf_data.temperature.values
        P, T, _ = atmo.standard_atmosphere(z)
    else:
        # check length of meteo_profiles with z
        if len(meteo_profiles[0]) != len(z):
            raise ValueError("Length of meteo_profiles must be equal to length of z")
        else:
            P = meteo_profiles[0]
            T = meteo_profiles[1]

    # Check if wavelength is a tuple
    if isinstance(wavelengths, tuple):
        wavelength = wavelengths[0]
        wavelength_raman = wavelengths[1]
    else:
        wavelength = wavelengths
        wavelength_raman = None

    # Generate molecular profiles for elastic wavelength
    mol_properties = molecular_properties(532, P, T, heights=z)
    
    # TODO
    # Particle elastic
    # 0.33 para polvo desértico
    # 0.0034 para parte molecular
    # Calcular beta_part parallel = total*(1-0.33)
    # Calcular beta_part perpendicular = total*(0.33)
    # Análogo con otro coeficiente para la parte molecular

    # beta_part_fine, beta_part_coarse, beta_total, alpha_part_fine, alpha_part_coarse, alpha_total
    (
        _,
        _,
        beta_part,
        alpha_part_fine,
        alpha_part_coarse,
        alpha_part,
    ) = generate_particle_properties(
        ranges, wavelength, ae=ae, lr=lr, synthetic_beta=synthetic_beta, sigmoid_edge=sigmoid_edge
    )

    # Elastic transmittance
    # T_elastic = np.exp(-cumulative_trapezoid(alpha_mol+ alpha_part, z, initial=0))  # type: ignore
    T_elastic = atmo.transmittance(mol_properties["molecular_alpha"] + alpha_part, z)
    # Elastic signal
    P_elastic = (
        k_lidar_elastic
        * (overlap / z**2)
        * (mol_properties["molecular_beta"] + beta_part)
        * T_elastic**2
    )

    clean_attenuated_molecular_beta = (
        mol_properties["molecular_beta"]
        * atmo.transmittance(mol_properties["molecular_alpha"], z) ** 2
    )

    # Save parameters to create synthetic elastic signal
    params: ParamsDict = {
        "particle_beta": beta_part,
        "particle_alpha": alpha_part,
        "molecular_beta": mol_properties["molecular_beta"],
        "molecular_alpha": mol_properties["molecular_alpha"],
        "lidar_ratio": lr,
        "attenuated_molecular_backscatter": clean_attenuated_molecular_beta,
        "transmittance_elastic": T_elastic,
        "overlap": overlap,
        "k_lidar": k_lidar,
        "particle_angstrom_exponent": ae,
        "synthetic_beta": synthetic_beta,
        "temperature": T,
        "pressure": P,
    } # type: ignore

    # Raman signal
    if wavelength_raman is not None:
        # Generate molecular profiles for raman wavelength
        mol_properties_raman = molecular_properties(wavelength_raman, P, T, heights=z)

        # Alpha particle raman
        alpha_part_fine_raman = alpha_part_fine * (wavelength_raman / wavelength) ** (
            -ae[0]
        )
        alpha_part_coarse_raman = alpha_part_coarse * (
            wavelength_raman / wavelength
        ) ** (-ae[1])
        alpha_part_raman = alpha_part_fine_raman + alpha_part_coarse_raman

        # Transmittance Raman
        # T_raman = np.exp(-cumulative_trapezoid(alpha_mol_raman + alpha_part_raman, z, initial=0))  # type: ignore
        T_raman = atmo.transmittance(
            mol_properties_raman["molecular_alpha"] + alpha_part_raman, z
        )
        P_raman = (
            k_lidar_raman
            * (overlap / z**2)
            * mol_properties_raman["molecular_beta"]
            * T_elastic
            * T_raman
        )

        clean_attenuated_molecular_beta_raman: xr.DataArray = (
            mol_properties_raman["molecular_beta"]
            * atmo.transmittance(mol_properties_raman["molecular_alpha"], z)
            * atmo.transmittance(mol_properties["molecular_alpha"], z)
        ) # type: ignore

        params["molecular_alpha_raman"] = mol_properties_raman["molecular_alpha"] # type: ignore
        params["molecular_beta_raman"] = mol_properties_raman["molecular_beta"] # type: ignore
        params["attenuated_molecular_backscatter_raman"] = (
            clean_attenuated_molecular_beta_raman, 
        ) # type: ignore
        params["transmittance_raman"] = T_raman
        params["overlap"] = overlap

    else:
        P_raman = None

    if force_zero_aer_after_bin is not None:
        alpha_part[force_zero_aer_after_bin:] = 0
        beta_part[force_zero_aer_after_bin:] = 0
    return P_elastic, P_raman, params
