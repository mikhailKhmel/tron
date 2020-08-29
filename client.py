import pygame
import random

from player import *


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.bot = Player()
        self.members = [self.player, self.bot]
        pygame.init()
        self.sc = pygame.display.set_mode((Config.h_window, Config.w_window))
        pygame.display.update()
        self.main_cycle()

    def restart(self):
        self.player = Player()
        self.bot = Player()
        self.members = [self.player, self.bot]
        self.sc.fill((0, 0, 0))

    def check_game_over(self):
        res = 0
        for member in self.members:
            future_head = [member.lightcycle['head'][0] + member.lightcycle['direction'][0],
                           member.lightcycle['head'][1] + member.lightcycle['direction'][1]]
            if future_head in member.lightcycle['tail'] or future_head[0] < 0 or future_head[0] > Config.h_window \
                    or future_head[1] < 0 or future_head[1] > Config.w_window:
                res += 1
                break
            else:
                for other_member in self.members:
                    if member is other_member:
                        continue
                    if future_head in other_member.lightcycle['tail']:
                        res += 1
        return True if res > 0 else False

    def bot_logic(self):
        def check_head(future_head):
            if future_head[0] < 2 or future_head[0] > Config.w_window - 2 or future_head[1] < 2 \
                    or future_head[1] > Config.h_window - 2 \
                    or future_head in self.player.lightcycle['tail'] \
                    or future_head in self.bot.lightcycle['tail']:
                return False
            else:
                return True

        def choose_direction():
            while True:
                new_direction = random.choice(directions).copy()
                if new_direction == self.bot.lightcycle['direction']:
                    continue
                future_head = [self.bot.lightcycle['head'][0] + new_direction[0],
                               self.bot.lightcycle['head'][1] + new_direction[1]]
                if check_head(future_head):
                    self.bot.lightcycle['direction'] = new_direction.copy()
                    break

        directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]
        future_bot_head = [self.bot.lightcycle['head'][0] + self.bot.lightcycle['direction'][0],
                           self.bot.lightcycle['head'][1] + self.bot.lightcycle['direction'][1]]
        if check_head(future_bot_head):
            if random.randint(0, 100) % random.randint(1000, 10000) == 0:
                choose_direction()
        else:
            choose_direction()

    def render(self):
        for member in self.members:
            pygame.draw.rect(self.sc, member.color,
                             (member.lightcycle['head'][0] - 2, member.lightcycle['head'][1] - 2, 5, 5))  # render head
            for tail in member.lightcycle['tail']:  # render tails
                pygame.draw.rect(self.sc, member.color,
                                 (tail[0], tail[1], 1, 1))

    def main_cycle(self):
        previous_key = self.player.lightcycle['direction']
        while True:
            self.sc.fill((0, 0, 0))
            self.clock.tick(Config.speed)
            self.render()
            if not self.check_game_over():
                for member in self.members:
                    member.lightcycle['tail'].append(member.lightcycle['head'])
                    member.lightcycle['head'] = [
                        member.lightcycle['head'][0] +
                        member.lightcycle['direction'][0],
                        member.lightcycle['head'][1] + member.lightcycle['direction'][1]]
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        exit()
                    elif i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_UP:
                            if previous_key == [0, 1]:
                                continue
                            self.player.lightcycle['direction'] = [0, -1]
                        elif i.key == pygame.K_DOWN:
                            if previous_key == [0, -1]:
                                continue
                            self.player.lightcycle['direction'] = [0, 1]
                        elif i.key == pygame.K_RIGHT:
                            if previous_key == [-1, 0]:
                                continue
                            self.player.lightcycle['direction'] = [1, 0]
                        elif i.key == pygame.K_LEFT:
                            if previous_key == [1, 0]:
                                continue
                            self.player.lightcycle['direction'] = [-1, 0]
                        previous_key = self.player.lightcycle['direction']
            else:
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        exit()
                    elif i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_SPACE:
                            self.restart()
            self.bot_logic()
            pygame.display.update()


game = Game()
