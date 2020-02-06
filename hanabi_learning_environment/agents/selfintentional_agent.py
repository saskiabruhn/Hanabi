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
"""Random Agent."""

import numpy as np
from hanabi_learning_environment.rl_env import Agent
import agents.rules as rules

class SelfIntentionalAgent(Agent):
  """Agent that takes random legal actions."""

  def __init__(self, config, *args, **kwargs):
    r"""Initialize the agent.

    Args:
      config: dict, With parameters for the game. Config takes the following
        keys and values.
          - colors: int, Number of colors \in [2,5].
          - ranks: int, Number of ranks \in [2,5].
          - players: int, Number of players \in [2,5].
          - hand_size: int, Hand size \in [4,5].
          - max_information_tokens: int, Number of information tokens (>=0)
          - max_life_tokens: int, Number of life tokens (>=0)
          - seed: int, Random seed.
          - random_start_player: bool, Random start player.
      *args: Optional arguments
      **kwargs: Optional keyword arguments.

    Raises:
      AgentError: Custom exceptions.
    """
    self.config = config
    self.memory = [] # stores observations since last turn
    #initial mental state RGBWY, 12345
    # mental_state[card][rank][color]
    self.color_encoding = {'R':0, 'G': 1, 'B': 2, 'W': 3, 'Y': 4}
    self.mental_state = np.array([[[3, 3, 3, 3, 3],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [1, 1, 1, 1, 1]],
                                 [[3, 3, 3, 3, 3],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [1, 1, 1, 1, 1]],
                                 [[3, 3, 3, 3, 3],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [1, 1, 1, 1, 1]],
                                 [[3, 3, 3, 3, 3],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [1, 1, 1, 1, 1]],
                                 [[3, 3, 3, 3, 3],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [2, 2, 2, 2, 2],
                                  [1, 1, 1, 1, 1]]])


      # self.mental_state = {'R':{'1': 3, '2': 2, '3': 2, '4': 2, '5': 1},
      #                      'G':{'1': 3, '2': 2, '3': 2, '4': 2, '5': 1},
      #                      'B':{'1': 3, '2': 2, '3': 2, '4': 2, '5': 1},
      #                      'W':{'1': 3, '2': 2, '3': 2, '4': 2, '5': 1},
      #                      'Y':{'1': 3, '2': 2, '3': 2, '4': 2, '5': 1}, }

  def reset(self, config):
    r"""Reset the agent with a new config.

    Signals agent to reset and restart using a config dict.

    Args:
      config: dict, With parameters for the game. Config takes the following
        keys and values.
          - colors: int, Number of colors \in [2,5].
          - ranks: int, Number of ranks \in [2,5].
          - players: int, Number of players \in [2,5].
          - hand_size: int, Hand size \in [4,5].
          - max_information_tokens: int, Number of information tokens (>=0)
          - max_life_tokens: int, Number of life tokens (>=0)
          - seed: int, Random seed.
          - random_start_player: bool, Random start player.
    """
    self.config = config


  def update_memory(self, observation):
    self.memory.append(observation)
    if len(self.memory) > self.config['players']:
      self.memory.pop(0)

  def observation_diff(self, observation):
    last_observation = self.memory[-2]
    diff = {'R':[], 'G':[], 'B':[], 'W':[], 'Y':[]}

    for key in observation['fireworks'].keys():
      if last_observation['fireworks'][key] != observation['fireworks'][key]:
        diff[key].append(observation['fireworks'][key])

    for h, hand in enumerate(observation['observed_hands']):
      for c, card in enumerate(hand):
        if card['color'] != last_observation['observed_hands'][h][c]['color']:
          diff[card['color']].append(card['rank'])
        if card['rank'] != last_observation['observed_hands'][h][c]['rank']:
          diff[card['color']].append(card['rank'])

    for k, knowledge in enumerate(observation['card_knowledge']):
      for c, card in enumerate(knowledge):
        if card['color'] != last_observation['card_knowledge'][k][c]['color']:
          diff[card['color']].append(card['rank'])
        if card['rank'] != last_observation['card_knowledge'][k][c]['rank']:
          diff[card['color']].append(card['rank'])

    if len(observation['discard_pile']) > len(last_observation['discard_pile']):
      diff[observation['discard_pile'][-1]['color']].append(observation['discard_pile'][-1]['rank'])

    return diff


  def update_mental_state(self, observation):
      for k, knowledge in enumerate(observation['card_knowledge']):
          for c, card in enumerate(knowledge):
              if card['color'] != last_observation['card_knowledge'][k][c]['color']:
                  if card['rank'] is not None:
                      self.mental_state[c].fill(0)
                      self.mental_state[c][card['rank']-1][self.color_encoding[card['color']]] = 1
                  else:
                      for i in range(5):
                          if i != self.color_encoding[card['color']]:
                              self.mental_state[c][:][i].fill(0)

              if card['rank'] != last_observation['card_knowledge'][k][c]['rank']:
                  if card['color'] is not None:
                      self.mental_state[c].fill(0)
                      self.mental_state[c][card['rank'] - 1][self.color_encoding[card['color']]] = 1
                  else:
                      for i in range(5):
                          if i != card['rank']:
                              self.mental_state[c][i][:].fill(0)


      observation_diff = observation_diff(observation)
      for card in self.mental_state:
          for rank in card:
              for color in rank:




  def act(self, observation):
    """Act based on an observation.

    Args:
      observation: dict, containing observation from the view of this agent.
        An example:
        {'current_player': 0,
         'current_player_offset': 1,
         'deck_size': 40,
         'discard_pile': [],
         'fireworks': {'B': 0,
                   'G': 0,
                   'R': 0,
                   'W': 0,
                   'Y': 0},
         'information_tokens': 8,
         'legal_moves': [],
         'life_tokens': 3,
         'observed_hands': [[{'color': None, 'rank': -1},
                         {'color': None, 'rank': -1},
                         {'color': None, 'rank': -1},
                         {'color': None, 'rank': -1},
                         {'color': None, 'rank': -1}],
                        [{'color': 'W', 'rank': 2},
                         {'color': 'Y', 'rank': 4},
                         {'color': 'Y', 'rank': 2},
                         {'color': 'G', 'rank': 0},
                         {'color': 'W', 'rank': 1}]],
         'num_players': 2}]}

    Returns:
      action: dict, mapping to a legal action taken by this agent. The following
        actions are supported:
          - { 'action_type': 'PLAY', 'card_index': int }
          - { 'action_type': 'DISCARD', 'card_index': int }rewar
          - {
              'action_type': 'REVEAL_COLOR',
              'color': str,
              'target_offset': int >=0
            }
          - {
              'action_type': 'REVEAL_RANK',
              'rank': str,
              'target_offset': int >=0
            }
    """
    update_memory(observation)




    if observation['current_player_offset'] == 0:

      action = rules.PlaySafeCard(observation)
      if action is None:
        action = rules.OsawaDiscard(observation)
      if action is None:
        action = rules.TellPlayableCard(observation)
      if action is None:
        action = rules.TellRandomly(observation)
      if action is None:
        action = rules.DiscardRandomly(observation)
      return action

    else:
      return None