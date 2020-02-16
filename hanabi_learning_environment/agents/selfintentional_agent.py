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
    self.last_action = None
    self.memory = [] # stores observations since last turn
    self.mental_state = []
    self.unplayed_cards = [[3, 3, 3, 3, 3],
                           [2, 2, 2, 2, 2],
                           [2, 2, 2, 2, 2],
                           [2, 2, 2, 2, 2],
                           [1, 1, 1, 1, 1]]

    # initial mental state RGBWY, 12345
    # mental_state[card][rank][color]
    self.color_encoding = {'R': 0, 'G': 1, 'B': 2, 'W': 3, 'Y': 4}
    for i in range(5):
      self.mental_state.append([[3, 3, 3, 3, 3],
                                [2, 2, 2, 2, 2],
                                [2, 2, 2, 2, 2],
                                [2, 2, 2, 2, 2],
                                [1, 1, 1, 1, 1]])

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
    # if len(self.memory) > self.config['players']:
    #   self.memory.pop(0)

  def update_unplayed_cards(self, observation):
    cards = [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

    for key in observation['fireworks'].keys():
      if observation['fireworks'][key] != 0:
        for rank in range(observation['fireworks'][key]):
          cards[rank][self.color_encoding[key]] +=1
          if 4 in cards[0] or 3 in cards[1] or 3 in cards[2] or 3 in cards[3] or 2 in cards[4]:
            print('mistake in fireworks')

    for d in observation['discard_pile']:
      cards[d['rank']][self.color_encoding[d['color']]] += 1
      if 4 in cards[0] or 3 in cards[1] or 3 in cards[2] or 3 in cards[3] or 2 in cards[4]:
        print('mistake in discardpile')

    for hand in observation['observed_hands']:
      for c in hand:
        if c['color'] is not None and c['rank'] != -1:
          cards[c['rank']][self.color_encoding[c['color']]] += 1
          if 4 in cards[0] or 3 in cards[1] or 3 in cards[2] or 3 in cards[3] or 2 in cards[4]:
            print('mistake in hands')

    for c in observation['card_knowledge'][0]:
      if c['color'] is not None and c['rank'] is not None:
        cards[c['rank']][self.color_encoding[c['color']]] += 1
        if 4 in cards[0] or 3 in cards[1] or 3 in cards[2] or 3 in cards[3] or 2 in cards[4]:
          print('mistake in knowledge')

    print('counted cards: ', cards)
    print(self.last_action)
    cards_in_game = [[3, 3, 3, 3, 3],
                     [2, 2, 2, 2, 2],
                     [2, 2, 2, 2, 2],
                     [2, 2, 2, 2, 2],
                     [1, 1, 1, 1, 1]]

    for r, rank in enumerate(self.unplayed_cards):
      for color in range(len(rank)):
        self.unplayed_cards[r][color] = cards_in_game[r][color] - cards[r][color]

    print('unplayed cards', self.unplayed_cards)


  # in here sth goes wrong
  def update_mental_state(self, observation):
    card_knowledge = [card.__str__() for card in observation['pyhanabi'].card_knowledge()[0]]
    print(card_knowledge)

    if self.last_action is not None:
      if self.last_action['action_type'] == 'DISCARD' or self.last_action['action_type'] == 'PLAY':

        self.mental_state.pop(self.last_action['card_index'])
        self.mental_state.append(self.unplayed_cards)


    for card_idx, knowledge in enumerate(card_knowledge):
      possibility_knowledge = knowledge.split('|')[1]

      for color in ['R','G', 'B', 'W', 'Y']:
        if color not in possibility_knowledge:
          for i in range(5):
            self.mental_state[card_idx][i][self.color_encoding[color]] = 0

      for rank in ['1','2','3','4','5']:
        if rank not in possibility_knowledge:
          for i in range(5):
            self.mental_state[card_idx][int(rank)-1][i] = 0

    for i, card in enumerate(self.mental_state):
      for r, rank in enumerate(card):
        for c, color in enumerate(rank):
          if self.mental_state[i][r][c] != 0:
            self.mental_state[i][r][c] = self.unplayed_cards[r][c]


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
    # self.update_memory(observation)
    self.update_unplayed_cards(observation)
    self.update_mental_state(observation)
    # print(self.mental_state)



    # print('unplayed cards: ', self.unplayed_cards)
    if observation['current_player_offset'] == 0:
      print('Current Player Mental State: ', self.mental_state)

      action = rules.PlaySafeCard(observation)
      if action is None:
        action = rules.OsawaDiscard(observation)
      if action is None:
        action = rules.TellPlayableCard(observation)
      if action is None:
        action = rules.TellRandomly(observation)
      if action is None:
        action = rules.DiscardRandomly(observation)
      self.last_action = action
      return action

    else:
      print('Other players menta; state: ', self.mental_state)
      return None