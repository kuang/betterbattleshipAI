import random
class NaiveAI:
    def __init__(self):
        # defaults
        self.last_shot = (0,0)
        self.seeking = False
        self.found = False
        self.shooting_direction = 0
        self.BOARD_SIZE = 10
        self.hit_board = [[' ' for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]

        # 1 = up, 2 = down, 3 = left, 4 = right
        self.SHIP_DIRECTIONS = [1, 2, 3, 4]

        self.coords = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.coords.append([i, j])
        random.shuffle(self.coords)


    def is_valid_shot(self, coord):
        x = coord[0]
        y = coord[1]
        if x<0 or x>9: return False
        if y<0 or y>9: return False
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
        
        # if there's a miss, but the ship is found but not sunk, retrace in other direction
        if response[0]==0 and self.shooting_direction!=0 and self.found == True:
            opposite_dir = self.get_opposite_direction(self.shooting_direction)
            next_coord = self.get_next_coord_in_direction(self.last_shot, opposite_dir)
            while not self.is_valid_shot(next_coord):
                next_coord = self.get_next_coord_in_direction(next_coord, opposite_dir)
            return next_coord

        # last shot wasn't a hit
        if response[0] == 0:
            # if seeking- try a different direction
            # if self.seeking:
                # print("seeking is on")
            # else:
                # print("seeking is off")
            if self.seeking == True and self.shooting_direction!=0:
                orig_coord = self.get_next_coord_in_direction(self.last_shot, self.get_opposite_direction(self.shooting_direction))
                # print("seeking coordinate: ")
                # print(orig_coord)
                rand_orthogonal_dir = self.get_rand_orthogonal_direction(self.shooting_direction)
                # print("rand chosen direction: " + str(rand_orthogonal_dir))
                coord_in_orthogonal_dir = self.get_next_coord_in_direction(orig_coord, rand_orthogonal_dir)
                # print(coord_in_orthogonal_dir)
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
                    # not very likely- both other orthogonal directions are invalid
                    else:
                        return self.pick_new_random_coord_and_reset_seeking()
            else:     
                return self.pick_new_random_coord_and_reset_seeking()
        # if last was a hit but there were no previous hits, pick a random direction
        if response[0] == 1 and self.shooting_direction==0 and self.seeking == False:
            # print("seeking on")
            random.shuffle(self.SHIP_DIRECTIONS)
            for direction in self.SHIP_DIRECTIONS:
                coord_in_dir = self.get_next_coord_in_direction(self.last_shot, direction)
                if self.is_valid_shot(coord_in_dir):
                    self.last_shot = coord_in_dir
                    self.shooting_direction = direction
                    self.seeking = True
                    return coord_in_dir
            return self.pick_new_random_coord_and_reset_seeking()
        
        # if last was a hit and didn't sink, keep shooting in that direction
        if response[0] == 1 and response[1] == 0 and self.shooting_direction!=0:
            coord_in_dir = self.get_next_coord_in_direction(self.last_shot, self.shooting_direction)
            #try shooting in same direction
            if self.is_valid_shot(coord_in_dir):
                self.seeking = False
                self.found = True
                self.last_shot = coord_in_dir
            # try opposite direction
            else:
                next_coord_in_opp_dir = self.get_next_coord_in_direction(self.last_shot, self.get_opposite_direction(self.shooting_direction))
                if self.is_valid_shot(next_coord_in_opp_dir):
                    self.last_shot = next_coord_in_opp_dir
                # if both original direction and opposite direction aren't valid (pretty rare): found a second ship! pick rand orthogonal direction and seek
                else:
                    random.shuffle(self.SHIP_DIRECTIONS)
                    for direction in self.SHIP_DIRECTIONS:
                        coord_in_dir = self.get_next_coord_in_direction(self.last_shot, direction)
                        if self.is_valid_shot(coord_in_dir):
                            self.last_shot = coord_in_dir
                            self.shooting_direction = direction
                            self.seeking = True
                            self.found = False
                            return coord_in_dir
                    return self.pick_new_random_coord_and_reset_seeking()
            return self.last_shot

        # ship was sunk: get new random shot, start over again
        if response[1] != 0:
            return self.pick_new_random_coord_and_reset_seeking()
            


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
        if direction<2:
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
        self.BOARD_SIZE = 10
        self.hit_board = [[' ' for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]

        # 1 = up, 2 = down, 3 = left, 4 = right
        self.SHIP_DIRECTIONS = [1, 2, 3, 4]

        self.coords = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.coords.append([i, j])
        random.shuffle(self.coords)
