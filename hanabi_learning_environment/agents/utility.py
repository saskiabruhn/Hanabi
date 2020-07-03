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

def utility(intention, estimated_board, card):
    score = 0

    if intention == 'play':
        # in intention is play and card is playable, this results in one more card on the fireworks.
        # reward this.
        if CardPlayable(card, estimated_board['fireworks']):
            score += 10

        # if intention is play and card is not playable at the time
        else:
            # punish loosing a card from stack
            score -= 1

            # punish getting a bomb depending on the number of bombs
            if estimated_board['life_tokens'] == 3:
                score -= 1
            elif estimated_board['life_tokens'] == 2:
                score -= 3
            elif estimated_board['life_tokens'] == 1:
                score -= 25

            # if card would still have been relevant in the future, punish loosing it depending on
            # the remaining copies of this card in the deck
            if not CardUnplayable(card, estimated_board['fireworks']):
                if remaining_copies(card, estimated_board['discard_pile']) == 2:
                    score -= 1
                elif remaining_copies(card, estimated_board['discard_pile']) == 1:
                    score -= 2
                elif remaining_copies(card, estimated_board['discard_pile']) == 0:
                    score -= 5


    elif intention == 'discard':
        # punish loosing a card from stack
        score -= 1

        # reward ganing a hint token:
        score += 0.5

        # punish discarding a playable card
        if CardPlayable(card, estimated_board['fireworks']):
            score -= 5

        # if card is not playable right now but would have been relevant in the future, punish
        # discarding it depending on the number of remaining copies in the game
        elif not CardUnplayable(card, estimated_board['fireworks']):
            if remaining_copies(card, estimated_board['discard_pile']) == 2:
                score -= 1
            elif remaining_copies(card, estimated_board['discard_pile']) == 1:
                score -= 2
            elif remaining_copies(card, estimated_board['discard_pile']) == 0:
                score -= 5

        # do we want to reward this additionally? I think rewarding gaining a hint token should be
        # enough, so nothing happens here
        elif CardUnplayable(card, estimated_board['fireworks']):
            pass

    elif intention == 'keep':
        # keeping a playable card is punished, because it does not help the game
        if CardPlayable(card, estimated_board['fireworks']):
            score -= 2

        # if card is not playable right now but is relevant in the future of the game reward keeping
        # this card depending on the remaining copies in the game
        elif not CardUnplayable(card, estimated_board['fireworks']):
            if remaining_copies(card, estimated_board['discard_pile']) == 2:
                score += 1
            elif remaining_copies(card, estimated_board['discard_pile']) == 1:
                score += 2
            elif remaining_copies(card, estimated_board['discard_pile']) == 0:
                score += 5

        # punish keeping a useless card
        elif CardUnplayable(card, estimated_board['fireworks']):
            score -= 1

    return score





estimated_board = {'life_tokens': 3,
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
# remember, that rank 0 in cards means rank 1, so rank = 0 and fireworks = 0 means card is playable!
card = {'color': 'B', 'rank': 2}


print('play: ', utility('play', estimated_board, card))
print('discard: ', utility('discard', estimated_board, card))
print('keep', utility('keep', estimated_board, card))

