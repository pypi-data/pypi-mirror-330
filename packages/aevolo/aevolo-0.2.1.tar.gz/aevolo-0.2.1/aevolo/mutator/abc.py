from abc import ABC, abstractmethod
from typing import List

from aevolo.individual.abc import IndividualABC


class MutatorABC[C, F](ABC):
    @abstractmethod
    def mutate(self, population: List[IndividualABC[C, F]]) -> List[IndividualABC[C, F]]:
        pass

    @abstractmethod
    def get_rate(self) -> float:
        pass