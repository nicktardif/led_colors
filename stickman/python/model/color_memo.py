from typing import Optional

from model.rgb import RGB


class ColorMemo:
    def __init__(self):
        self._memo = {}

    def set_value(self, algorithm_key: str, percent: str, value: RGB):
        if not algorithm_key in self._memo:
            self._memo[algorithm_key] = {}

        self._memo[algorithm_key][percent] = value

    def get(self, algorithm_key: str, percent: str) -> Optional[RGB]:
        return self._memo.get(algorithm_key, {}).get(percent, None)
