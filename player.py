from random import randint, choice

from config import Config


class Player(object):

    def __init__(self):
        self.lightcycle = {
            'head': [randint(20, Config.w_window - 50), randint(20, Config.w_window - 50)],
            'tail': [],
            'direction': choice([[0, -1], [0, 1], [1, 0], [-1, 0]])
        }
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        # [X,Y]: [0,-1] UP; [0,1] DOWN; [1,0] RIGHT; [-1,0] LEFT
