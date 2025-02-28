#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ~~ Imports ~~ ────────────────────────────────────────────────────────────────
from typing import List

import torch as th

# ~~ Exports ~~ ────────────────────────────────────────────────────────────────
__all__: List[str] = [
    "complex_dtypes",
    "real_dtypes",
    "c2r_map",
    "r2c_map",
]

# ~~ dtypes ~~ ─────────────────────────────────────────────────────────────────

complex_dtypes: List[th.dtype] = [
    th.cdouble,
    th.cfloat,
    th.chalf,
    th.complex128,
    th.complex32,
    th.complex64,
]

real_dtypes: List[th.dtype] = [
    th.bfloat16,
    th.double,
    th.float,
    th.float16,
    th.float32,
    th.float64,
    th.float8_e4m3fn,
    th.float8_e4m3fnuz,
    th.float8_e5m2,
    th.float8_e5m2fnuz,
    th.half,
]

# ~~ dtype-maps ~~ ─────────────────────────────────────────────────────────────
c2r_map: dict[th.dtype, th.dtype] = {
    th.cdouble: th.double,
    th.cfloat: th.float,
    th.chalf: th.half,
    th.complex128: th.float64,
    th.complex32: th.float16,
    th.complex64: th.float32,
}

r2c_map: dict[th.dtype, th.dtype] = {
    th.bfloat16: th.complex32,
    th.double: th.cdouble,
    th.float16: th.complex32,
    th.float32: th.complex64,
    th.float64: th.complex128,
    th.float8_e4m3fn: th.complex32,
    th.float8_e4m3fnuz: th.complex32,
    th.float8_e5m2: th.complex32,
    th.float8_e5m2fnuz: th.complex32,
    th.float: th.cfloat,
    th.half: th.chalf,
}
