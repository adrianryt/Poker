import pygame
pygame.init()

class StatsWindow:
    BLACK = (0, 0, 0)
    WIDTH = 1200
    HEIGHT = 800
    HISTORY_FONT = pygame.font.Font(None, 24)
    def __init__(self):
        pygame.init()
        self.history_surface = [self.HISTORY_FONT.render("Your game stat: ", True, self.BLACK)]

    def update_history(self,player, winners):
        curr_tokens = None
        for idx, winner in enumerate(winners):
            if winner.id == player.id:
                curr_tokens = winner.tokens

        if curr_tokens != None:
            tmp = "win - " + str(curr_tokens - (player.tokens_in_pool + player.tokens))
        else:
            tmp = "lose - " + str(player.tokens_in_pool)
        self.history_surface.append(self.HISTORY_FONT.render(tmp, True, self.BLACK))

    def draw_history(self,window):
        X = self.WIDTH / 3 * 2 + 20
        Y = 20
        N = len(self.history_surface)
        if Y + (N * 24) + (15 * N) >= self.HEIGHT:
            self.history_surface.pop(1)
        for line in range(N):  # v - fontsize
            window.blit(self.history_surface[line], (X, Y + (line * 24) + (15 * line)))