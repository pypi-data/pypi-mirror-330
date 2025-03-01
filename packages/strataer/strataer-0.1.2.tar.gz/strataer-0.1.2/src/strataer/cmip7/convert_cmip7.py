import xarray as xr
import numpy as np
from typing import Callable
from pathlib import Path
from strataer.utils import regridding_weights, planck, linear_weight, calculate_bounds_from_array


BASE_FILENAME = "input4MIPs_aerosolProperties_CMIP_UOEXETER-CMIP-1-3-0_gnz_175001-202312.nc"
clim_filename = "input4MIPs_aerosolProperties_CMIP_UOEXETER-CMIP-1-3-0_gnz_185001-202112-clim.nc"


def planck_weights(
    wavelength_1: float | np.ndarray, wavelength_2: float | np.ndarray, temperature: float
) -> float | np.ndarray:
    """
    compute the area under of the plank curve between wavelength_1 and wavelength_2.
    If inputs are numpy arrays they should be of the same size.
    """
    if isinstance(wavelength_2, np.ndarray) and isinstance(wavelength_1, np.ndarray):
        weights = []
        for w1, w2 in zip(wavelength_1, wavelength_2):
            wavel = np.sort(np.linspace(w1, w2, 1000).flatten())
            weights.append(np.trapezoid(planck(wavel, temperature), wavel))
        return np.array(weights)
    else:
        wavel = np.sort(np.linspace(wavelength_1, wavelength_2, 1000).flatten())
        return np.trapezoid(planck(wavel, temperature), wavel)


def solar_planck_weights(wavelength_1: float | np.ndarray, wavelength_2: float | np.ndarray):
    return planck_weights(wavelength_1=wavelength_1, wavelength_2=wavelength_2, temperature=5777.0)


def terrestrial_planck_weights(wavelength_1: float | np.ndarray, wavelength_2: float | np.ndarray):
    return planck_weights(wavelength_1=wavelength_1, wavelength_2=wavelength_2, temperature=254.356)


def interpolation_wavelengths(bounds: np.ndarray, wavelengths_per_band: int = 30):
    # return None
    wavels = []
    for start, end in bounds:
        wavels.append(np.geomspace(start, end, wavelengths_per_band))
    return np.sort(np.unique(np.array(wavels).flatten()))


def open_variable(file: Path, interp_wavelength: np.ndarray | None = None):
    """

    Parameters
    ----------
    file : Path
        path to the netcdf file
    interp_wavelength : np.ndarray | None, optional
        if provided, interpolate the variables onto the new wavelength grid, by default None

    Returns
    -------
    _type_
        _description_
    """
    data = xr.open_mfdataset(file)

    if interp_wavelength is not None:
        data = data.interp(wavelength=interp_wavelength)
        bounds = calculate_bounds_from_array(
            xr.DataArray(
                interp_wavelength,
                dims="wavelength",
                coords=[interp_wavelength],
                name="wavelength_bnds",
            )
        )
        data["wavelength_bnds"].values = bounds.values

    return data


def wavel_interpolation_weights(
    input_wavel_bnds: xr.DataArray,
    output_wavel_bnds: xr.DataArray,
    input_wavel: xr.DataArray = None,
    output_wavel: xr.DataArray = None,
    weight_function: Callable = solar_planck_weights,
) -> xr.DataArray:
    """
    Determine the wavelength interpolation matrix given an input and output grid.

    Parameters
    ----------
    input_wavel_bnds : xr.DataArray
        wavelength bounds of input grid
    output_wavel_bnds : xr.DataArray
        wavelength bounds of output grid
    input_wavel : xr.DataArray, optional
        midpoints of input grid, by default None and will be calculated from the bounds.
    output_wavel : xr.DataArray, optional
        midpoints of output grid, by default None and will be calculated from the bounds.

    Returns
    -------
    xr.DataArray
        2d matrix of weights
    """

    input_bounds = input_wavel_bnds.values
    output_bounds = output_wavel_bnds.values
    weights = regridding_weights(input_bounds, output_bounds, weight_function=weight_function)

    if input_wavel is None:
        input_wavel = input_bounds[0:-1] + np.diff(input_bounds) / 2

    if output_wavel is None:
        output_wavel = output_bounds[0:-1] + np.diff(output_bounds) / 2

    return xr.DataArray(
        weights,
        dims=["new_wavelength", "wavelength"],
        coords=[output_wavel, input_wavel],
    )


def interpolate_optics(
    folder: Path,
    output_wavel_bnds: xr.DataArray,
    base_filename: str = BASE_FILENAME,
    weight_function: Callable[[float, float], float] = solar_planck_weights,
    subsample_wavelengths: int | None = None,
) -> tuple[xr.Dataset]:
    """interoplate the extinction, single scattering albedo and asymmetry
    parameters from the native grid onto `output_wavel_bands`

    Parameters
    ----------
    folder : Path
        path to folder containing the input files
    output_wavel_bnds : xr.DataArray
        wavelength bands of the output datasets
    base_filename : str, optional
        partial string of the input filenames, by default BASE_FILENAME
    weight_function : _type_, optional
        function that computes the weight of a band given its edges, by default uses planck weighting
    subsample_wavelengths : int | None, optional
        If provided interpolate the input dataset onto a higher resolution grid for more accurate weighting.
        Input dataset is subdivided into `subsample_wavelengths` for each output bin. By default None

    Returns
    -------
    tuple[xr.Dataset]
        extinction, single scatter albedo and asymmetry factor datasets
    """

    interp_wavelength = None
    if subsample_wavelengths is not None:
        interp_wavelength = interpolation_wavelengths(
            output_wavel_bnds.values, wavelengths_per_band=subsample_wavelengths
        )

    ext = open_variable(
        file=folder / f"ext_{base_filename}",
        interp_wavelength=interp_wavelength,
    )

    ssa = open_variable(
        file=folder / f"ssa_{base_filename}",
        interp_wavelength=interp_wavelength,
    )

    asy = open_variable(
        file=folder / f"asy_{base_filename}",
        interp_wavelength=interp_wavelength,
    )

    w = wavel_interpolation_weights(
        ext.wavelength_bnds,
        output_wavel_bnds,
        ext.wavelength.values,
        output_wavel_bnds.wavelength.values,
        weight_function=weight_function,
    )

    print("\tconverting extinction")
    ext_new = (ext.ext @ w).rename({"new_wavelength": "wavelength"})
    ext_new = xr.merge([ext_new.rename("ext"), asy[["time_bnds", "lat_bnds", "height_bnds"]]])
    ext_new.attrs = ext.attrs

    print("\tconverting single scatter albedo")
    weights = ext.ext
    ssa_new = (((ssa.ssa * weights) @ w) / (weights @ w)).rename({"new_wavelength": "wavelength"})
    ssa_new = xr.merge([ssa_new.rename("ssa"), ssa[["time_bnds", "lat_bnds", "height_bnds"]]])
    ssa_new.attrs = ssa.attrs

    print("\tconverting asymmetry factor")
    weights = ext.ext * ssa.ssa
    asy_new = (((asy.asy * weights) @ w) / (weights @ w)).rename({"new_wavelength": "wavelength"})
    asy_new = xr.merge([asy_new.rename("asy"), asy[["time_bnds", "lat_bnds", "height_bnds"]]])
    asy_new.attrs = asy.attrs

    return ext_new, ssa_new, asy_new
