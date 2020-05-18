import random
from engine import BOARD_SIZE

class NaiveAI:
    def __init__(self):
        # defaults
        self.last_shot = (0,0)
        self.seeking = False
        self.found = False
        self.shooting_direction = 0
        self.BOARD_SIZE = BOARD_SIZE
        self.hit_board = [[' ' for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]

        # 1 = up, 2 = down, 3 = left, 4 = right
        self.SHIP_DIRECTIONS = [1, 2, 3, 4]

        self.coords = [
            [0,4], [5,9], [9,5], [4,0], [0,6], [3,9], [9,3], [6,0], 
            [0,2], [7,9], [9,7], [2,0], [2,2], [7,7], [2,6], [3,7], 
            [7,3], [6,2], [2,4], [5,7], [7,5], [4,2], [4,4], [5,5], 
            [3,5], [4,6], [6,4], [5,3], [3,3], [6,6], [1,7], [2,8], 
            [8,2], [7,1], [1,3], [6,8], [8,6], [3,1], [1,5], [4,8], 
            [8,4], [5,1], [0,8], [1,9], [9,1], [8,0], [1,1], [8,8], 
            [0,0], [9,9]
        ]


    def is_valid_shot(self, coord):
        x = coord[0]
        y = coord[1]
        if x<0 or x>BOARD_SIZE-1: return False
        if y<0 or y>BOARD_SIZE-1: return False
        if self.hit_board[x][y] == "x":
            return False
        return True

    def next_move(self, response):
        # first move
        if response == None:
            self.last_shot = self.get_next_valid_random()
            self.shooting_direction = 0
            return self.last_shot  
        else:
            self.hit_board[self.last_shot[0]][self.last_shot[1]] = 'x'
        
        # miss
        if response[0] == 0:
            # had a previous hit, but still need to look for the rest of the ship
            if self.seeking == True:
                orig_coord = self.get_next_coord_in_direction(self.last_shot, self.get_opposite_direction(self.shooting_direction))
                # print("miss, but still seeking")
                # print("original coord: " + str(orig_coord))
                # print("last shooting direction: " + str(self.shooting_direction))
                rand_orthogonal_dir = self.get_rand_orthogonal_direction(self.shooting_direction)
                # print("next rand orthogonal direction: " + str(rand_orthogonal_dir))
                coord_in_orthogonal_dir = self.get_next_coord_in_direction(orig_coord, rand_orthogonal_dir)
                # print("next coord to try: "+ str(coord_in_orthogonal_dir))
                if self.is_valid_shot(coord_in_orthogonal_dir):
                    self.shooting_direction = rand_orthogonal_dir
                    self.last_shot = coord_in_orthogonal_dir
                    return coord_in_orthogonal_dir
                else:
                    other_rand_orthogonal_dir = self.get_opposite_direction(rand_orthogonal_dir)
                    coord_in_other_orthogonal_dir = self.get_next_coord_in_direction(orig_coord, other_rand_orthogonal_dir)
                    if self.is_valid_shot(coord_in_other_orthogonal_dir):
                        self.shooting_direction = other_rand_orthogonal_dir
                        self.last_shot = coord_in_other_orthogonal_dir
                        return coord_in_other_orthogonal_dir
                    else:
                        self.last_shot = self.pick_new_random_coord_and_reset_seeking()
                        return self.last_shot
            # if found but miss, try opposite direction
            if self.found == True:
                # print("RETRACE")
                opposite_dir = self.get_opposite_direction(self.shooting_direction)
                next_coord = self.get_next_coord_in_direction(self.last_shot, opposite_dir)
                self.shooting_direction = opposite_dir
                while not self.is_valid_shot(next_coord):
                    next_coord = self.get_next_coord_in_direction(next_coord, opposite_dir)
                    # print("while loop")
                    # print(next_coord)
                self.last_shot = next_coord
                return next_coord
            
            return self.pick_new_random_coord_and_reset_seeking()

        # hit
        else:
            # ship was sunk: get new random shot, start over again
            if response[1] != 0:
                self.found = False
                self.seeking = False
                return self.pick_new_random_coord_and_reset_seeking()

            # new ship found
            if self.seeking == False and self.found == False:
                self.seeking = True
                # print("SEEKING")
                random.shuffle(self.SHIP_DIRECTIONS)
                # print(self.SHIP_DIRECTIONS)
                for direction in self.SHIP_DIRECTIONS:
                    coord_in_dir = self.get_next_coord_in_direction(self.last_shot, direction)
                    # print(coord_in_dir)
                    # print("direction: " + str(direction))
                    if self.is_valid_shot(coord_in_dir):
                        self.last_shot = coord_in_dir
                        self.shooting_direction = direction
                        return coord_in_dir
            
            if self.seeking == True or self.found == True:
                coord_in_dir = self.get_next_coord_in_direction(self.last_shot, self.shooting_direction)
                self.seeking = False
                self.found = True
                # print("SHIP FOUND")

                # try next in same direction
                if self.is_valid_shot(coord_in_dir):
                    self.last_shot = coord_in_dir
                # if invalid- try opposite direction
                else:
                    opposite_dir = self.get_opposite_direction(self.shooting_direction)
                    next_coord = self.get_next_coord_in_direction(self.last_shot, opposite_dir)
                    self.shooting_direction = opposite_dir
                    while not self.is_valid_shot(next_coord):
                        next_coord = self.get_next_coord_in_direction(next_coord, opposite_dir)
                    self.last_shot = next_coord            
                return self.last_shot

    def pick_new_random_coord_and_reset_seeking(self):
        self.shooting_direction = 0
        shot = self.get_next_valid_random()
        self.last_shot = shot
        self.seeking = False
        self.found = False
        return shot

    def get_opposite_direction(self, direction):
        # 2 or 4
        if direction%2 == 0:
            return direction - 1
        return direction + 1

    def get_rand_orthogonal_direction(self, direction):
        # if 1 or 2: return rand 3 or 4 
        if direction<=2:
            return random.choice([3,4])
        return random.choice([1,2])


    def get_next_coord_in_direction(self, coord, direction):
        x = coord[0]
        y = coord[1]
        # up
        if direction == 1:
            return (x-1, y)
        # down
        if direction == 2:
            return (x+1, y)
        # left
        if direction == 3:
            return (x, y-1)
        #right
        if direction == 4:
            return (x, y+1)

    def get_next_valid_random(self):
        next = self.coords.pop()
        while self.hit_board[next[0]][next[1]] == 'x':
            next = self.coords.pop()
        return next

    def restart(self):
        # defaults
        self.last_shot = (0,0)
        self.seeking = False
        self.found = False
        self.shooting_direction = 0
        self.BOARD_SIZE = BOARD_SIZE
        self.hit_board = [[' ' for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]

        # 1 = up, 2 = down, 3 = left, 4 = right
        self.SHIP_DIRECTIONS = [1, 2, 3, 4]

        self.coords = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.coords.append([i, j])
        random.shuffle(self.coords)
