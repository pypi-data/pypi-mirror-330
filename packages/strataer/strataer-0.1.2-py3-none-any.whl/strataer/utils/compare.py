import matplotlib.pyplot as plt
from pathlib import Path
import xarray as xr
import numpy as np
from strataer.utils.physics import planck

plt.style.use(
    r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/software/ht-paper/ht-paper.mplstyle"
)

folder = Path(
    r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/data/cmip/input/strat_aerosol/v1.3"
)
model_folder = "canesm"
model = "CanESM"

fields = {
    "ext": "Extinction [m$^{-1}$]",
    "asy": "Asymmetry Factor",
    "ssa": "Single Scattering Albedo",
}

for var in fields:
    files = {
        "original": [
            folder
            / f"{var}_input4MIPs_aerosolProperties_CMIP_UOEXETER-CMIP-1-3-0_gnz_175001-202312.nc"
        ],
        "weighted": list(
            (folder / model_folder / "weighted").glob(
                f"{var}_input4MIPs_aerosolProperties_CMIP_{model}_*-CMIP-1-3-0_gnz_175001-202312.nc"
            )
        ),
        # "weighted-ben": list(
        #     (folder / "UKESM" / "weighted-ben").glob(f"{var}_*_CMIP7_interpolated.nc")
        # ),
        "interpolated": list(
            (folder / model_folder / "linear").glob(f"{var}_*_CMIP7_interpolated.nc")
        ),
    }

    time = "2021-12-01"
    height = 22000.0
    lat = 0

    data = {}
    for key, file in files.items():
        # need to manually concatenate non-monotonic wavelength datasets
        tmp = xr.concat(
            [
                xr.open_mfdataset(f)
                .sel(height=slice(0, 40000))
                .sel(lat=slice(-90, 90))
                .sel(time=slice("2021-12-01", "2021-12-31"))
                .sortby("wavelength")
                for f in file
            ],
            dim="wavelength",
        ).sortby("wavelength")
        data[key] = tmp.sel(lat=lat, height=height, method="nearest").sel(time=time)
        # data[key] = (tmp * np.cos(tmp.lat * np.pi / 180)).sum(dim="lat") / np.sum(
        #     np.cos(tmp.lat.values * np.pi / 180)
        # )

    fig, ax = plt.subplots(2, 1, figsize=(4, 4), sharex=True)
    fig.subplots_adjust(left=0.14, bottom=0.09, top=0.96, right=0.97, hspace=0.02)
    for key, ds in data.items():
        ax[0].plot(ds.wavelength.values, ds[var].values, marker=".", label=key)

    for w in ["weighted"]:
        percent = False
        if var == "ext":
            diff = (data[w][var] - data["interpolated"][var]) / data[w][var] * 100
            percent = True
        else:
            diff = data[w][var] - data["interpolated"][var]
        ax[1].plot(diff.wavelength.values, diff.values, marker=".", label=w)

    ax[1].legend()
    ax[0].set_title(fields[var])
    ax[0].set_ylabel(fields[var])
    ax[1].set_ylabel(f"Difference (weighted - interp){' [%]' if percent else ''}")
    ax[0].set_xscale("log")
    if percent:
        ax[0].set_yscale("log")
    else:
        ax[0].set_yscale("linear")
    # ax[1].set_yscale('log')
    ax[1].set_xlabel("Wavelength [nm]")
    ax[0].legend()
    fig.savefig(f"compare_methods_{var}-{model}-nosubsample.png", dpi=450)
