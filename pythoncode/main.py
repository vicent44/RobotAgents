# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
from typing import Dict
import curlsac
import matplotlib.pyplot as plt
import os
import argparse
import torch
from copy import deepcopy
from utils import ReplayBuffer
from mlagents_envs.environment import UnityEnvironment

from yaml_operations import load_yaml


def main():
    # This is a non-blocking call that only loads the environment.
    """env = UnityEnvironment(file_name=None)

    # Start interacting with the environment.
    env.reset()
    env.reset()
    # print(env.behavior_spec.observation_shapes)

    episodes = 500  # Number of games (number of times that succed the goal)
    num_train_steps = 1000  # The number of training steps that will be performed
    num_new_ext = 1000 # The number of experiences to collect per training step
    buffer_size = 10000 # The maximum size of the Buffer
    batch_size = 32
    stached_frames = 3
    dimension_h = 84
    dimension_w = 84

    # batch_observation = np.empty((batch_size, stached_frames, dimension_h, dimension_w))
    batch_observation = []
    im = np.random.randint(0, 255, (16, 16))
    print(im.shape, type(im))"""

    #1 - First take the config of the yml file for the algorithm
    #2 - Open the Unity environment and initiate the neural networks
    #3 - Initialize unity (agents)
    #4 - Run simulation

    args = load_yaml("config.yaml")
    env = init_unity_env(args["unity_wrapper"])

    action_shape = env.behavior_spec.action_size.shape
    obs_shape = (3 * args["environment"]["frame_stack"], args["environment"]["image_size_post"], args["environment"]["image_size_post"])
    pre_aug_obs_shape = (3 * args["environment"]["frame_stack"], args["environment"]["image_size_pre"], args["environment"]["image_size_pre"])
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    replay_buffer = ReplayBuffer(
        obs_shape = pre_aug_obs_shape,
        action_shape= action_shape,
        capacity= args["environment"]["buffer_size"],
        batch_size= args["environment"]["batch_size"],
        device=device,
        image_size= args["environment"]["image_size_post"]
    )






"""
    #Number of times that the goal if succed
    for n in range(num_train_steps):
        #number of steps maximum that have the agent to get the goal
        for steps in range(max_steps):
            behavior_names, behavior_spec = env.behavior_specs
            print(behavior_spec, behavior_names[1])

            behavior_name_left = list(env.behavior_specs)[0]
            behavior_name_right = list(env.behavior_specs)[1]

            spec =env.behavior_specs[behavior_name_left]

            # Examine the number of observations per Agent
            print("Number of observations : ", len(spec.observation_shapes))

            # Is there a visual observation ?
            # Visual observation have 3 dimensions: Height, Width and number of channels
            vis_obs = any(len(shape) == 3 for shape in spec.observation_shapes)
            print("Is there a visual observation ?", vis_obs)

            print(f"There are {spec.action_size} action(s)")

            # For discrete actions only : How many different options does each action has ?
            if spec.is_action_discrete():
                for action, branch_size in enumerate(spec.discrete_action_branches):
                    print(f"Action number {action} has {branch_size} different options")

            decision_steps_left, terminal_steps_left = env.get_steps(behavior_name_left)
            decision_steps_right, terminal_steps_right = env.get_steps(behavior_name_right)
            print(decision_steps_left.reward, decision_steps_right.reward)


            if (steps % 4) == 0:
                image = get_image(decision_steps_left[0].obs[0], 1)
                image = get_image(decision_steps_right[0].obs[0], 1)
            else:
                image = concatenate_image(image, get_image(decision_steps_left[0].obs[0], 1))

            if image.shape[0] == 4:
                batch_images = add_batch_dimension(image, batch_size)
                print(batch_images.shape)

                actions = []
                actions.append(np.random.uniform(0, 6, 1))
                env.set_actions(behavior_name_left, np.array(actions))
                env.set_actions(behavior_name_right, np.array(actions))

            env.step()


        batch_observation.append(decision_steps_left[0].obs[0])
        print(len(batch_observation))
        if len(batch_observation) == 4:
            print( len(batch_observation))
            observation = decision_steps_left[0].obs[0]
            prova = np.transpose(observation, (2, 0, 1))
            image_observation = observation[:,:,0]
            print(observation[:,:,0].shape, type(batch_observation[0]), prova.shape)
            #temp = decision_steps_left[0].obs[0]
            plt.imshow(observation[:,:,0])
            plt.show()
            if np.array_equal(batch_observation[0],batch_observation[3]) :
                print("equal")
            batch_observation.clear()
            actions = []
            actions.append(np.random.uniform(0,6,1))
            print(len(actions))
            env.set_actions(behavior_name_left, np.array(actions))
            env.set_actions(behavior_name_right, np.array(actions))
        #print(type(decision_steps_left[0].obs[0]))
            env.step()
    for observation in decision_steps_left[0].obs:
        print(observation.shape)
        if len(observation.shape) == 3 :
            print("uno")
    #print(get_behavior_spec)"""

    #print(decision_steps_left.agent_id[0], decision_steps_right.agent_id[0])
    #print(terminal_steps_left.agent_id, terminal_steps_right.agent_id)
    #if():
    #    env

    #h, w = env.behavior_specs.obserbation_shapes[1:]
    #print(decision_steps_left.obs, h, w)

    #curl(decision_steps_left)

    #env.step()

    #print(len(decision_steps_left), len(terminal_steps_left), behavior_name_left)
    #print(len(decision_steps_right), len(terminal_steps_right), behavior_name_right)
    #tracked_agent = decision_steps.agent_id[0]

    #print(list(decision_steps), list(terminal_steps), tracked_agent)

def get_image(observation, color):
    transpose_observation = np.transpose(observation, (2, 0, 1))
    if color == 1:
        image_observation = transpose_observation[ 0:1,:,:]
    elif color == 3:
        image_observation = transpose_observation[ 0:3,:,:]
    return image_observation

def concatenate_image(image_stack, new_image):
    new_image_stack = np.concatenate((image_stack, new_image))
    return new_image_stack

def add_batch_dimension(image_stack, batch_stack):
    batch_stack_image = np.expand_dims(image_stack, axis = 0)
    batch_stack_image = np.vstack([batch_stack_image]*batch_stack)
    return batch_stack_image

def init_unity_env(env_args):
    from unity_wrapper import (UnityWrapper, UnityReturnWrapper,
                                InfoWrapper, ActionWrapper, StackVisualWrapper)
    env_kargs = deepcopy(env_args)
    env = UnityWrapper(env_kargs)
    print('Unity UnityWrapper success.')

    env = InfoWrapper(env, env_kargs)
    print('Unity InfoWrapper success.')

    if env_args['frame_stack'] > 1:
        env = StackVisualWrapper(env, stack_nums=env_kargs['stack_visual_nums'])
        print('Unity StackVisualWrapper success.')
    else:
        env = UnityReturnWrapper(env)
        print('Unity UnityReturnWrapper success.')

    env = ActionWrapper(env)
    print('Unity ActionWrapper success.')

    return env


if __name__ == "__main__":
    main()