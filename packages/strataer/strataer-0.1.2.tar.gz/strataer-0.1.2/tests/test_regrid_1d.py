import pytest
import numpy as np
import xarray as xr
from strataer.utils import Regridder1D, regridding_weights


@pytest.fixture()
def input_ds():
    lat_bnds = np.linspace(-90, 90, 20)
    lat = lat_bnds[0:-1] + np.diff(lat_bnds) / 2
    alt = np.arange(5.5, 30.5, 1.0)
    return xr.Dataset(
        {"temperature": (["lat", "altitude"], np.ones((len(lat), len(alt))))},
        coords={"lat": lat, "altitude": alt, "lat_bnds": lat_bnds},
    )


@pytest.fixture()
def output_ds():
    lat_bnds = np.linspace(-90, 90, 30)
    lat = lat_bnds[0:-1] + np.diff(lat_bnds) / 2
    alt = np.arange(5.5, 30.5, 1.0)
    return xr.Dataset(
        {"temperature": (["lat", "altitude"], np.ones((len(lat), len(alt))))},
        coords={"lat": lat, "altitude": alt, "lat_bnds": lat_bnds},
    )


def test_half_input():
    # input  |  |  |  |  |  |  |
    # output |     |     |     |
    input_lat_bnds = np.arange(-90, 91, 5)
    output_lat_bnds = np.arange(-90, 91, 10)
    weights = regridding_weights(input_lat_bnds, output_lat_bnds)
    assert weights @ np.ones(len(input_lat_bnds) - 1) == pytest.approx(1)


def test_double_input():
    # input  |     |     |     |
    # output |  |  |  |  |  |  |
    input_lat_bnds = np.arange(-90, 91, 10)
    output_lat_bnds = np.arange(-90, 91, 5)
    weights = regridding_weights(input_lat_bnds, output_lat_bnds)
    assert weights @ np.ones(len(input_lat_bnds) - 1) == pytest.approx(1)


def test_unequal_to_higher():
    # input  |    |     |      |
    # output |  |  |  |  |  |  |
    input_lat_bnds = np.arange(-90, 91, 10)
    output_lat_bnds = np.linspace(-90, 90, 31)
    weights = regridding_weights(input_lat_bnds, output_lat_bnds)
    assert weights @ np.ones(len(input_lat_bnds) - 1) == pytest.approx(1)


def test_unequal_to_lower():
    # input  | | | | | | | | | |
    # output |  |  |  |  |  |  |

    input_lat_bnds = np.linspace(-90, 90, 31)
    output_lat_bnds = np.linspace(-90, 90, 10)
    weights = regridding_weights(input_lat_bnds, output_lat_bnds)
    assert weights @ np.ones(len(input_lat_bnds) - 1) == pytest.approx(1)


def test_unequal_output_full_overlap():
    # input  |  |  |  |  |  |  |
    # output |    |  X |    |  |

    input_lat_bnds = np.linspace(-90, 90, 20)
    output_lat_bnds = np.linspace(-90, 90, 30)
    weights = regridding_weights(input_lat_bnds, output_lat_bnds)
    assert weights @ np.ones(len(input_lat_bnds) - 1) == pytest.approx(1)


def test_regrid(input_ds, output_ds):

    regrid = Regridder1D(input_ds, output_ds)
    ds = regrid(input_ds)
    assert ds.temperature.shape == (len(input_ds.altitude), len(output_ds.lat))
    assert ds.temperature.values == pytest.approx(1)


def test_noncontiguous_input():
    input_lat_bnds = np.array([[0, 20], [20, 40], [50, 70]])
    output_lat_bnds = np.linspace(10, 50, 10)
    with pytest.raises(ValueError):
        weights = regridding_weights(input_lat_bnds, output_lat_bnds)


def test_noncontiguous_output():
    input_lat_bnds = np.arange(-90, 91, 10)
    output_lat_bnds = np.array([[0, 20], [20, 40], [50, 70]])
    weights = regridding_weights(input_lat_bnds, output_lat_bnds)
    assert weights @ np.ones(len(input_lat_bnds) - 1) == pytest.approx(1)
