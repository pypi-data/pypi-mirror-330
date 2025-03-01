import xarray as xr
import numpy as np
import pandas as pd
from strataer.utils.canesm import split_bands_to_separate_variables
from strataer.utils import (
    calculate_bounds_from_array,
    interpolate_pressure_to_altitude,
)
from strataer.utils import Regridder1D


def format_dims(ds: xr.Dataset) -> xr.Dataset:
    """format the EVA file to have the expected dimension names and formats

    Parameters
    ----------
    ds : xr.Dataset
        EVA dataset

    Returns
    -------
    xr.Dataset
        formatted EVA dataset
    """

    if "latitude" in ds.variables:
        ds = ds.rename({"latitude": "lat"})

    if "longitude" in ds.variables:
        ds = ds.rename({"longitude": "lon"})

    if "month" in ds.variables and "months since" in ds.month.attrs["units"]:
        start = ds.month.attrs["units"].split(" ")[-1].split("-")
        start = pd.Timestamp(f"{start[1]}-{start[0]}-{1}")
        time = np.array(
            [start + pd.DateOffset(months=i) for i in ds.month.values],
            dtype="datetime64[ns]",
        )
        ds = ds.assign(time=xr.DataArray(time, dims=["month"], coords=[ds.month.values]))
        ds = ds.swap_dims({"month": "time"}).reset_coords()

    return ds


def broadcast_longitude(
    ds: xr.Dataset,
    lon: np.ndarray | None = None,
    variables=["ext_sun", "ext_earth", "g_earth", "g_sun", "omega_earth", "omega_sun"],
) -> xr.Dataset:
    """_summary_

    Parameters
    ----------
    ds : xr.Dataset
        input dataset
    lon : np.ndarray | None, optional
        array of longitudes, by default None
    variables : list, optional
        list of variables to broadcast, by default ["ext_sun", "ext_earth", "g_earth", "g_sun", "omega_earth", "omega_sun"]

    Returns
    -------
    xr.Dataset
        dataset with variables broadcast on `lon`
    """
    # Return dataset with all of the radiation variables in the list variables
    # padded with a longitude coordinate

    if lon is None:
        lon = np.arange(30, 331, 60)

    lon = xr.DataArray(lon, dims="lon", coords=[lon])
    ds_with_lon = ds[variables].expand_dims(lon=lon)
    return xr.merge([ds.drop_vars(variables), ds_with_lon])


def add_lon_bnds(ds: xr.Dataset) -> xr.Dataset:
    """Add lat and lon bounds to a dataset

    Parameters
    ----------
    ds : xr.Dataset
        input dataset, should have `lat` and optionally `lon` coordinates.

    Returns
    -------
    xr.Dataset
        input dataset with bounds
    """

    if "lon" in ds.dims:
        lon_bnds = calculate_bounds_from_array(ds.lon, ndim=1)
    else:
        ds = ds.assign_coords({"lon": [0.0]})
        lon_bnds = xr.DataArray(
            np.array([[-180.0, 180.0]]),
            dims=["lon", "lon_bnds"],
            coords=[ds.lon.values, [0, 1]],
        )

    ds = ds.assign_coords(lon_bnds=lon_bnds)
    return ds


def add_lat_bnds(ds: xr.Dataset) -> xr.Dataset:
    lat_bnds = calculate_bounds_from_array(ds.lat, ndim=1)
    ds = ds.assign_coords(lat_bnds=lat_bnds)
    return ds


def interpolate_onto_gcm(ds: xr.Dataset, out_grid: xr.Dataset):
    """regrid optical dataset onto a new grid, using appropriate weights

    Parameters
    ----------
    ds : xr.Dataset
        input EVA dataset
    out_grid : xr.Dataset
        output grid

    Returns
    -------
    xr.Dataset
        EVA dataset on new grid
    """
    from xesmf import Regridder

    if "lon" in ds:
        regridder = Regridder
        ds = ds.rename({"lon_bnds": "lon_b", "lat_bnds": "lat_b"})
    else:
        regridder = Regridder1D
        if isinstance(out_grid, xr.DataArray):
            out_grid = out_grid.to_dataset()
        out_grid = add_lat_bnds(out_grid)

    regrid = regridder(
        ds,
        out_grid,
        method="conservative_normed",
        periodic=True,
    )

    ext_sun = regrid(ds.ext_sun)
    omega_weights = regrid(ds.omega_sun * ds.ext_sun)
    omega_sun = omega_weights / ext_sun
    g_sun = regrid(ds.omega_sun * ds.g_sun * ds.ext_sun) / omega_weights

    ext_earth = regrid(ds.ext_earth)
    omega_weights = regrid(ds.omega_earth * ds.ext_earth)
    omega_earth = omega_weights / ext_earth
    g_earth = regrid(ds.omega_earth * ds.g_earth * ds.ext_earth) / omega_weights

    out = xr.merge(
        [
            ext_sun.rename("ext_sun"),
            g_sun.rename("g_sun"),
            omega_sun.rename("omega_sun"),
            ext_earth.rename("ext_earth"),
            g_earth.rename("g_earth"),
            omega_earth.rename("omega_earth"),
        ]
    )
    return out


def eva_on_gcm_grid(eva: xr.Dataset, gcm_grid: xr.Dataset, broadcast_lon: bool = True):
    """Put EVA data onto GCM grid

    Parameters
    ----------
    eva_file : xr.Dataset
        EVA dataset
    gcm_grid : xr.Dataset
        GCM target grid

    Returns
    -------
    xr.Dataset
        EVA on GCM grid
    """
    eva = format_dims(eva)
    if broadcast_lon:
        eva = broadcast_longitude(eva)
        eva = add_lon_bnds(eva)
    eva = add_lat_bnds(eva)
    eva = interpolate_onto_gcm(eva, gcm_grid)
    return eva


