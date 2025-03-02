from abc import ABC, abstractmethod


class IndividualABC[C, F](ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def get_chromosome(self) -> C:
        pass

    @abstractmethod
    def get_fitness(self) -> F:
        pass
