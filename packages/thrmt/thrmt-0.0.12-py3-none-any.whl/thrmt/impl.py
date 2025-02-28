#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ~~ Imports ~~ ────────────────────────────────────────────────────────────────
from math import sqrt as msqrt
from typing import List
from typing import Optional
from typing import Tuple

import torch as th
from torch import Tensor

from .types import c2r_map

# ~~ Exports ~~ ────────────────────────────────────────────────────────────────

__all__: List[str] = [
    "random_coe",  # Circular Orthogonal Ensemble
    "random_cue",  # Circular Unitary (Haar Uniform) Ensemble
    "random_gce",  # Ginibre Complex Ensemble
    "random_goe",  # Gaussian (Hermite, or Wigner) Orthogonal Ensemble
    "random_gre",  # Ginibre Real Ensemble
    "random_gue",  # Gaussian (Hermite, or Wigner) Unitary Ensemble
    "random_jce",  # Jacobi (MANOVA) Complex Ensemble
    "random_jre",  # Jacobi (MANOVA) Real Ensemble
    "random_wce",  # Wishart (Laguerre) Complex Ensemble
    "random_wre",  # Wishart (Laguerre) Real Ensemble
]

# ~~ Functions ~~ ──────────────────────────────────────────────────────────────


def random_gre(
    size: int,
    nnorm: bool = False,
    dtype: th.dtype = th.double,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
):
    x: Tensor = th.randn(*batch_shape, size, size, dtype=dtype, device=device)
    if nnorm:
        x: Tensor = x / msqrt(size)
    return x


def random_gce(
    size: int,
    nnorm: bool = False,
    cnorm: bool = True,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
):
    x: Tensor = th.randn(*batch_shape, size, size, dtype=dtype, device=device)
    if nnorm and (not cnorm):
        x: Tensor = x / msqrt(size / 2)
    else:
        if nnorm:
            x: Tensor = x / msqrt(size)
        if not cnorm:
            x: Tensor = x * msqrt(2)
    return x


def random_cue(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
    random_phases: bool = False,
) -> Tensor:
    a: Tensor = random_gce(
        size=size, dtype=dtype, device=device, batch_shape=batch_shape
    )
    q, r = th.linalg.qr(a)
    if random_phases:
        d: Tensor = th.exp(
            1j
            * 2
            * th.pi
            * th.rand(*batch_shape, size, dtype=c2r_map[dtype], device=device)
        )
    else:
        d: Tensor = r.diagonal(dim1=-2, dim2=-1)
        d: Tensor = d / th.abs(d)
    return q @ th.diag_embed(d)


def random_coe(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
    random_phases: bool = False,
) -> Tensor:
    x: Tensor = random_cue(
        size=size,
        dtype=dtype,
        device=device,
        batch_shape=batch_shape,
        random_phases=random_phases,
    )
    return x.transpose(-2, -1) @ x


def random_gue(
    size: int,
    sigma: float,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    x: Tensor = (
        random_gce(size=size, dtype=dtype, device=device, batch_shape=batch_shape)
        * sigma
    )
    return (x + x.transpose(-2, -1).conj()) / msqrt(2)


def random_goe(
    size: int,
    sigma: float,
    dtype: th.dtype = th.double,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    x: Tensor = (
        random_gre(size=size, dtype=dtype, device=device, batch_shape=batch_shape)
        * sigma
    )
    return (x + x.transpose(-2, -1)) / msqrt(2)


def random_wre(
    size_n: int,
    sigma: float,
    size_m: Optional[int] = None,
    dtype: th.dtype = th.double,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    actual_size_m: int = size_m or size_n
    x: Tensor = (
        th.randn(*batch_shape, size_n, actual_size_m, dtype=dtype, device=device)
        * sigma
    )
    return x @ x.transpose(-2, -1)


def random_wce(
    size_n: int,
    sigma: float,
    size_m: Optional[int] = None,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    actual_size_m: int = size_m or size_n
    x: Tensor = (
        th.randn(*batch_shape, size_n, actual_size_m, dtype=dtype, device=device)
        * sigma
    )
    return x @ x.transpose(-2, -1).conj()


def random_jre(
    size_n: int,
    size_m1: Optional[int] = None,
    size_m2: Optional[int] = None,
    dtype: th.dtype = th.double,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    actual_size_m1: int = size_m1 or size_n
    actual_size_m2: int = size_m2 or size_n
    x: Tensor = th.randn(
        *batch_shape, size_n, actual_size_m1, dtype=dtype, device=device
    )
    a1: Tensor = x @ x.transpose(-2, -1)
    y: Tensor = th.randn(
        *batch_shape, size_n, actual_size_m2, dtype=dtype, device=device
    )
    a2: Tensor = a1 + y @ y.transpose(-2, -1)
    return a1 @ th.linalg.inv(a2)


def random_jce(
    size_n: int,
    size_m1: Optional[int] = None,
    size_m2: Optional[int] = None,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    actual_size_m1: int = size_m1 or size_n
    actual_size_m2: int = size_m2 or size_n
    x: Tensor = th.randn(
        *batch_shape, size_n, actual_size_m1, dtype=dtype, device=device
    )
    a1: Tensor = x @ x.transpose(-2, -1).conj()
    y: Tensor = th.randn(
        *batch_shape, size_n, actual_size_m2, dtype=dtype, device=device
    )
    a2: Tensor = a1 + y @ y.transpose(-2, -1).conj()
    return a1 @ th.linalg.inv(a2)
