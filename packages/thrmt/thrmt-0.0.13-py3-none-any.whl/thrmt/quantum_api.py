#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ~~ Imports ~~ ────────────────────────────────────────────────────────────────
from collections.abc import Callable
from typing import List
from typing import Optional
from typing import Tuple

import torch as th
from torch import Tensor

from .auxiliary import check_bounds
from .auxiliary import check_dtype
from .auxiliary import check_size
from .gellmann_impl import random_obs_cgi as _random_obs_cgi
from .quantum_impl import random_obs_csu as _random_obs_csu
from .quantum_impl import random_obs_gue as _random_obs_gue
from .quantum_impl import random_rho_bh as _random_rho_bh
from .quantum_impl import random_rho_hs as _random_rho_hs
from .quantum_impl import random_rho_pure as _random_rho_pure
from .types import complex_dtypes

# ~~ Exports ~~ ────────────────────────────────────────────────────────────────
__all__: List[str] = [
    "random_rho_bh",
    "random_rho_hs",
    "random_obs_csu",
    "random_obs_gue",
    "random_obs_cgi",
    "random_rho_pure",
]


# ~~ Functions ~~ ──────────────────────────────────────────────────────────────
# noinspection DuplicatedCode
def random_rho_hs(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Optional[Tuple[int, ...]] = None,
) -> Tensor:
    """
    Generate a random quantum state (or a batch thereof) uniformly w.r.t. the Hilbert-Schmidt measure.

    Parameters
    ----------
    size : int
        The size of the square matrix.
    dtype : torch.dtype
        The data type. Default is torch.double.
    device : torch.device, optional
        The device. Default is None.
    batch_shape : tuple of ints, optional
        The batch shape for generating multiple matrices. Default is None.

    Returns
    -------
    Tensor
        A random quantum state (or a batch thereof) uniformly w.r.t. the Hilbert-Schmidt measure.
    """
    check_size(size)
    check_dtype(dtype, complex_dtypes)
    bs = () if batch_shape is None else batch_shape
    return _random_rho_hs(size=size, dtype=dtype, device=device, batch_shape=bs)


def random_rho_bh(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Optional[Tuple[int, ...]] = None,
    random_phases: bool = False,
) -> Tensor:
    """
    Generate a random quantum state (or a batch thereof) uniformly w.r.t. the Bures-Helstrom measure.

    Parameters
    ----------
    size : int
        The size of the square matrix.
    dtype : torch.dtype
        The data type. Default is torch.double.
    device : torch.device, optional
        The device. Default is None.
    batch_shape : tuple of ints, optional
        The batch shape for generating multiple matrices. Default is None.
    random_phases : bool, optional
        Use uniform random phases for piecewise correction within QR decomposition. Default is False.

    Returns
    -------
    Tensor
        A random quantum state (or a batch thereof) uniformly w.r.t. the Bures-Helstrom measure.
    """
    check_size(size)
    check_dtype(dtype, complex_dtypes)
    bs = () if batch_shape is None else batch_shape
    return _random_rho_bh(
        size=size,
        dtype=dtype,
        device=device,
        batch_shape=bs,
        random_phases=random_phases,
    )


def random_obs_csu(
    size: int,
    evdist: Callable[..., Tensor],
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Optional[Tuple[int, ...]] = None,
    random_phases: bool = False,
) -> Tensor:
    """
    Generate a random observable (or a batch thereof) uniformly in a compact set from the distribution of eigenvalues.

    Parameters
    ----------
    size : int
        The size of the square matrix.
    evdist : Callable[..., Tensor]
        A function to sample from distribution of eigenvalues. Must implement the Torch API.
    dtype : torch.dtype
        The data type. Default is torch.double.
    device : torch.device, optional
        The device. Default is None.
    batch_shape : tuple of ints, optional
        The batch shape for generating multiple matrices. Default is None.
    random_phases : bool, optional
        Use uniform random phases for piecewise correction within QR decomposition. Default is False.

    Returns
    -------
    Tensor
        A random observable (or a batch thereof) uniformly w.r.t. the CSU measure.
    """
    check_size(size)
    check_dtype(dtype, complex_dtypes)
    bs = () if batch_shape is None else batch_shape
    return _random_obs_csu(
        size=size,
        evdist=evdist,
        dtype=dtype,
        device=device,
        batch_shape=bs,
        random_phases=random_phases,
    )


def random_obs_gue(
    size: int,
    sigma: float,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Optional[Tuple[int, ...]] = None,
) -> Tensor:
    """
    Generate a random observable (or a batch thereof) uniformly in the Gaussian Unitary Ensemble.

    Parameters
    ----------
    size : int
        The size of the square matrix.
    sigma : float
        The scale parameter.
    dtype : torch.dtype
        The data type. Default is torch.double.
    device : torch.device, optional
        The device. Default is None.
    batch_shape : tuple of ints, optional
        The batch shape for generating multiple matrices. Default is None.

    Returns
    -------
    Tensor
        A random observable (or a batch thereof) uniformly w.r.t. the GUE measure.
    """
    check_size(size)
    check_dtype(dtype, complex_dtypes)
    bs = () if batch_shape is None else batch_shape
    return _random_obs_gue(
        size=size, sigma=sigma, dtype=dtype, device=device, batch_shape=bs
    )


def random_obs_cgi(
    size: int,
    coeff_low: float = 0.0,
    coeff_upp: float = 1.0,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Optional[Tuple[int, ...]] = None,
) -> Tensor:
    """
    Generate a random observable (or a batch thereof) uniformly in the Gell-Mann parameterization of Hermitians.

    Parameters
    ----------
    size : int
        The size of the square matrix.
    coeff_low : float, optional
        The lower bound for the coefficients. Default is 0.0.
    coeff_upp : float, optional
        The upper bound for the coefficients. Default is 1.0.
    dtype : torch.dtype
        The data type. Default is torch.double.
    device : torch.device, optional
        The device. Default is None.
    batch_shape : tuple of ints, optional
        The batch shape for generating multiple matrices. Default is None.

    Returns
    -------
    Tensor
        A random observable (or a batch thereof) uniformly w.r.t. the CGI measure.
    """
    check_size(size, disallow_equality=True)
    check_bounds(coeff_low, coeff_upp)
    check_dtype(dtype, complex_dtypes)
    bs = () if batch_shape is None else batch_shape
    return _random_obs_cgi(
        size=size,
        coeff_low=coeff_low,
        coeff_upp=coeff_upp,
        dtype=dtype,
        device=device,
        batch_shape=bs,
    )


def random_rho_pure(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Optional[Tuple[int, ...]] = None,
    *,
    bo_einsum: bool = False,
) -> Tensor:
    """
    Generate a random pure quantum state (or a batch thereof).

    Parameters
    ----------
    size : int
        The size of the square matrix.
    dtype : torch.dtype
        The data type. Default is torch.double.
    device : torch.device, optional
        The device. Default is None.
    batch_shape : tuple of ints, optional
        The batch shape for generating multiple matrices. Default is None.
    bo_einsum : bool, optional
        If True, use einsum for batched outer product. Default is False.

    Returns
    -------
    Tensor
        A random pure quantum state (or a batch thereof).
    """
    check_size(size)
    check_dtype(dtype, complex_dtypes)
    bs = () if batch_shape is None else batch_shape
    return _random_rho_pure(
        size=size,
        dtype=dtype,
        device=device,
        batch_shape=bs,
        bo_einsum=bo_einsum,
    )
