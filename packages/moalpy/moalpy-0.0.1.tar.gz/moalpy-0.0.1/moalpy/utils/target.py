from typing import Union, List, Tuple
import numbers
import numpy as np


class Target:
    SUPPORTED_ARRAY = [tuple, list, np.ndarray]

    def __init__(self, objectives: Union[List, Tuple, np.ndarray] = None) -> None:
        """
        Initialize the Target with a list of objectives and a fitness value.

        Parameters:
            objectives: The list of objective values.
        """
        self._objectives = None
        self.set_objectives(objectives)

    def copy(self) -> 'Target':
        return Target(self.objectives)

    @property
    def objectives(self):
        """Returns the list of objective values."""
        return self._objectives

    def set_objectives(self, objs):
        if objs is None:
            raise ValueError(f"Invalid objectives. It should be a list, tuple, np.ndarray, int or float.")
        else:
            if type(objs) not in self.SUPPORTED_ARRAY:
                if isinstance(objs, numbers.Number):
                    objs = [objs]
                else:
                    raise ValueError(f"Invalid objectives. It should be a list, tuple, np.ndarray, int or float.")
            objs = np.array(objs).flatten()
        self._objectives = objs

    def is_equal(self, other: 'Target') -> bool:
        return np.array_equal(np.array(self.objectives), np.array(other.objectives))

    def __str__(self):
        return f"Objectives: {self.objectives}"