#!/usr/bin/env python
"""
Runs experiment with custom domain
"""
__author__ = "Richard Liaw"
import rlpy
from rlpy.Tools import deltaT, clock, hhmmss, getTimeStr
# from .. import visualize_trajectories as visual
import os
import yaml
import shutil

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        ret_val = yaml.load(f)
    return ret_val

def run_experiment_params(param_path='./params.yaml'):
    params = type("Parameters", (), load_yaml(param_path))

    domain = eval(params.domain)(**params.domain_params)
    performance_domain = eval(params.performance_domain)(**params.performance_params)
    representation = eval(params.representation)(domain, **params.representation_params)
    policy = eval(params.policy)(representation, **params.policy_params)
    agent = eval(params.agent)(policy, representation,
             discount_factor=domain.discount_factor, **params.agent_params)

    opt = {}
    opt["exp_id"] = params.exp_id
    opt["path"] = params.results_path + getTimeStr() + "/"
    opt["domain"] = domain
    opt["performance_domain"] = performance_domain
    opt["agent"] = agent
    opt["checks_per_policy"] = params.checks_per_policy
    opt["max_eps"] = params.max_eps
    opt["num_policy_checks"] = params.num_policy_checks

    if not os.path.exists(opt["path"]):
        os.makedirs(opt["path"])

    shutil.copy(param_path, opt["path"] + "params.yml")

    return eval(params.experiment)(**opt)


if __name__ == '__main__':
    import sys
    experiment = run_experiment_params(sys.argv[1])
    experiment.domain.s0()
    experiment.domain.showDomain(None)
