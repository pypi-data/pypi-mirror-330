import numpy as np
import xarray as xr


def calculate_bounds_from_array(data: xr.DataArray, ndim: int = 2, bnds_dim="bnds") -> xr.DataArray:
    """
    Estimate the bounds of a 1D array
    """

    array = data.to_numpy()
    diff = np.diff(array)
    edges = np.concatenate(
        [[array[0] - diff[0] / 2], array[0:-1] + diff / 2, [array[-1] + diff[-1] / 2]]
    )
    if ndim == 2:
        edges = np.array([[float(a), float(b)] for a, b in zip(edges[0:-1], edges[1:])])
        return xr.DataArray(edges, dims=[data.name, bnds_dim], coords=[array, [0, 1]])
    else:
        return xr.DataArray(
            edges, dims=[f"{data.name}_{bnds_dim}"], coords=[np.arange(0, len(edges))]
        )
