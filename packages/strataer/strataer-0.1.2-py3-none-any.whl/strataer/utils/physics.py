import numpy as np
from scipy.interpolate import interp1d
import xarray as xr


def hypsometric_pressure(
    geopotential_height: np.ndarray,
    temperature: np.ndarray,
    plev: np.ndarray,
    altitude: np.ndarray,
):
    """Compute the pressure at altitude levels useing the hypsometric equation

    Parameters
    ----------
    geopotential_height : np.ndarray
        geopotential height in meters. Should be strictly increasing.
    temperature : np.ndarray
        temperature in kelvin
    plev : np.ndarray
        pressure levels corresonding to geopotential and temperature arrays
    altitude : np.ndarray
        output altitude grid in meters

    Returns
    -------
    np.ndarray
        1D array of pressure at altitude
    """

    g_over_R = 0.034163043478260866  # gravity / gas_constant = 9.80616/287.04

    # get the temperature at the altitudes of interest
    # temp_on_alt = np.interp(altitude, geopotential_height, temperature)
    temp_on_alt = interp1d(geopotential_height, temperature, kind="cubic")(altitude)

    # index of zg just below altitude
    # TODO: better to use the nearest?
    idx = np.digitize(altitude, geopotential_height) - 1

    return plev[idx] * np.exp(
        g_over_R / ((temperature[idx] + temp_on_alt) / 2) * (geopotential_height[idx] - altitude)
    )


def interpolate_pressure_to_altitude(
    geopotential_height: xr.DataArray, temperature: xr.DataArray, altitude: xr.DataArray
) -> xr.DataArray:
    """Interpolate pressure at a given altitude using the hypsometric equation

    Parameters
    ----------
    geopotential_height : xr.DataArray
        geopotential height [m]
    temperature : xr.DataArray
        temperature [k]
    altitude : xr.DataArray
        altitude [m]

    Returns
    -------
    xr.DataArray
        pressure at altitude levels
    """

    # TODO: avoid load call - required for now since data isn't chunked by altitude so single altitudes are passed without load.
    return xr.apply_ufunc(
        hypsometric_pressure,
        geopotential_height.load(),
        temperature.load(),
        geopotential_height.plev,
        altitude,
        input_core_dims=[["plev"], ["plev"], ["plev"], ["altitude"]],
        output_core_dims=[["altitude"]],
        vectorize=True,
    )


def planck(wavelength: float | np.ndarray, temperature: float):
    """compute the planck function at a given wavelength [m] and temperature [K]

    Parameters
    ----------
    wavelength : float | np.ndarray
        wavelength in meters
    temperature : float
        blackbody temperature in kelvin.

    Returns
    -------
    float | np.ndarray
    """
    h = 6.626070156e-34  # Js
    c = 299792458.0  # m/s
    k = 1.380649e-23  # J

    a = 2 * h * c**2
    b = h * c / (wavelength * k * temperature)
    return a / ((wavelength**5) * (np.exp(b) - 1))


def wavenumber_to_wavelength(wavenumber):
    return 1e7 / wavenumber
