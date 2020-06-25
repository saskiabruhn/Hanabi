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
    if fireworks[card['color']] > int(card['rank']):
            return True
    else:
        return False

def remaining_copies(card, discard_pile):
    if card['rank'] == 1:
        total_copies = 3
    elif card['rank'] == 5:
        total_copies = 1
    else:
        total_copies = 2

    discarded_copies = discard_pile.count(str(card['color']) + str(card['rank']))

    return total_copies - discarded_copies

def utility(intention, estimated_board, card_identities, last_action):
    scores = {}
    for c in card_identities['color']:
        if card_identities['color'][c] != 0:
            for r in card_identities['rank']:
                if card_identities['rank'][r] != 0:
                    card = {'color': c, 'rank': r}
                    score = 0


                    if last_action['action_type'] == 'REVEAL_RANK' or last_action['action_type'] == 'REVEAL_COLOR':
                        # punish use of information token
                        if estimated_board['information_tokens'] in [7,6,5]:
                            score -= 0.2
                        if estimated_board['information_tokens'] in [4, 3]:
                            score -= 0.3
                        if estimated_board['information_tokens'] in [2,1]:
                            score -= 0.4
                        if estimated_board['information_tokens'] == 0:
                            score -= 0.5

                        if intention == 'play':
                            if CardPlayable(card, estimated_board['fireworks']):
                                score += 5
                            else:
                                if estimated_board['life_tokens'] == 3:
                                    score -= 1
                                elif estimated_board['life_tokens'] == 2:
                                    score -= 3
                                elif estimated_board['life_tokens'] == 1:
                                    score -= 25

                                if not CardUnplayable(card, estimated_board['fireworks']):
                                    if remaining_copies(card, estimated_board['discard_pile']) == 2:
                                        score -= 1
                                    elif remaining_copies(card, estimated_board['discard_pile']) == 1:
                                        score -= 2
                                    elif remaining_copies(card, estimated_board['discard_pile']) == 0:
                                        score -= 5


                        elif intention == 'discard':
                            # punishing discard actions after receiving a hint on this card in general
                            score -= 0.3

                            if CardPlayable(card, estimated_board['fireworks']):
                                score -= 5

                            elif not CardUnplayable(card, estimated_board['fireworks']):
                                if remaining_copies(card, estimated_board['discard_pile']) == 2:
                                    score -= 1
                                elif remaining_copies(card, estimated_board['discard_pile']) == 1:
                                    score -= 2
                                elif remaining_copies(card, estimated_board['discard_pile']) == 0:
                                    score -= 5

                            elif CardUnplayable(card, estimated_board['fireworks']):
                                pass

                        elif intention == 'keep':
                            if CardPlayable(card, estimated_board['fireworks']):
                                score -= 2

                            elif not CardUnplayable(card, estimated_board['fireworks']):
                                if remaining_copies(card, estimated_board['discard_pile']) == 2:
                                    score += 1
                                elif remaining_copies(card, estimated_board['discard_pile']) == 1:
                                    score += 2
                                elif remaining_copies(card, estimated_board['discard_pile']) == 0:
                                    score += 5

                            elif CardUnplayable(card, estimated_board['fireworks']):
                                pass
                    scores[str(c) + str(r)] = score


    return scores




estimated_board = {'life_tokens': 1,
                   'information_tokens': 7,
                   'fireworks': {'R': 3, 'Y': 2, 'G': 4, 'W': 1, 'B': 2},
                   'discard_pile': ['B2', 'B3', 'B2'],
                   'estimated_hands': [
                       [{'color': None, 'rank': -1},
                        {'color': None, 'rank': 0},
                        {'color': None, 'rank': -1},
                        {'color': None, 'rank': -1},
                        {'color': None, 'rank': -1}],
                       [{'color': 'B', 'rank': 2},
                        {'color': 'R', 'rank': 0},
                        {'color': 'Y', 'rank': 4},
                        {'color': 'B', 'rank': 3},
                        {'color': 'Y', 'rank': 0}]
                    ]
                   }

last_action = {'action_type': 'REVEAL_COLOR', 'target_offset': 1, 'color': 'B'}
intention = 'play'
card_identities = {'color': {'B': 1, 'R': 0, 'G': 0, 'Y': 0, 'W': 0},
                   'rank': {'1': 1/5, '2': 1/5, '3': 1/5, '4': 1/5, '5': 1/5}}

print(utility(intention, estimated_board, card_identities, last_action))


