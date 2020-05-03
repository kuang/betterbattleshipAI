import random


BOARD_SIZE = 10

coords = []
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        coords.append([i, j])
random.shuffle(coords)



def next_move(response):
    return coords.pop()
