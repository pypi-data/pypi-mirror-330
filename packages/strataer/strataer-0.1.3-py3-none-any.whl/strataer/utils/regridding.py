import numpy as np
import xarray as xr
from typing import Callable
import logging


def latitude_weight(lat1: np.ndarray, lat2: np.ndarray):
    """normalized area between two latitude bands"""
    return np.abs(np.sin(np.deg2rad(lat2)) - np.sin(np.deg2rad(lat1)))


def linear_weight(lat1: np.ndarray, lat2: np.ndarray):
    """absolute difference between lat2 and lat1"""
    return np.abs(lat2 - lat1)


def flatten_bounds(bounds):
    if len(bounds.shape) == 1:
        left = bounds[0:-1]
        right = bounds[1:]
    else:
        left = bounds[:, 0]
        right = bounds[:, 1]

    if not np.all(left < right):
        right, left = left, right

    return left, right


def regridding_weights(
    input_bnds: np.ndarray,
    output_bnds: np.ndarray,
    weight_function: Callable[
        [float | np.ndarray, float | np.ndarray], float | np.ndarray
    ] = linear_weight,
) -> np.ndarray:
    """compute the weighting matrix used to map between input and output grids.

    Parameters
    ----------
    input_bnds : np.ndarray
        1d array of input bounds
    output_bnds : np.ndarray
        1d array of output bounds
    weight_function : Callable[[float, float], float], optional
        function used to compute the width of a band given the edges.
        By default `linear_weight` where width = np.abs(bnds[1] - bnds[0])

    Returns
    -------
    np.ndarray
        array of size (len(output_bnds) - 1, len(input_bnds) - 1)
    """

    in_left, in_right = flatten_bounds(input_bnds)

    if len(np.unique(np.concat([in_left, in_right]))) != len(in_left) + 1:
        raise ValueError("Input data must have contiguous bounds")

    out_starts, out_ends = flatten_bounds(output_bnds)

    weights = np.zeros((len(out_starts), len(in_left)), dtype=float)

    for cell_idx, (out_left, out_right) in enumerate(zip(out_starts, out_ends)):

        cell_area = weight_function(out_right, out_left)

        # higher res input - output cell completely overlaps at least 1 input cell
        inside = (in_left >= out_left) & (in_right <= out_right)
        inside_area = weight_function(in_right[inside], in_left[inside])
        weights[cell_idx, inside] = inside_area / cell_area

        # higher res output - input cell completely overlaps output cell
        full_overlap = (in_left <= out_left) & (in_right >= out_right)
        if np.any(full_overlap):
            weights[cell_idx, full_overlap] = 1.0
        else:

            # partial overlap of input cell left/right sides of output cell
            left_overlap = (in_left < out_left) & (in_right > out_left)
            left_overlap_area = weight_function(in_right[left_overlap], out_left)

            right_overlap = (in_left < out_right) & (in_right > out_right)
            right_overlap_area = weight_function(out_right, in_left[right_overlap])

            weights[cell_idx, left_overlap] = left_overlap_area / cell_area
            weights[cell_idx, right_overlap] = right_overlap_area / cell_area

        if weights[cell_idx].sum() != 1.0:
            if np.abs(weights[cell_idx].sum() - 1.0) > 0.01:
                logging.warning(
                    f"weights from cell {cell_idx} sum to {weights[cell_idx].sum()}, requiring large renormalization"
                )
            weights[cell_idx] /= weights[cell_idx].sum()

    return weights


class Regridder1D:
    """
    Conservatively regrid a 1D dataset in latitude. Duplicates the interface to xesmf.Regridder so either can be used
    """

    def __init__(self, input, output, method="conservative_normed", periodic=False):

        self.input_lat = input.lat
        self.input_lat_bnds = input.lat_bnds

        self.output_lat = output.lat
        self.output_lat_bnds = output.lat_bnds

        if (self.input_lat_bnds[0] > self.output_lat_bnds[0]) | (
            self.input_lat_bnds[-1] < self.output_lat_bnds[-1]
        ):
            raise ValueError("input grid must span output grid")

        weights = regridding_weights(
            self.input_lat_bnds.values, self.output_lat_bnds.values, weight_function=latitude_weight
        )
        self.weights = xr.DataArray(
            weights,
            dims=["new_lat", "lat"],
            coords=[self.output_lat, self.input_lat],
            name="weights",
        )

    def __call__(self, ds: xr.Dataset | xr.DataArray):

        if isinstance(ds, xr.Dataset):
            new_ds = []
            for var in ds:
                new_ds.append((ds[var] @ self.weights).rename(var))
            return xr.merge(new_ds).rename({"new_lat": "lat"})

        new_ds = ds @ self.weights
        return new_ds.rename({"new_lat": "lat"})
