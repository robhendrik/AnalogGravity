"""Wave-state container and leapfrog initialization."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(slots=True)
class WaveState:
    """State used by the centered-in-time finite-difference solver."""

    y_curr: NDArray[np.float64]
    y_prev: NDArray[np.float64]
    t: float = 0.0

    def __post_init__(self) -> None:
        self.y_curr = np.asarray(self.y_curr, dtype=float)
        self.y_prev = np.asarray(self.y_prev, dtype=float)
        if self.y_curr.ndim != 1 or self.y_prev.ndim != 1:
            raise ValueError("state arrays must be one-dimensional")
        if self.y_curr.shape != self.y_prev.shape:
            raise ValueError("y_curr and y_prev must have identical shapes")
        if not np.all(np.isfinite(self.y_curr)) or not np.all(np.isfinite(self.y_prev)):
            raise ValueError("state arrays must contain only finite values")
