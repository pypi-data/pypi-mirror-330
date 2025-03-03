import numbers
import numpy as np
from typing import Union, List, Tuple, Dict
from moalpy.utils.space import BaseVar, IntegerVar, FloatVar, PermutationVar, StringVar, BinaryVar, BoolVar, MixedSetVar
from moalpy.utils.target import Target
from moalpy.utils.logger import Logger


class Problem:
    SUPPORTED_VARS = (IntegerVar, FloatVar, PermutationVar, StringVar, BinaryVar, BoolVar, MixedSetVar)
    SUPPORTED_ARRAYS = (list, tuple, np.ndarray)

    def __init__(self, bounds: Union[List, Tuple, np.ndarray, BaseVar], minmax: str = "min", **kwargs) -> None:
        self._bounds, self.lb, self.ub = None, None, None
        self.minmax = minmax
        self.seed = None
        self.name = "Problem"
        self.n_dims, self.save_population = None, False
        self._set_keyword_arguments(kwargs)
        self.set_bounds(bounds)
        self._set_functions()
        self.msg = 'Solving problem with multi objectives'
        self.logger = Logger().create(name=f"{__name__}.{__class__.__name__}",
                                      format_str='%(asctime)s, %(levelname)s, %(name)s [line: %(lineno)d]: %(message)s')

    @property
    def bounds(self):
        return self._bounds

    def set_bounds(self, bounds):
        if isinstance(bounds, BaseVar):
            bounds.seed = self.seed
            self._bounds = [bounds, ]
        elif type(bounds) in self.SUPPORTED_ARRAYS:
            self._bounds = []
            for bound in bounds:
                if isinstance(bound, BaseVar):
                    bound.seed = self.seed
                else:
                    raise ValueError(f"Invalid bounds. All variables in bounds should be an instance of {self.SUPPORTED_VARS}")
                self._bounds.append(bound)
        else:
            raise TypeError(f"Invalid bounds. It should be type of {self.SUPPORTED_ARRAYS} or an instance of {self.SUPPORTED_VARS}")
        self.lb = np.concatenate([bound.lb for bound in self._bounds])
        self.ub = np.concatenate([bound.ub for bound in self._bounds])

    def set_seed(self, seed: int = None) -> None:
        self.seed = seed
        for idx in range(len(self._bounds)):
            self._bounds[idx].seed = seed

    def _set_keyword_arguments(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _set_functions(self):
        tested_solution = self.generate_solution(encoded=True)
        self.n_dims = len(tested_solution)
        result = self.obj_func(tested_solution)
        if not type(result) in self.SUPPORTED_ARRAYS:
            raise ValueError(f"obj_func needs to return a multi value or a list of values")

    def obj_func(self, x: np.ndarray) -> Union[List, Tuple, np.ndarray]:
        """Objective function

        Args:
            x (numpy.ndarray): Solution.

        Returns:
            float: Function value of `x`.
        """
        raise NotImplementedError

    def get_name(self) -> str:
        """
        Returns:
            string: The name of the problem
        """
        return self.name

    def get_class_name(self) -> str:
        """Get class name."""
        return self.__class__.__name__

    @staticmethod
    def encode_solution_with_bounds(x, bounds):
        x_new = []
        for idx, var in enumerate(bounds):
            x_new += list(var.encode(x[idx]))
        return np.array(x_new)

    @staticmethod
    def decode_solution_with_bounds(x, bounds):
        x_new, n_vars = {}, 0
        for idx, var in enumerate(bounds):
            temp = var.decode(x[n_vars:n_vars + var.n_vars])
            if var.n_vars == 1:
                x_new[var.name] = temp[0]
            else:
                x_new[var.name] = temp
            n_vars += var.n_vars
        return x_new

    @staticmethod
    def correct_solution_with_bounds(x: Union[List, Tuple, np.ndarray], bounds: List) -> np.ndarray:
        x_new, n_vars = [], 0
        for idx, var in enumerate(bounds):
            x_new += list(var.correct(x[n_vars:n_vars+var.n_vars]))
            n_vars += var.n_vars
        return np.array(x_new)

    @staticmethod
    def generate_solution_with_bounds(bounds: Union[List, Tuple, np.ndarray], encoded: bool = True) -> Union[List, np.ndarray]:
        x = [var.generate() for var in bounds]
        if encoded:
            return Problem.encode_solution_with_bounds(x, bounds)
        return x

    def encode_solution(self, x: Union[List, tuple, np.ndarray]) -> np.ndarray:
        """
        Encode the real-world solution to optimized solution (real-value solution)

        Args:
            x (Union[List, tuple, np.ndarray]): The real-world solution

        Returns:
            The real-value solution
        """
        return self.encode_solution_with_bounds(x, self.bounds)

    def decode_solution(self, x: np.ndarray) -> Dict:
        """
        Decode the encoded solution to real-world solution

        Args:
            x (np.ndarray): The real-value solution

        Returns:
            The real-world (decoded) solution
        """
        return self.decode_solution_with_bounds(x, self.bounds)

    def correct_solution(self, x: np.ndarray) -> np.ndarray:
        """
        Correct the solution to valid bounds

        Args:
            x (np.ndarray): The real-value solution

        Returns:
            The corrected solution
        """
        return self.correct_solution_with_bounds(x, self.bounds)

    def generate_solution(self, encoded: bool = True) -> Union[List, np.ndarray]:
        """
        Generate the solution.

        Args:
            encoded (bool): Encode the solution or not

        Returns:
            the encoded/non-encoded solution for the problem
        """
        return self.generate_solution_with_bounds(self.bounds, encoded)

    def constraints(self, x: np.ndarray) -> np.array:
        return [0]

    def violate_value(self):
        return 10e4

    def get_target(self, solution: np.ndarray) -> Target:
        """
        Args:
            solution: The real-value solution

        Returns:
            The target object
        """
        objs = self.obj_func(solution)
        if not np.all(self.constraints(solution) <= 0):
            objs = np.array(objs) + self.violate_value()

        return Target(objectives=objs)
