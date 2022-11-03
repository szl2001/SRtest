from abc import ABC, abstractmethod
from typing import Tuple, List


class FloatConverter(ABC):

    @abstractmethod
    def encode(self, val: float) -> Tuple:
        pass

    @abstractmethod
    def decode(self, lst: Tuple) -> float:
        pass

    @property
    @abstractmethod
    def tokens(self) -> List[str]:
        pass
