from abc import ABC, abstractmethod


class EvolutionInfoABC[EI](ABC):
    @abstractmethod
    def get_info(self) -> EI:
        pass


class EvolverABC[C, F, EI](ABC):
    @abstractmethod
    def evolve(self,*args,**kwargs) -> EvolutionInfoABC[EI]:
        pass
