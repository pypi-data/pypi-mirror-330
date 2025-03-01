from strataer.cmip7.convert_cmip7 import interpolate_asy, interpolate_ext, interpolate_ssa
from strataer.utils import wavenumber_to_wavelength
from pathlib import Path
import numpy as np
import xarray as xr


def solar_bands():
    return xr.DataArray(
        wavenumber_to_wavelength(
            np.array([(50000, 14500), (14500, 8400), (8400, 4200), (4200, 2500)])
        ),
        dims=["wavelength", "bnds"],
        coords=[[444.82758621, 940.06568144, 1785.71428571, 3190.47619048], [0, 1]],
    )


def terrestrial_bands():
    return xr.DataArray(
        wavenumber_to_wavelength(
            np.array(
                [
                    (2200, 2500),
                    (1900, 2200),
                    (1400, 1900),
                    (1100, 1400),
                    (980, 1100),
                    (800, 980),
                    (540, 800),
                    (340, 540),
                    (10, 340),
                ]
            )
        ),
        dims=["wavelength", "bnds"],
        coords=[
            [
                4272.72727273,
                4904.3062201,
                6203.0075188,
                8116.88311688,
                9647.49536178,
                11352.04081633,
                15509.25925926,
                23965.1416122,
                58823.529411764706,
            ],
            [0, 1],
        ],
    )


def split_bands_to_separate_variables(var: xr.DataArray, bands: str):
    ds = []
    for band in var[bands].values:
        ds.append(var.isel({bands: band}).rename(f"{var.name}{int(band + 1)}"))
    return xr.merge(ds)


def interpolate_to_new_wavelengths(folder, output_wavel_bnds: xr.DataArray) -> tuple[xr.DataArray]:

    ext = interpolate_ext(folder, output_wavel_bnds)
    asy = interpolate_asy(folder, output_wavel_bnds)
    ssa = interpolate_ssa(folder, output_wavel_bnds)
    return ext, asy, ssa


def process_for_canesm(folder, output_wavel_bnds: xr.DataArray):
    ext, asy, ssa = interpolate_to_new_wavelengths(folder, output_wavel_bnds)
    data = xr.merge([ext.rename("SWE"), asy.rename("SWG"), ssa.rename("SWS")])
    data = split_bands_to_separate_variables(data, bands="wavelength")


if __name__ == "__main__":
    folder = Path(
        r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/data/cmip/input/strat_aerosol/v1.3"
    )
    output_wavel_bnds = solar_bands()
    output_wavel_bnds["wavelength"] = output_wavel_bnds["wavelength"] * 1e-9
    output_wavel_bnds *= 1e-9
    interpolate_to_new_wavelengths(folder=folder, output_wavel_bnds=output_wavel_bnds)