def align_times(ds1: xr.Dataset, ds2: xr.Dataset, origin: str = "2020-01-01"):
    """Align times for ds2 onto ds1.time"""

    ds = []
    if "month" in ds2.dims:
        for time in ds1.time.values:
            temp = ds2.sel(month=pd.Timestamp(time).month)
            temp["time"] = time
            ds.append(temp)

        ds = xr.concat(ds, dim="time").reset_coords(drop=True)

    ds.time.attrs = {
        "units": f"days since {origin}",
        "calendar": "365_days",
        "long_name": "time",
    }

    return ds


def extend_start_end_timesteps(eva):

    new_start = pd.Timestamp(eva.time.values[0]) - pd.DateOffset(months=1)
    new_end = pd.Timestamp(eva.time.values[-1]) + pd.DateOffset(months=1)

    start = eva.isel(time=0)
    start["time"] = new_start.to_numpy()

    end = eva.isel(time=-1)
    end["time"] = new_end.to_numpy()

    return xr.concat([start, eva, end], dim="time")


def format_eva_variables_for_canesm(eva):
    output = eva.rename(
        {
            "pressure": "PRES",
            "ext_sun": "SWE",
            "g_sun": "SWG",
            "omega_sun": "SWS",
            "ext_earth": "LWE",
            "g_earth": "LWG",
            "omega_earth": "LWS",
            "altitude": "lev",
        }
    ).rename({"lat": "latitude"})

    ds = []
    for var in output:
        if "solar_bands" in output[var].dims:
            bands = "solar_bands"
        elif "terrestrial_bands" in output[var].dims:
            bands = "terrestrial_bands"
        else:
            continue
        ds.append(split_bands_to_separate_variables(output[var], bands))
    ds = xr.merge(ds)

    e055 = output.SWE.isel(solar_bands=-1).rename("E055")
    w055 = output.SWS.isel(solar_bands=-1).rename("W055")
    g055 = output.SWG.isel(solar_bands=-1).rename("G055")

    e110 = output.LWE.isel(terrestrial_bands=-1).rename("E110")
    w110 = output.LWS.isel(terrestrial_bands=-1).rename("W110")
    g110 = output.LWG.isel(terrestrial_bands=-1).rename("G110")

    return xr.merge([ds, e055, w055, g055, e110, w110, g110, output.PRES])


def shift_times(eva: xr.Dataset, n_years: int):
    times = np.array(
        [(pd.Timestamp(v) - pd.DateOffset(years=n_years)).to_numpy() for v in eva.time.values]
    )
    return eva.assign_coords(time=times)


def process_eva_for_canesm(
    eva,
    temperature,
    geopotential_height,
    outfile: str | None = None,
    zonal_ave: bool = False,
    time_ave: bool = False,
):

    if time_ave:
        temperature = temperature.groupby("time.month").mean()
        geopotential_height = geopotential_height.groupby("time.month").mean()

    if zonal_ave:
        temperature = temperature.mean(dim="lon")
        geopotential_height = geopotential_height.mean(dim="lon")

    eva = eva_on_gcm_grid(eva, temperature, broadcast_lon=not zonal_ave)
    pressure = interpolate_pressure_to_altitude(
        geopotential_height=geopotential_height,
        temperature=temperature,
        altitude=eva.altitude * 1000,
    )

    start_date = pd.Timestamp("1990-01-01")
    eva = shift_times(eva, 0)
    pressure = align_times(eva, pressure)
    output = xr.merge([eva, pressure.rename("pressure")])
    output = format_eva_variables_for_canesm(output)
    output = extend_start_end_timesteps(output)
    output: xr.Dataset = output.transpose("time", "lev", "latitude", ...)
    print("Saved pre-processed input file to temp location: {}".format(outfile))
    output.to_netcdf()
    output.load()
    output.to_netcdf(outfile)
    return output


if __name__ == "__main__":

    config = {
        "geopotential_height": r"/space/hall5/sitestore/eccc/crd/ccrn/users/jcl001/PROJECTS/VolRes-RE/inputs/zg_Amon_CanAM4_amip_r1i1p1_197901-200912.nc",
        "temperature": r"/space/hall5/sitestore/eccc/crd/ccrn/users/jcl001/PROJECTS/VolRes-RE/inputs/ta_Amon_CanAM4_amip_r1i1p1_197901-200912.nc",
        "pressure": r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/cccma_processing/EVA/pressure_Amon_CanAM4_amip_r1i1p1_197901-200912.nc",
    }

    # input = r"/space/hall5/sitestore/eccc/crd/ccrn/users/jcl001/PROJECTS/ESSDA_USASK/data/EVA/eva_forcing_CMIP6_ECHAM5_1990.nc"
    input = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/cccma_processing/EVA/input/eva_forcing_CMIP6_CanESM_1990-1996/*.nc"
    output = r"/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/cccma_processing/EVA/output/eva_forcing_CMIP6_CanESM_1990-1996/eva_forcing_VolRes-RE_CanESM_1990-1996_v1.nc"

    eva = xr.open_mfdataset(input, decode_times=False)
    temperature = xr.open_mfdataset(config["temperature"]).ta
    geopotential_height = xr.open_mfdataset(config["geopotential_height"]).zg

    # output = r'/space/hall5/sitestore/eccc/crd/ccrn/users/rlr001/canesm_runs/rlr-test-eva/data/ sc_rlr-test-eva_200501_200512_gp_ev55.001'
    # output = xr.open_mfdataset(output)
    process_eva_for_canesm(
        eva,
        temperature,
        geopotential_height,
        outfile=output,
        zonal_ave=True,
        time_ave=True,
    )

    final = xr.open_dataset(output)
