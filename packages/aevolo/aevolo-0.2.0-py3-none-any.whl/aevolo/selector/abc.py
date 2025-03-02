from abc import ABC, abstractmethod
from typing import List

from aevolo.individual.abc import IndividualABC
from aevolo.generation.abc import GenerationABC


class SelectorABC[C, F](ABC):
    @abstractmethod
    def select(self, population: List[IndividualABC[C, F]]) -> List[IndividualABC[C, F]]:
        pass
