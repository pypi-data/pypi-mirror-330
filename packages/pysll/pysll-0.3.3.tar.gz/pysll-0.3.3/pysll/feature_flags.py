from __future__ import annotations

import os
from dataclasses import dataclass

from pysll.utils import truthy


@dataclass
class FeatureFlags:
    use_numpy: bool

    @staticmethod
    def from_environment() -> FeatureFlags:
        return FeatureFlags(
            use_numpy=truthy(os.environ.get("PYSLL_USE_NUMPY")),
        )
