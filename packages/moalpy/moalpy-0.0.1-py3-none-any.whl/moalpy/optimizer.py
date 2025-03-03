from abc import abstractmethod
from typing import Union, List, Tuple, Dict
from moalpy.utils.agent import Agent, Target
from moalpy.utils.problem import Problem
from moalpy.utils.logger import Logger
from moalpy.utils.history import History
from moalpy.utils.validator import Validator
from moalpy.multi_objectives.reference_direction import merge_population_by_ref_dirs, UniformReferenceDirectionFactory
from moalpy.multi_objectives.non_dominated_sorting import find_non_dominated
import numpy as np
import time


class MultiObjectiveOptimizer:
    EPSILON = 10E-10
    SUPPORTED_ARRAYS = [list, tuple, np.ndarray]

    def __init__(self, n_partitions=12, **kwargs):
        super(MultiObjectiveOptimizer, self).__init__()
        self.n_partitions = n_partitions
        self.ref_dirs = None
        self.epoch, self.pop_size = None, None
        self.mode, self.n_workers, self.name = None, None, None
        self.pop, self.g_best, self.g_worst = None, Agent(), None
        self.problem, self.logger, self.history = None, None, None
        self.generator = None
        if self.name is None: self.name = self.__class__.__name__
        self._set_keyword_arguments(kwargs)
        self.validator = Validator()
        self.pareto: List['Agent'] = []
        self.parameters, self.params_name_ordered = {}, None

    def _set_keyword_arguments(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_parameters(self, parameters: Union[List, Tuple, Dict]) -> None:
        """
        Set the parameters for current optimizer.

        if paras is a list of parameter's name, then it will set the default value in optimizer as current parameters
        if paras is a dict of parameter's name and value, then it will override the current parameters

        Args:
            parameters: The parameters
        """
        if type(parameters) in (list, tuple):
            self.params_name_ordered = tuple(parameters)
            self.parameters = {}
            for name in parameters:
                self.parameters[name] = self.__dict__[name]

        if type(parameters) is dict:
            valid_para_names = set(self.parameters.keys())
            new_para_names = set(parameters.keys())
            if new_para_names.issubset(valid_para_names):
                for key, value in parameters.items():
                    setattr(self, key, value)
                    self.parameters[key] = value
            else:
                raise ValueError(f"Invalid input parameters: {new_para_names} for {self.get_name()} optimizer. "
                                 f"Valid parameters are: {valid_para_names}.")

    def get_parameters(self) -> Dict:
        """
        Get parameters of optimizer.
        """
        return self.parameters

    def get_attributes(self) -> Dict:
        """
        Get all attributes in optimizer.
        """
        return self.__dict__

    def get_name(self) -> str:
        """
        Get name of the optimizer
        """
        return self.name

    def get_best_agents(self, size=1) -> List[Agent]:
        actual_size = size if len(self.pareto) >= size else len(self.pareto)
        selected_indices = np.random.choice(len(self.pareto), actual_size, False)
        return [a for i, a in enumerate(self.pareto) if i in selected_indices]

    @abstractmethod
    def evolve(self, epoch: int) -> None:
        pass

    def initialize_variables(self):
        pass

    def before_initialization(self, starting_solutions: Union[List, Tuple, np.ndarray] = None) -> None:
        """
        Args:
            starting_solutions: The starting solutions (not recommended)
        """
        if starting_solutions is None:
            pass
        elif type(starting_solutions) in self.SUPPORTED_ARRAYS and len(starting_solutions) == self.pop_size:
            if type(starting_solutions[0]) in self.SUPPORTED_ARRAYS and len(
                    starting_solutions[0]) == self.problem.n_dims:
                self.pop = [self.generate_agent(solution) for solution in starting_solutions]
            else:
                raise ValueError(
                    "Invalid starting_solutions. It should be a list of positions or 2D matrix of positions only.")
        else:
            raise ValueError(
                "Invalid starting_solutions. It should be a list/2D matrix of positions with same length as pop_size.")

    def initialization(self) -> None:
        if self.pop is None:
            self.pop = self.generate_population(self.pop_size)

    def after_initialization(self) -> None:
        self.update_pareto(self.pop)

    def before_main_loop(self):
        pass

    def check_problem(self, problem, seed) -> None:
        if isinstance(problem, Problem):
            problem.set_seed(seed)
            self.problem = problem
        elif isinstance(problem, dict):
            problem["seed"] = seed
            self.problem = Problem(**problem)
        else:
            raise ValueError("problem needs to be a dict or an instance of Problem class.")
        self.ref_dirs = UniformReferenceDirectionFactory(problem.n_dims, n_partitions=self.n_partitions).do()
        self.generator = np.random.default_rng(seed)
        self.logger = Logger.create(name=f"{self.__module__}.{self.__class__.__name__}")
        self.logger.info(self.problem.msg)
        self.history = History(self.name)
        self.pop = None

    def solve(self, problem: Union[Dict, Problem] = None, starting_solutions: Union[List, np.ndarray, Tuple] = None,
              seed: int = None) -> List['Agent']:
        """
        Args:
            problem: an instance of Problem class or a dictionary
            starting_solutions: List or 2D matrix (numpy array) of starting positions with length equal pop_size parameter
            seed: seed for random number generation needed to be *explicitly* set to int value

        Returns:
            g_best: g_best, the best found agent, that hold the best solution and the best target. Access by: .g_best.solution, .g_best.target
        """
        self.check_problem(problem, seed)
        self.initialize_variables()

        self.before_initialization(starting_solutions)
        self.initialization()
        self.after_initialization()

        self.before_main_loop()
        for epoch in range(1, self.epoch + 1):
            # Evolve method will be called in child class
            time_epoch = time.perf_counter()
            self.evolve(epoch)
            self.update_pareto(self.pop)
            time_epoch = time.perf_counter() - time_epoch
            self.track_optimize_step(self.pop, self.pareto, epoch, time_epoch)
        self.track_optimize_process()
        return self.pareto

    def track_optimize_step(self, pop: List[Agent] = None, pareto: List[Agent] = None, epoch: int = None, runtime: float = None) -> None:
        """
        Save some historical data and print out the detailed information of training process in each epoch

        Args:
            pop: the current population
            pareto:
            epoch: current iteration
            runtime: the runtime for current iteration
        """
        # Save history data
        if self.problem.save_population:
            self.history.list_population.append(self.duplicate_pop(pop))
        pareto_clone = self.duplicate_pop(pareto)
        self.history.list_global_best_agents.append(pareto_clone)
        self.history.list_current_best_agents.append(pareto_clone)
        # Print epoch

        self.logger.info(f">>>Problem: {self.problem.name}, Epoch: {epoch}, Current best: {self.pareto[-1].target.objectives}, Runtime: {runtime:.5f} seconds")

    def track_optimize_process(self) -> None:
        """
        Save some historical data after training process finished
        """
        self.history.list_global_best_agents = self.history.list_global_best_agents[1:]
        self.history.list_current_best_agents = self.history.list_current_best_agents[1:]

    def generate_empty_agent(self, solution: np.ndarray = None) -> Agent:
        """
        Generate new agent with solution

        Args:
            solution (np.ndarray): The solution
        """
        if solution is None:
            solution = self.problem.generate_solution(encoded=True)
        return Agent(solution=solution)

    def generate_agent(self, solution: np.ndarray = None) -> Agent:
        """
        Generate new agent with full information

        Args:
            solution (np.ndarray): The solution
        """
        agent = self.generate_empty_agent(solution)
        agent.target = self.get_target(agent.solution)
        return agent

    def generate_population(self, pop_size: int = None) -> List[Agent]:
        return [self.generate_agent() for _ in range(0, pop_size)]

    def amend_solution(self, solution: np.ndarray) -> np.ndarray:
        """
        This function is based on optimizer strategy.
        """
        return solution

    def correct_solution(self, solution: np.ndarray) -> np.ndarray:
        solution = self.amend_solution(solution)
        return self.problem.correct_solution(solution)

    def get_target(self, solution: np.ndarray) -> Target:
        return self.problem.get_target(solution)

    @staticmethod
    def duplicate_pop(pop: List[Agent]) -> List[Agent]:
        return [agent.copy() for agent in pop]

    def update_pareto(self, pop: List["Agent"]):
        all_pop = pop + self.pareto
        self.pareto = find_non_dominated(all_pop)

    def update_population(self, pop: List['Agent']) -> List['Agent']:
        return merge_population_by_ref_dirs(self.ref_dirs, pop, self.pop_size)