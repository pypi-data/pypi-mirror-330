"""
Any MDP Task Sampler
"""
import numpy
import gym
import pygame
import time
from numpy import random
from copy import deepcopy
from l3c.utils import pseudo_random_seed, RandomMLP, RandomGoal
from l3c.anymdp.solver import check_task_trans, check_task_rewards


def sample_action_mapping(task):
    ndim = task['ndim']
    action_dim = task['action_dim']
    s_map = RandomMLP(ndim, ndim, activation='tanh', biases=True)
    a_map = RandomMLP(action_dim, ndim, activation='tanh', biases=False)
    func = lambda s,a: s_map(s) + a_map(a)

    return {"action_map": func}

def sample_observation_mapping(task):
    ndim = task['ndim']
    observation_dim = task['state_dim']
    # Add partial observability to the environment by introducing a bottleneck of lower dimensionality
    observation_map = RandomMLP(ndim, observation_dim,
        n_hidden_layers=random.randint(max(ndim - 3, 3), ndim + 1), 
        activation=['none','tanh'],
        biases=[True, False])
    return {
        "observation_map": observation_map
    }

def sample_born_loc(task):
    born_loc_num = random.randint(1, 10)
    born_loc = [(random.uniform(- 0.9 * task['box_size'], 0.9 * task['box_size'], 
                size=(task['ndim'],)), 
                random.exponential(0.10,)) for i in range(born_loc_num)]
    return {"born_loc": born_loc}

def sample_goal_statictrigger(task, num=None):
    if(num is None):
        goal_num = random.randint(1, 10)
    else:
        goal_num = num

    repetitive_loc = [loc for loc, _ in task['born_loc']]
    for goal in task["goals"]:
        if(goal.reward_type.find('t') != -1):
            repetitive_loc.append(goal.position(0))
    for i in range(goal_num):
        goal = RandomGoal(task['ndim'],
                                repetitive_position=repetitive_loc,
                                type='static',
                                reward_type='t',
                                box_size=task['box_size'])
        repetitive_loc.append(goal.position(0))
        task["goals"].append(goal)

def sample_goal_pitfalls(task, num=None):
    if(num is None):
        goal_num = max(0, random.randint(-50, 150))
    else:
        goal_num = num
    repetitive_loc = [loc for loc, _ in task['born_loc']]
    for goal in task["goals"]:
        if(goal.reward_type.find('t') != -1):
            repetitive_loc.append(goal.position(0))
    for i in range(goal_num):
        goal = RandomGoal(task['ndim'],
                                repetitive_position=repetitive_loc,
                                is_pitfall=True,
                                type='static',
                                reward_type='t',
                                box_size=task['box_size'])
        repetitive_loc.append(goal.position(0))
        task["goals"].append(goal)

def sample_goal_potential_energy(task, num=None):
    if(num is None):
        goal_num = max(0, random.randint(-5, 5))
    else:
        goal_num = num
    for i in range(goal_num):
        task["goals"].append(RandomGoal(task['ndim'],
                                is_pitfall=random.choice([True, False]),
                                type='static',
                                reward_type='p',
                                box_size=task['box_size']))
        
def sample_goal_dynamic(task):
    task["goals"].append(RandomGoal(task['ndim'],
                                    type='fourier',
                                    reward_type='f',
                                    box_size=task['box_size']))

def sample_universal_reward(task):
    ndim = task['ndim']
    random_reward_fields = RandomMLP(ndim, 1, 
                        n_hidden_layers=random.randint(ndim * 2, ndim *4), 
                        activation=['sin', 'tanh'],
                        biases=[True, False])
    factor = random.exponential(1.0)
    func = lambda x: factor * max(random_reward_fields(x) - 0.5, 0.0)
    return {"random_reward_fields": func}

def AnyMDPv2TaskSampler(state_dim:int=256,
                 action_dim:int=256,
                 seed=None,
                 verbose=False):
    # Sampling Transition Matrix and Reward Matrix based on Irwin-Hall Distribution and Gaussian Distribution
    # Task:
    # mode: static goal or moving goal
    # ndim: number of inner dimensions
    # born_loc: born location and noise
    # sgoal_loc: static goal location, range of sink, and reward
    # pf_loc: pitfall location, range of sink, and reward
    # line_potential_energy: line potential energy specified by direction and detal_V
    # point_potential_energy: point potential energy specified by location and detal_V

    if(seed is not None):
        random.seed(seed)
    else:
        random.seed(pseudo_random_seed())

    task = dict()
    mode = random.choice(["static", "dynamic", "universal"])
    # static: static goal, one-step reward with reset
    # dynamic: moving goal, continuous reward
    # universal: an random reward field generated by a neural network

    task["mode"] = mode
    task["box_size"] = 2
    task["state_dim"] = state_dim
    task["action_dim"] = action_dim
    task["ndim"] = random.randint(4, 16) # At most 32-dimensional space
    task["max_steps"] = random.randint(100, 1000) # At most 10-dimensional space
    task["action_weight"] = random.uniform(0.01, 0.05, size=(task['ndim'],))
    task["average_cost"] = random.exponential(0.01) * random.choice([-2, -1, 0, 1])
    task["transition_noise"] = max(0, random.normal(scale=1.0e-4))
    task["reward_noise"] = max(0, random.normal(scale=1.0e-4))

    task["goals"] = []

    task.update(sample_observation_mapping(task)) # Observation Model
    task.update(sample_action_mapping(task)) # Action Mapping
    task.update(sample_born_loc(task)) # Born Location

    if(task['mode'] == 'static') :
        sample_goal_statictrigger(task, num=1) # Static Goal Location
    elif(task['mode'] == 'dynamic'):
        sample_goal_dynamic(task) # Moving Goal Location
    elif(task['mode'] == 'universal'):
        task.update(sample_universal_reward(task)) # Others, use a random field

    if(random.random() < 0.7):
        sample_goal_pitfalls(task)
    if(random.random() < 0.5):
        sample_goal_potential_energy(task)

    return task