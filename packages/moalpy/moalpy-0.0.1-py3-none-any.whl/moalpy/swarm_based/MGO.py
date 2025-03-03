import numpy as np
from moalpy.optimizer import MultiObjectiveOptimizer
from moalpy.utils.agent import Agent


class OriginalMGO(MultiObjectiveOptimizer):
    def __init__(self, epoch: int = 10000, pop_size: int = 100, n_partitions=12, num_best_agent=1, **kwargs: object) -> None:
        """
        Args:
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(n_partitions, **kwargs)
        self.num_best_agent = num_best_agent
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [5, 10000])
        self.set_parameters(["epoch", "pop_size"])
        self.sort_flag = True

    def coefficient_vector__(self, n_dims, epoch, max_epoch):
        a2 = -1. + epoch * (-1. / max_epoch)
        u = self.generator.standard_normal(n_dims)
        v = self.generator.standard_normal(n_dims)
        cofi = np.zeros((4, n_dims))
        cofi[0, :] = self.generator.random(n_dims)
        cofi[1, :] = (a2 + 1) + self.generator.random()
        cofi[2, :] = a2 * self.generator.standard_normal(n_dims)
        cofi[3, :] = u * np.power(v, 2) * np.cos((self.generator.random() * 2) * u)
        return cofi

    def _generate_new_pop(self, epoch, idx_pop, best_agent: Agent):
        best_solution = best_agent.solution
        idxs_rand = self.generator.permutation(self.pop_size)[:int(np.ceil(self.pop_size / 3))]
        pos_list = np.array([self.pop[mm].solution for mm in idxs_rand])
        idx_rand = self.generator.integers(int(np.ceil(self.pop_size / 3)), self.pop_size)
        M = self.pop[idx_rand].solution * np.floor(self.generator.normal()) + np.mean(pos_list, axis=0) * np.ceil(
            self.generator.normal())

        # Calculate the vector of coefficients
        cofi = self.coefficient_vector__(self.problem.n_dims, epoch + 1, self.epoch)
        A = self.generator.standard_normal(self.problem.n_dims) * np.exp(2 - (epoch + 1) * (2. / self.epoch))
        D = (np.abs(self.pop[idx_pop].solution) + np.abs(best_solution)) * (2 * self.generator.random() - 1)

        # Update the location
        x2 = best_solution - np.abs((self.generator.integers(1, 3) * M - self.generator.integers(1, 3) * self.pop[idx_pop].solution) * A) * cofi[self.generator.integers(0, 4), :]
        x3 = M + cofi[self.generator.integers(0, 4), :] + (self.generator.integers(1, 3) * best_solution - self.generator.integers(1, 3) * self.pop[self.generator.integers(self.pop_size)].solution) * cofi[self.generator.integers(0, 4), :]
        x4 = self.pop[idx_pop].solution - D + (self.generator.integers(1, 3) * best_solution - self.generator.integers(1, 3) * M) * cofi[self.generator.integers(0, 4), :]

        x1 = self.problem.generate_solution()
        x1 = self.correct_solution(x1)
        x2 = self.correct_solution(x2)
        x3 = self.correct_solution(x3)
        x4 = self.correct_solution(x4)

        agent1 = self.generate_empty_agent(x1)
        agent2 = self.generate_empty_agent(x2)
        agent3 = self.generate_empty_agent(x3)
        agent4 = self.generate_empty_agent(x4)

        pop_new = [agent1, agent2, agent3, agent4]
        for jdx in range(-4, 0):
            pop_new[jdx].target = self.get_target(pop_new[jdx].solution)
        return pop_new

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop_new = []
        best_agents = self.get_best_agents(size=self.num_best_agent)
        for idx in range(0, self.pop_size):
            for a in best_agents:
                pop_new += self._generate_new_pop(epoch, idx, a)

        self.pop = self.update_population(self.pop + pop_new)
