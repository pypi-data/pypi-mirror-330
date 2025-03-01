import yaml
import numpy as np
import xarray as xr
from pathlib import Path
from strataer.cmip7.convert_cmip7 import (
    interpolate_optics,
    planck_weights,
)
from strataer.utils import wavenumber_to_wavelength
from functools import partial
import os


def cli_run(config):
    """Interpolate the CMIP7 stratospheric aerosol forcing to new wavelength bands."""

    config = yaml.safe_load(open(config, "r"))
    folder = Path(config["input"]["folder"])

    for key, band in config["output"]["bands"].items():
        output_wavel_bnds = np.array(band["bounds"])
        units = band["units"]
        base_filename = config["input"]["base_filename"]
        if "model" in config["output"]:
            model = f'{config["output"]["model"]}_{key}'
        else:
            model = f"INTERPOLATED_{key}"

        if units == "cm-1":
            output_wavel_bnds = wavenumber_to_wavelength(output_wavel_bnds) * 1e-9
        if units == "nm":
            output_wavel_bnds = output_wavel_bnds * 1e-9

        source = band["source"]
        function_name = list(source.keys())[0]
        if function_name.lower() == "planck":
            weight_function = partial(planck_weights, **source[function_name])
        else:
            raise ValueError("only planck source function weighting is currently supported")

        wavelength = [(b[1] + b[0]) / 2 for b in output_wavel_bnds]
        output_wavel_bnds = xr.DataArray(
            np.array(output_wavel_bnds),
            dims=["wavelength", "bnds"],
            coords=[wavelength, [0, 1]],
        )

        output_folder = Path(config["output"]["folder"])
        os.makedirs(output_folder, exist_ok=True)
        new_base = base_filename.replace("UOEXETER", model)

        print(f"converting {key} optics")
        ext, ssa, asy = interpolate_optics(
            folder,
            output_wavel_bnds,
            base_filename=base_filename,
            weight_function=weight_function,
            subsample_wavelengths=None,
        )

        for ds, var in zip([ext, ssa, asy], ["ext", "ssa", "asy"]):
            ds.to_netcdf(output_folder / f"{var}_{new_base}")


if __name__ == "__main__":
    cli_run(
        Path(
            r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/software/cmip7-strat-aerosol/config.yaml"
        )
    )
