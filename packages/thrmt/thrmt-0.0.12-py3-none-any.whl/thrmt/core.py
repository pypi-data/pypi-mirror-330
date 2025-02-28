#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────────────
from typing import List

import torch
from torch import Tensor

# ──────────────────────────────────────────────────────────────────────────────
__all__: List[str] = ["batched_outer"]
# ──────────────────────────────────────────────────────────────────────────────


def batched_outer(vec1: Tensor, vec2: Tensor, use_einsum: bool = False) -> Tensor:
    if use_einsum:
        return torch.einsum("bi,bj->bij", (vec1, vec2))
    else:
        return torch.bmm(vec1.unsqueeze(2), vec2.unsqueeze(1))
