#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ~~ Imports ~~ ────────────────────────────────────────────────────────────────
import itertools
import math
from typing import List
from typing import Optional
from typing import Tuple

import torch as th
from torch import Tensor

from .types import c2r_map

# ~~ Exports ~~ ────────────────────────────────────────────────────────────────
__all__: List[str] = [
    "random_obs_cgi",  # Observable as linear combination of Generalized Gell-Mann matrices
]


# ~~ Functions ~~ ──────────────────────────────────────────────────────────────


def _gen_gmm(
    size: int,
    dtype=th.cdouble,
    device: Optional[th.device] = None,
) -> List[Tensor]:
    matrices: List[Tensor] = []

    for i, j in itertools.combinations(range(size), 2):
        symmetric: Tensor = th.zeros((size, size), dtype=dtype, device=device)
        symmetric[i, j] = 1.0 / math.sqrt(2.0)
        symmetric[j, i] = 1.0 / math.sqrt(2.0)
        matrices.append(symmetric)

        antisymmetric: Tensor = th.zeros((size, size), dtype=dtype, device=device)
        antisymmetric[i, j] = -1j / math.sqrt(2.0)  # type: ignore
        antisymmetric[j, i] = 1j / math.sqrt(2.0)  # type: ignore
        matrices.append(antisymmetric)

    for k in range(1, size):
        diag_matrix: Tensor = th.zeros((size, size), dtype=dtype, device=device)
        coeff: float = 1.0 / math.sqrt(k * (k + 1.0))
        for i in range(k):
            diag_matrix[i, i] = coeff
        diag_matrix[k, k] = -k * coeff
        matrices.append(diag_matrix)

    return matrices


def random_obs_cgi(
    size: int,
    coeff_low: float,
    coeff_upp: float,
    dtype: th.dtype = th.cdouble,
    device: Optional[th.device] = None,
    batch_shape: Tuple[int, ...] = (),
) -> Tensor:
    gell_mann_matrices: List[Tensor] = _gen_gmm(size, dtype=dtype, device=device)

    batch_size: Tuple[int, ...] = batch_shape if batch_shape else (1,)
    random_coeffs: Tensor = (coeff_upp - coeff_low) * th.rand(
        *batch_size, size * size - 1, dtype=c2r_map[dtype], device=device
    ) + coeff_low

    result: Tensor = (
        sum(  # type: ignore
            random_coeffs[..., i, None, None] * m
            for i, m in enumerate(gell_mann_matrices)
        )
        + th.eye(size, dtype=dtype, device=device) / size
    )
    return result.squeeze(0) if batch_shape == () else result  # type: ignore
