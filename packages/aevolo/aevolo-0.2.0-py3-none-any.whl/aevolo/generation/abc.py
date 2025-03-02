from abc import ABC, abstractmethod
from typing import List

from aevolo.individual.abc import IndividualABC


class GenerationABC[C, F](ABC):
    @abstractmethod
    def lazy_init(self, n: int) -> 'GenerationABC[C, F]':
        pass

    @abstractmethod
    def get_best_individual(self) -> IndividualABC[C, F]:
        pass

    @abstractmethod
    def get_best_individual_fitness(self) -> F:
        pass

    @abstractmethod
    def get_population(self) -> List[IndividualABC[C, F]]:
        pass

    @abstractmethod
    def set_population(self, population: List[IndividualABC[C, F]]):
        pass

    def get_population_chromosomes(self) -> List[C]:
        return [individual.get_chromosome() for individual in self.get_population()]

    def get_population_fitness(self) -> List[F]:
        return [individual.get_fitness() for individual in self.get_population()]

    def get_population_size(self) -> int:
        return len(self.get_population())
