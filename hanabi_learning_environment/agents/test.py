mental_state = []
unplayed_cards = [[3, 3, 3, 3, 3],
                  [2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2],
                  [1, 1, 1, 1, 1]]

    # initial mental state RGBWY, 12345
    # mental_state[card][rank][color]
color_encoding = {'R': 0, 'G': 1, 'B': 2, 'W': 3, 'Y': 4}
for i in range(5):
  mental_state.append([[3, 3, 3, 3, 3],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [1, 1, 1, 1, 1]])


for i in range(5):
  mental_state[0][i][1] = 0

print(mental_state)