import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd


class History:
    def __init__(self, optimizer_name, **kwargs):
        self.optimizer_name = optimizer_name
        self.list_current_best_agents = []
        self.list_global_best_agents = []

        self.list_population = []
        self._set_keyword_arguments(kwargs)

    def _set_keyword_arguments(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def visualize_pareto(self, dim_fitness=(1, 2)):
        if len(dim_fitness) != 2:
            print("The dim fitness should be 2 values")

        plt.rc('font', family='Helvetica')
        fig, ax = plt.subplots()

        objectives = [a.target.objectives for a in self.list_global_best_agents[-1]]
        x = [o[dim_fitness[0] - 1] for o in objectives]
        y = [o[dim_fitness[1] - 1] for o in objectives]

        plt.grid(True, linestyle='--', color='gray', linewidth=0.5)
        plt.gca().set_axisbelow(True)
        ax.set_title("Pareto")
        for index in reversed(range(len(x))):
            ax.scatter(x[index], y[index])

        plt.show()

    @staticmethod
    def export_to_csv(result: pd.DataFrame, save_path: str):
        result.to_csv(f"{save_path}.csv", header=True, index=False, sep=";")

    def save(self, save_path):
        path_best_fit = f"{save_path}/multi_best_fit"
        path_convergence = f"{save_path}/convergence/{self.optimizer_name}"
        Path(path_best_fit).mkdir(parents=True, exist_ok=True)
        Path(path_convergence).mkdir(parents=True, exist_ok=True)

        df2 = pd.DataFrame([{"objectives": list(a.target.objectives), 'solution': list(a.solution)} for a in self.list_global_best_agents[-1]])
        self.export_to_csv(df2, f"{path_best_fit}/{self.optimizer_name}_multi_best_fit")