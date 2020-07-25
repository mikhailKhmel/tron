class Config:
    h_window = 500
    w_window = 500
    window = (h_window, w_window)
    speed = 20
    colors = [(255, 0, 0), (254, 133, 21), (47, 0, 247), (208, 126, 0)]


# import random
#
#
# def bot_logic(self):
#     def check_head(future_head):
#         if future_head[0] < 2 or future_head[0] > Config.w_window - 2 or future_head[1] < 2 \
#                 or future_head[1] > Config.h_window - 2 \
#                 or future_head in self.player.lightcycle['tail'] \
#                 or future_head in self.bot.lightcycle['tail']:
#             return False
#         else:
#             return True
#
#     def choose_direction():
#         while True:
#             new_direction = random.choice(directions).copy()
#             if new_direction == self.bot.lightcycle['direction']:
#                 continue
#             future_head = [self.bot.lightcycle['head'][0] + new_direction[0],
#                            self.bot.lightcycle['head'][1] + new_direction[1]]
#             if check_head(future_head):
#                 self.bot.lightcycle['direction'] = new_direction.copy()
#                 break
#
#     directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]
#     future_bot_head = [self.bot.lightcycle['head'][0] + self.bot.lightcycle['direction'][0],
#                        self.bot.lightcycle['head'][1] + self.bot.lightcycle['direction'][1]]
#     if check_head(future_bot_head):
#         if random.randint(0, 100) % random.randint(1000, 10000) == 0:
#             choose_direction()
#     else:
#         choose_direction()
