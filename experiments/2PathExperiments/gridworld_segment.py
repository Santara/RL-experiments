#!/usr/bin/env python
"""
Runs experiment with custom domain - 7x7-Segment.txt
"""
__author__ = "Robert H. Klein"
from rlpy.CustomDomains import GridWorldInter, GridWorld
from rlpy.Agents import SARSA, Q_Learning
from rlpy.Representations import Tabular
from rlpy.Policies import eGreedy
from rlpy.Experiments import ExperimentDelayed, Experiment
from rlpy.Tools import deltaT, clock, hhmmss, getTimeStr
import visualize_trajectories as visual
import os


maze = os.path.join(GridWorldInter.default_map_dir, '7x7-Segment.txt') 

def make_experiment(exp_id=1, path="./Results/Experiments/Segment/" + getTimeStr() + "/", save=False):
    """
    Each file specifying an experimental setup should contain a
    make_experiment function which returns an instance of the Experiment
    class with everything set up.

    @param id: number used to seed the random number generators
    @param path: output directory where logs and results are stored
    """
    opt = {}
    opt["exp_id"] = exp_id
    opt["path"] = path

    ## Domain:
    domain = GridWorld(maze, noise=0.01)
    opt["domain"] = domain

    ## Representation
    # discretization only needed for continuous state spaces, discarded otherwise
    representation  = Tabular(domain, discretization=20)

    ## Policy
    policy = eGreedy(representation, epsilon=0.1) ## Need to change this back, limiting noise ATM

    ## Agent
    opt["agent"] = Q_Learning(representation=representation, policy=policy,
                   discount_factor=domain.discount_factor,
                       initial_learn_rate=0.3)
    opt["checks_per_policy"] = 50
    opt["max_steps"] = 2000
    opt["num_policy_checks"] = 10
    # experiment = ExperimentDelayed(**opt)
    experiment = Experiment(**opt)
    return experiment


# ## DEBUG
# import ipdb; ipdb.set_trace()
# ########


if __name__ == '__main__':
    experiment = make_experiment(1)
    experiment.run(visualize_steps=False,  # should each learning step be shown?
                   visualize_learning=False,  # show policy / value function per step?
                   saveTrajectories=False)  # show trajectories runs?
    # experiment.plotTrials(save=True)

    import ipdb; ipdb.set_trace()
    visual.saveDomain(experiment, GridWorld, maze)

    experiment.domain.showLearning(experiment.agent.representation)

    experiment.plot(save=True)
    experiment.save()

