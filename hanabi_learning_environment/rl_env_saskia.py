# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A simple episode runner using the RL environment."""

from __future__ import print_function

import sys
import getopt
import rl_env
from agents.random_agent import RandomAgent
from agents.simple_agent import SimpleAgent
from agents.rulebased_agent import RuleBasedAgent
from agents.selfintentional_agent import SelfIntentionalAgent
from pyhanabi import ObservationEncoder

AGENT_CLASSES = {'SimpleAgent': SimpleAgent, 'RandomAgent': RandomAgent, 'RuleBasedAgent': RuleBasedAgent, 'SelfIntentionalAgent': SelfIntentionalAgent}


class Runner(object):
  """Runner class."""

  def __init__(self, flags):
    """Initialize runner."""
    self.flags = flags
    self.agent_config = {'players': ['players']}
    self.environment = rl_env.make('Hanabi-Full', num_players=flags['players'])
    self.agent_class = AGENT_CLASSES[flags['agent_class']]


  def run(self):
    """Run episodes."""
    rewards = []
    for episode in range(flags['num_episodes']):
      observations = self.environment.reset()
      agents = [self.agent_class(self.agent_config)
                for _ in range(self.flags['players'])]
      done = False
      episode_reward = 0
      while not done:
        for agent_id, agent in enumerate(agents):
          observation = observations['player_observations'][agent_id]
          # card_knowledge = [card.__str__() for card in observation['pyhanabi'].card_knowledge()[0]]
          print(observation)
          action = agent.act(observation)
          if observation['current_player'] == agent_id:
            assert action is not None
            current_player_action = action

          else:
            assert action is None
        print('---------------------------------------------------------------')

        # Make an environment step.
        # print('Agent: {} action: {}'.format(observation['current_player'],
        #                                     current_player_action))
        observations, reward, done, unused_info = self.environment.step(
            current_player_action)
        episode_reward += reward
      rewards.append(episode_reward)
      print('Running episode: %d' % episode)
      print('Max Reward: %.3f' % max(rewards))
    return rewards

  # def run(self):
  #   """Run episodes."""
  #   rewards = []
  #   for episode in range(flags['num_episodes']):
  #     observations = self.environment.reset()
  #     agents = [self.agent_class(self.agent_config)
  #               for _ in range(self.flags['players'])]
  #     done = False
  #     episode_reward = 0
  #     while not done:
  #       for agent_id, agent in enumerate(agents):
  #         observation = observations['player_observations'][agent_id]
  #         if observation['current_player'] == agent_id:
  #           if observation['current_player_offset'] == 0:
  #             old_observation = observation
  #             action, observations, reward, done, unused_info = agent.act(observation, self.environment)
  #             current_player_observation = observation
  #             current_player_observation_encoded = current_player_observation['vectorized']
  #             # print(current_player_observation['pyhanabi'])
  #             # print('-------------------------------------------------------')
  #             # done = True
  #           # observation1 = observations['player_observations'][agent_id]
  #           # agent.learn(observation, action, observation1, reward)
  #
  #         # Make an environment step.
  #       # print('Agent: {} action: {}'.format(observation['current_player'],
  #       #                                     action))
  #       episode_reward += reward
  #     rewards.append(episode_reward)
  #     # print('Running episode: %d' % episode)
  #     # print('Max Reward: %.3f' % max(rewards))
  #   return rewards

if __name__ == "__main__":
  flags = {'players': 2, 'num_episodes': 1, 'agent_class': 'SelfIntentionalAgent'}
  options, arguments = getopt.getopt(sys.argv[1:], '',
                                     ['players=',
                                      'num_episodes=',
                                      'agent_class='])
  if arguments:
    sys.exit('usage: rl_env_saskia.py [options]\n'
             '--players       number of players in the game.\n'
             '--num_episodes  number of game episodes to run.\n'
             '--agent_class   {}'.format(' or '.join(AGENT_CLASSES.keys())))
  for flag, value in options:
    flag = flag[2:]  # Strip leading --.
    flags[flag] = type(flags[flag])(value)
  runner = Runner(flags)
  rewards = runner.run()