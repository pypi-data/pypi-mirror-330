import numpy as np
from moalpy.multi_objectives.dominator import Dominator
from typing import List
from moalpy.utils.agent import Agent


def find_non_dominated(agents: List['Agent']) -> List['Agent']:
    objectives = np.array([agent.target.objectives for agent in agents])
    domination_matrix = Dominator.calc_domination_matrix(objectives, None)
    pareto_index = np.where(np.all(domination_matrix >= 0, axis=1))[0]

    pareto_agents = {}
    for index, agent in enumerate(agents):
        if index not in pareto_index: continue
        if any(agent.target.is_equal(ut.target) for ut in pareto_agents.values()): continue

        pareto_agents[agent.target] = agent

    return list(pareto_agents.values())