#!/usr/bin/env python
"""
Runs experiment with custom domain - 9x9-2Path0.txt
"""
__author__ = "Richard Liaw"
from rlpy.Domains import RCCar
from rlpy.Agents import SARSA, Q_Learning
from rlpy.Representations import Tabular, IncrementalTabular, CustomIncreTabular
from rlpy.Policies import eGreedy
from rlpy.Experiments import ExperimentSegment, Experiment
from rlpy.Tools import deltaT, clock, hhmmss, getTimeStr
from rlpy.CustomDomains import TestRCCar, RCSegment
# from .. import visualize_trajectories as visual
import os
import numpy as np


def make_experiment(exp_id=1, path="./Results/Experiments/TrialCar/" + getTimeStr() + "/"):
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
    # domain =  RCSegment(noise=0.01, episodeCap=100, with_collision=True)
    opt["performance_domain"] =  RCSegment(goal=[0.5, 0.3, None, np.pi / 3], noise=0.01, episodeCap=100)
    opt["domain"] = RCSegment(goal=[0.5, 0.3, None, np.pi / 3], noise=0.1, episodeCap=100, rewardfile="../reward/reward.json")

    ## Representation
    # discretization only needed for continuous state spaces, discarded otherwise
    representation  = CustomIncreTabular(domain, discretization=20)

    ## Policy
    policy = eGreedy(representation, epsilon=0.3) ## Need to change this back, limiting noise ATM

    ## Agent
    opt["agent"] = Q_Learning(representation=representation, policy=policy,
                   discount_factor=domain.discount_factor,
                       initial_learn_rate=0.3, learn_rate_decay_mode='const')
    opt["checks_per_policy"] = 20
    opt["max_eps"] = 300
    opt["num_policy_checks"] = 40
    experiment = ExperimentSegment(**opt)
    return experiment


if __name__ == '__main__':
    experiment = make_experiment(1, path="./Results/Experiments/TrialCar/" + getTimeStr() + "/")
    experiment.run(visualize_steps=False,  # should each learning step be shown?
                   visualize_learning=False,
                   visualize_performance=False)  # show policy / value function?
                   # saveTrajectories=False)  # show performance runs?

    # visual.saveDomain(experiment, GridWorldInter, maze)
    # import ipdb; ipdb.set_trace()
    experiment.domain.showLearning(experiment.agent.representation)

    # experiment.plotTrials(save=True)
    # experiment.plot(save=True, x = "learning_episode") #, y="reward")
    experiment.save()

