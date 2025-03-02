import logging
import textwrap
from copy import deepcopy
from logging import Logger
from typing import Type, Union, Optional

from aevolo.crossover.abc import CrossoverABC
from aevolo.evolver.abc import EvolverABC, EvolutionInfoABC
from aevolo.individual.abc import IndividualABC
from aevolo.mutator.abc import MutatorABC
from aevolo.generation.abc import GenerationABC
from aevolo.selector.abc import SelectorABC


class GAEvolutionInfoABC[EI](EvolutionInfoABC):
    def __init__(self):
        self.initial_info = {}
        self.generations_info = []
        self.final_info = {}

    def record_initial_info(self, **kwargs):
        self.initial_info = {**kwargs}

    def record_generation_info(self, **kwargs):
        self.generations_info.append({**kwargs})

    def record_final_info(self, **kwargs):
        self.final_info = {**kwargs}

    def get_info(self) -> EI:
        return deepcopy({
            'initial_info': self.initial_info,
            'generations_info': self.generations_info,
            'final_info': self.final_info
        })


class GAEvolver[C, F, EI](EvolverABC):
    """
    A typical Genetic Algorithm Evolver
    """

    def __init__(self,
                 initial_generation: Optional[GenerationABC[C, F]] = None,
                 population_n: int = 0,
                 generations_n: int = 0,
                 selector: Optional[SelectorABC[C, F]] = None,
                 mutator: Optional[MutatorABC[C, F]] = None,
                 crossover: Optional[CrossoverABC[C, F]] = None,
                 logger: Optional[Logger] = None
                 ):
        self.initial_generation = initial_generation
        # defaults
        self.population_n: int = population_n
        self.generations_n: int = generations_n
        self.selector: Optional[SelectorABC[C, F]] = selector
        self.mutator: Optional[MutatorABC[C, F]] = mutator
        self.crossover: Optional[CrossoverABC[C, F]] = crossover
        # evolve record
        self.best_individual: Optional[IndividualABC[C, F]] = None
        self.best_fitness: Optional[F] = None
        self.evolve_info = GAEvolutionInfoABC()
        self.logger = logger

    def check_params(self):
        assert self.initial_generation is not None
        assert self.population_n > 0
        assert self.generations_n > 0
        assert self.selector is not None
        assert self.mutator is not None
        assert self.crossover is not None

    def evolve(self) -> GAEvolutionInfoABC[EI]:
        """
        Start evolve
        :return:
        """
        # check params
        self.check_params()
        # record initial info
        self.evolve_info.record_initial_info(
            population_n=self.population_n,
            generations_n=self.generations_n,
            selector=str(self.selector),
            mutator=str(self.mutator),
            crossover=str(self.crossover),
            crossover_rate=self.crossover.get_rate(),
            mutation_rate=self.mutator.get_rate(),
        )
        self.get_logger().log(logging.INFO, textwrap.dedent(f"""
        Evolving with the following parameters:   
        Population N: {self.population_n}
        Generation N: {self.generations_n}
        Crossover Rate: {self.crossover.get_rate()}
        Mutation Rate: {self.mutator.get_rate()}
        """.strip()))
        # initialize first generation
        generation = self.initial_generation.lazy_init(self.population_n)
        # track the best individual
        self.best_individual = generation.get_best_individual()
        self.best_fitness = self.best_individual.get_fitness()
        # record initial generation info
        self.evolve_info.record_generation_info(
            generation_iteration=-1,
            best_individual=self.best_individual.get_chromosome(),
            best_fitness=self.best_fitness,
            chromosomes=generation.get_population_chromosomes(),
            fitness=generation.get_population_fitness()
        )
        self.get_logger().log(logging.INFO, textwrap.dedent(f"""
        Initial best individual: {self.best_individual}
        Initial best fitness: {self.best_fitness}
        """.strip()))
        # evolve
        for iteration_i in range(self.generations_n):
            # select
            population = generation.get_population()
            selected_population = self.selector.select(population=population)
            # crossover
            crossed_population = self.crossover.cross(population=selected_population)
            # mutate
            mutated_population = self.mutator.mutate(population=crossed_population)
            # make it as the new generation
            generation = deepcopy(generation)
            generation.set_population(mutated_population)
            # track the best individual
            best_individual = generation.get_best_individual()
            best_fitness = best_individual.get_fitness()
            if best_fitness > self.best_fitness:
                self.best_individual = best_individual
                self.best_fitness = best_fitness

            # record generation info
            self.evolve_info.record_generation_info(
                generation_iteration=iteration_i,
                best_individual=best_individual.get_chromosome(),
                best_fitness=self.best_fitness,
                chromosomes=generation.get_population_chromosomes(),
                fitness=generation.get_population_fitness()
            )
            self.get_logger().log(logging.INFO, textwrap.dedent(f"""
            Generation {iteration_i}:
            Best individual: {str(self.best_individual)}
            Best fitness: {self.best_fitness}
            """.strip()))

        # record final info
        self.evolve_info.record_final_info(
            best_individual=self.best_individual.get_chromosome(),
            best_fitness=self.best_fitness
        )
        self.get_logger().log(logging.INFO, textwrap.dedent(f"""
        Final best individual: {str(self.best_individual)}
        Final best fitness: {self.best_fitness}
        """.strip()))
        return self.evolve_info

    def get_logger(self) -> Logger:
        if self.logger is not None:
            return self.logger
        handler = logging.StreamHandler()
        logger = logging.getLogger(f"{__name__}_default")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger


class GABuilder:
    """
    A builder for GAEvolver
    """

    def __init__(self):
        self.initial_generation = None
        self.population_n = 0
        self.generations_n = 0
        self.selector = None
        self.mutator = None
        self.crossover = None
        self.logger = None

    def set_initial_generation(self, initial_generation: GenerationABC) -> 'GABuilder':
        self.initial_generation = initial_generation
        return self

    def set_population_n(self, population_n: int) -> 'GABuilder':
        self.population_n = population_n
        return self

    def set_generations_n(self, generations_n: int) -> 'GABuilder':
        self.generations_n = generations_n
        return self

    def set_selector(self, selector: SelectorABC) -> 'GABuilder':
        self.selector = selector
        return self

    def set_mutator(self, mutator: MutatorABC) -> 'GABuilder':
        self.mutator = mutator
        return self

    def set_crossover(self, crossover: CrossoverABC) -> 'GABuilder':
        self.crossover = crossover
        return self

    def set_logger(self, logger: Logger) -> 'GABuilder':
        self.logger = logger
        return self

    def build(self) -> GAEvolver:
        return GAEvolver(
            initial_generation=self.initial_generation,
            population_n=self.population_n,
            generations_n=self.generations_n,
            selector=self.selector,
            mutator=self.mutator,
            crossover=self.crossover,
            logger=self.logger
        )
