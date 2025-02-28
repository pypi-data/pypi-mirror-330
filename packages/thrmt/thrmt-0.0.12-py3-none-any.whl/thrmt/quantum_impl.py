#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~~ Imports ~~ ────────────────────────────────────────────────────────────────
from collections.abc import Callable
from typing import List
from typing import Optional
from typing import Tuple

import torch as th
from torch import Tensor

from .core import batched_outer
from .impl import random_cue as _random_cue
from .impl import random_gce as _random_gce
from .impl import random_gue as _random_gue

# ~~ Exports ~~ ────────────────────────────────────────────────────────────────
__all__: List[str] = [
    "random_rho_hs",
    "random_rho_bh",
    "random_obs_gue",
    "random_obs_csu",
    "random_rho_pure",
]


# ~~ Functions ~~ ──────────────────────────────────────────────────────────────


def random_rho_hs(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
):
    x: Tensor = _random_gce(
        size=size, dtype=dtype, device=device, batch_shape=batch_shape
    )
    aad: Tensor = x @ x.transpose(-2, -1).conj()
    return aad / aad.diagonal(offset=0, dim1=-2, dim2=-1).sum(-1)


def random_rho_bh(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
    random_phases: bool = False,
):
    u: Tensor = _random_cue(
        size=size,
        dtype=dtype,
        device=device,
        batch_shape=batch_shape,
        random_phases=random_phases,
    )
    a: Tensor = _random_gce(
        size=size, dtype=dtype, device=device, batch_shape=batch_shape
    )
    beye: Tensor = th.diag_embed(
        th.ones(*batch_shape, size, dtype=dtype, device=device)
    )
    x: Tensor = (beye + u) @ a
    aad: Tensor = x @ x.transpose(-2, -1).conj()
    return aad / aad.diagonal(offset=0, dim1=-2, dim2=-1).sum(-1)


def random_obs_gue(
    size: int,
    sigma: float,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    return _random_gue(
        size=size, sigma=sigma, dtype=dtype, device=device, batch_shape=batch_shape
    )


def random_obs_csu(
    size: int,
    evdist: Callable[..., Tensor],
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
    random_phases: bool = False,
) -> Tensor:
    u: Tensor = _random_cue(
        size=size,
        dtype=dtype,
        device=device,
        batch_shape=batch_shape,
        random_phases=random_phases,
    )
    ev: Tensor = evdist(*batch_shape, size, dtype=dtype, device=device)
    return u @ th.diag_embed(ev) @ u.transpose(-2, -1).conj()


def random_rho_pure(
    size: int,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
    *,
    bo_einsum: bool = False,
) -> Tensor:
    p: Tensor = th.randn(*batch_shape, size, dtype=dtype, device=device)
    p: Tensor = p / th.linalg.norm(p, dim=-1, keepdim=True)
    p: Tensor = p.unsqueeze(0) if batch_shape == () else p
    return batched_outer(p, p.conj(), use_einsum=bo_einsum)
