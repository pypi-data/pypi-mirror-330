from strataer.utils import interpolate_pressure_to_altitude
import pytest
import numpy as np
import xarray as xr


def cmip6_plev():
    return np.array(
        [
            100000.0,
            92500.0,
            85000.0,
            70000.0,
            60000.0,
            50000.0,
            40000.0,
            30000.0,
            25000.0,
            20000.0,
            15000.0,
            10000.0,
            7000.0,
            5000.0,
            3000.0,
            2000.0,
            1000.0,
            700.0,
            500.0,
            300.0,
            200.0,
            100.0,
        ]
    )


def generate_xarray(data):
    plev = cmip6_plev()
    lat = [1.395309]
    lon = [180.0]
    time = [np.datetime64("1979-01-16 12:00:00")]
    return xr.DataArray(
        np.expand_dims(data, axis=(0, 2, 3)),
        dims=["time", "plev", "lat", "lon"],
        coords=[time, plev, lat, lon],
    )


@pytest.fixture()
def geopotential_height():
    return generate_xarray(
        np.array(
            [
                51.514843,
                735.8145,
                1466.1454,
                3105.7039,
                4373.565,
                5832.229,
                7558.27,
                9679.323,
                10958.566,
                12448.173,
                14251.253,
                16592.805,
                18591.885,
                20608.094,
                23784.965,
                26412.266,
                31057.271,
                33488.508,
                35824.023,
                39550.445,
                42655.703,
                48064.65,
            ]
        )
    )


@pytest.fixture()
def temperature():
    return generate_xarray(
        np.array(
            [
                299.4967,
                294.4713,
                291.10654,
                283.17514,
                276.44437,
                268.63263,
                258.95068,
                244.29887,
                234.48796,
                221.64804,
                206.75763,
                189.84383,
                198.36491,
                208.87149,
                217.08853,
                224.71947,
                231.85716,
                233.88535,
                241.1477,
                257.46854,
                263.63553,
                269.30783,
            ]
        )
    )


def test_hypsometric_pressure(geopotential_height, temperature):
    """
    Test the hypsometric interpolation by iterating over zg, ta profiles and interpolating the known value.
    """

    diff_ln_pres = []
    diff = []
    for pidx, pressure in enumerate(temperature.plev.values[1:-1]):

        zg_temp = geopotential_height.where(geopotential_height.plev != pressure, drop=True)
        ta_temp = temperature.where(geopotential_height.plev != pressure, drop=True)

        alt = np.array([float(geopotential_height.sel(plev=pressure).values.squeeze())])
        int_pressure = interpolate_pressure_to_altitude(
            zg_temp, ta_temp, xr.DataArray(alt, dims="altitude", coords=[alt])
        )
        diff.append((int_pressure.values.squeeze() - pressure) / pressure * 100)

        # compute simple log-pressure space interpolation for comparison
        int_ln_pressure = np.exp(
            np.interp(alt, zg_temp.values.squeeze(), np.log(zg_temp.plev.values))
        )
        diff_ln_pres.append((int_ln_pressure - pressure) / pressure * 100)

    # Allow max error of 1%. Typically should be better but this can occur when the
    # tropopause is not sampled and it is difficult to estimate temperature
    assert np.all(np.abs(np.array(diff)) < 1.0)

    # On average hypsometric equation should provide improvement over log-pressure interpolation
    assert np.sum(np.array(diff) ** 2) < np.sum(np.array(diff_ln_pres) ** 2)
