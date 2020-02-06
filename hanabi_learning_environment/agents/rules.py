import random

def CardPlayable(card, fireworks):
    if card['color'] is None or card['rank'] is None:
        return False
    if fireworks[card['color']] == card['rank']:
        return True
    else:
        return False

def CardUnplayable(card, fireworks):
    if card['color'] is None or card['rank'] is None:
        return False
    if fireworks[card['color']] > card['rank']:
            return True
    else:
        return False

########################################################################################################################

def PlaySafeCard(observation):
    """
    Plays a card only if it is guaranteed that it is playable.
    :argument: observation: dict, containing observation from the view of this agent.
    :return:
    """
    playable = []
    for card in observation['card_knowledge'][0]:
        playable.append((CardPlayable(card, observation['fireworks'])))

    if True not in playable:
        return None

    elif playable.count(True) == 1:
        safe_card_idx = playable.index(True)
        return {'action_type': 'PLAY', 'card_index': safe_card_idx}

    else:
        indices = [playable.index(i) for i in playable if i is True]
        safe_card_idx = random.choice(indices)
        return {'action_type': 'PLAY', 'card_index': safe_card_idx}

def OsawaDiscard(observation):
    """
    Discards a card if it cannot be played at the end of the turn. This will discard cards that we know enough
    about to disqualify them from being playable. For example, a card with an unknown suit but a rank of 1 will not
    be playable if all the stacks have been started. This rule also considers cards that can not be played because
    their pre-requisite cards have already been discarded.
    :return:
    """
    unplayable = []
    for card in observation['card_knowledge'][0]:
        unplayable.append((CardUnplayable(card, observation['fireworks'])))

    if True not in unplayable:
        return None

    elif unplayable.count(True) == 1:
        card_idx = unplayable.index(True)
        return {'action_type': 'DISCARD', 'card_index': card_idx}

    else:
        indices = [unplayable.index(i) for i in unplayable if i is True]
        card_idx = random.choice(indices)
        return {'action_type': 'DISCARD', 'card_index': card_idx}

def TellPlayableCard(observation):
    """
    Tells the next player a random fact about any playable card in their hand.
    :return:
    """
    if observation['information_tokens'] == 0:
        return None

    playable = []
    possible_actions = []
    for card in observation['observed_hands'][1]:
        playable.append(CardPlayable(card, observation['fireworks']))

    if True not in playable:
        return None

    elif playable.count(True) == 1:
        card_idx = playable.index(True)

    else:
        indices = [playable.index(i) for i in playable if i is True]
        card_idx = random.choice(indices)

    if observation['card_knowledge'][1][card_idx]['color'] is None:
        possible_actions.append({'action_type': 'REVEAL_COLOR', 'target_offset': 1, 'color': observation['observed_hands'][1][card_idx]['color']})
    if observation['card_knowledge'][1][card_idx]['rank'] is None:
        possible_actions.append({'action_type': 'REVEAL_RANK', 'target_offset': 1, 'rank': observation['observed_hands'][1][card_idx]['rank']})

    if possible_actions:
        return random.choice(possible_actions)

    else:
        return None

def TellRandomly(observation):
    """
    Tells the next player a random fact about any card in their hand.
    :return:
    """
    if observation['information_tokens'] == 0:
        return None

    possible_actions = []
    for i, knowledge in enumerate(observation['card_knowledge'][1]):
        if knowledge['color'] is None:
            possible_actions.append({'action_type': 'REVEAL_COLOR', 'target_offset': 1, 'color': observation['observed_hands'][1][i]['color']})
        if knowledge['rank'] is None:
            possible_actions.append({'action_type': 'REVEAL_RANK', 'target_offset': 1, 'rank': observation['observed_hands'][1][i]['rank']})

    if possible_actions:
        return random.choice(possible_actions)

    else:
        return None

def DiscardRandomly(observation):
    """
    Randomly discards a card from the hand.
    :return:
    """
    return {'action_type': 'DISCARD', 'card_index': random.randint(0,4)}