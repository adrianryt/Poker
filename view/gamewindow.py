import pygame
import os
import math
from pygame_widgets import Slider, TextBox
import threading
from view.button import ActionButton
from view.statswindow import StatsWindow

lock = threading.Lock()


class GameWindow:
    pygame.init()
    cardDict = {0: 'card_back.png', 8: '2_of_spades.png', 9: '2_of_clubs.png', 10: '2_of_diamonds.png',
                11: '2_of_hearts.png',
                12: '3_of_spades.png', 13: '3_of_clubs.png', 14: '3_of_diamonds.png', 15: '3_of_hearts.png',
                16: '4_of_spades.png', 17: '4_of_clubs.png', 18: '4_of_diamonds.png', 19: '4_of_hearts.png',
                20: '5_of_spades.png', 21: '5_of_clubs.png', 22: '5_of_diamonds.png', 23: '5_of_hearts.png',
                24: '6_of_spades.png', 25: '6_of_clubs.png', 26: '6_of_diamonds.png', 27: '6_of_hearts.png',
                28: '7_of_spades.png', 29: '7_of_clubs.png', 30: '7_of_diamonds.png', 31: '7_of_hearts.png',
                32: '8_of_spades.png', 33: '8_of_clubs.png', 34: '8_of_diamonds.png', 35: '8_of_hearts.png',
                36: '9_of_spades.png', 37: '9_of_clubs.png', 38: '9_of_diamonds.png', 39: '9_of_hearts.png',
                40: '10_of_spades.png', 41: '10_of_clubs.png', 42: '10_of_diamonds.png', 43: '10_of_hearts.png',
                44: 'jack_of_spades.png', 45: 'jack_of_clubs.png', 46: 'jack_of_diamonds.png', 47: 'jack_of_hearts.png',
                48: 'queen_of_spades.png', 49: 'queen_of_clubs.png', 50: 'queen_of_diamonds.png',
                51: 'queen_of_hearts.png',
                52: 'king_of_spades.png', 53: 'king_of_clubs.png', 54: 'king_of_diamonds.png', 55: 'king_of_hearts.png',
                56: 'ace_of_spades.png', 57: 'ace_of_clubs.png', 58: 'ace_of_diamonds.png', 59: 'ace_of_hearts.png',
                }
    WIDTH = 1200
    HEIGHT = 800
    FPS = 60
    BACKGROUND = (241, 245, 215)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    BLACK = (0, 0, 0)
    TABLE_RADIUS = 250
    Y_CONF = 80
    BORDER = pygame.Rect(WIDTH / 3 * 2, 0, 2, HEIGHT)
    CLIENT_FONT = pygame.font.Font(None, 50)
    OPPONENTS_FONT = pygame.font.Font(None, 32)

    def __init__(self, client):
        self.client = client
        self.player = None
        self.opponents = {}
        self.table_cards = []
        self.game_info = None
        self.pool = 0
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # wszystkie przyciski
        self.call_btn = ActionButton(self.window, 100, 665 + self.Y_CONF, 'Call', self)
        self.fold_btn = ActionButton(self.window, 400, 665 + self.Y_CONF, 'Fold', self)
        self.check_btn = ActionButton(self.window, 300, 665 + self.Y_CONF, 'Check', self)
        self.all_in_btn = ActionButton(self.window, 200, 665 + self.Y_CONF, 'AllIn', self)
        self.raise_btn = ActionButton(self.window, 500, 665 + self.Y_CONF, "Raise", self)
        self.slider = Slider(self.window, 600, 600 + self.Y_CONF, 150, 30, min=0, max=99, step=10)
        self.raise_text_box = TextBox(self.window, 600, 665 + self.Y_CONF, 100, 50, fontSize=30)
        self.stat_window = StatsWindow()

        pygame.display.set_caption("PokerGame!")

    def update_opponent(self, limited_player):
        self.opponents[limited_player.id] = limited_player

    def transform_img(self, img, a, b):
        img = pygame.transform.scale(img, (a, b))
        return img

    def wrap_angle(self, n):
        res = n % 180
        if res > 90:
            return 180 - res
        return res

    def calculate_position_for_opponent(self, angle, radius):
        alpha = self.wrap_angle(angle)
        t_x = self.WIDTH / 3
        t_y = self.HEIGHT / 2 + self.Y_CONF
        x = 1
        y = 1
        if angle <= 90:
            x = t_x - radius * math.sin(math.radians(alpha))
            y = t_y + radius * math.cos(math.radians(alpha))
        elif 90 < angle <= 180:
            x = t_x - radius * math.sin(math.radians(alpha))
            y = t_y - radius * math.cos(math.radians(alpha))
        elif 180 < angle <= 270:
            x = t_x + radius * math.sin(math.radians(alpha))
            y = t_y - radius * math.cos(math.radians(alpha))
        elif 270 < angle <= 360:
            x = t_x + radius * math.sin(math.radians(alpha))
            y = t_y + radius * math.cos(math.radians(alpha))
        return x, y

    def draw_card(self,X,Y,card_in_int):
        card1 = pygame.image.load(
            os.path.join('../Assets/cards', card_in_int))
        card1 = self.transform_img(card1, 70, 105)
        self.window.blit(card1, (X, Y))

    def draw_window(self):
        self.window.fill(self.BACKGROUND)
        pygame.draw.circle(self.window, (0, 255, 0), (self.WIDTH / 3, self.HEIGHT / 2 + self.Y_CONF), self.TABLE_RADIUS)
        # player_drawing
        if self.player is not None:
            self.slider.__setattr__("min", self.game_info.big_blind)
            if self.player.tokens - (
                    self.game_info.biggest_bet - self.player.tokens_in_pool) == self.game_info.big_blind:
                self.slider.__setattr__("max", self.game_info.big_blind + 1)
            else:
                self.slider.__setattr__("max",
                                        self.player.tokens - (self.game_info.biggest_bet - self.player.tokens_in_pool))
            self.draw_card(self.WIDTH / 3 - 70,self.HEIGHT - 240 + self.Y_CONF,self.cardDict.get(self.player.cards[0].get_card_in_int()) )
            self.draw_card(self.WIDTH / 3,self.HEIGHT - 240 + self.Y_CONF,self.cardDict.get(self.player.cards[1].get_card_in_int()) )
            tokens_surface = self.CLIENT_FONT.render(str(self.player.tokens), True, (0, 0, 0))
            self.window.blit(tokens_surface, (620, 650))
            tokens_pool_surface = self.OPPONENTS_FONT.render(str(self.player.tokens_in_pool), True, (0, 0, 0))
            self.window.blit(tokens_pool_surface, (self.WIDTH / 3, self.HEIGHT - 275 + self.Y_CONF))
        #start_oponnents_drawing
        if len(self.opponents) != 0:
            no_opponents = len(self.opponents)
            angle = 360 / (no_opponents + 1)
            lock.acquire()
            i = 1
            for key, val in self.opponents.items():
                X, Y = self.calculate_position_for_opponent(angle * i, self.TABLE_RADIUS + 30)
                pygame.draw.circle(self.window, (128, 119, 119), (X, Y), 50)
                id_surface = self.OPPONENTS_FONT.render(str(val.name), True, self.BLACK)
                tokens_surface = self.OPPONENTS_FONT.render(str(val.tokens), True, self.BLACK)
                tokens_pool_surface = self.OPPONENTS_FONT.render(str(val.tokens_in_pool), True, self.BLACK)
                self.window.blit(id_surface, (X, Y))
                self.window.blit((tokens_surface),
                                 (self.calculate_position_for_opponent(angle * i, self.TABLE_RADIUS + 70)))
                self.window.blit((tokens_pool_surface),
                                 (self.calculate_position_for_opponent(angle * i, self.TABLE_RADIUS - 40)))
                
                if hasattr(val, "cards"):
                    self.draw_card(X - 70,Y - 170,self.cardDict.get(val.cards[0].get_card_in_int()))
                    self.draw_card(X, Y - 170, self.cardDict.get(val.cards[1].get_card_in_int()))
                else:
                    self.draw_card(X - 70, Y - 170, self.cardDict.get(0))
                    self.draw_card(X, Y - 170, self.cardDict.get(0))
                i += 1
            lock.release()
            #end_oponnents_drawing
        # table_cards_drawing
        lock.acquire()
        x_offset = 0
        for card in self.table_cards:
            self.draw_card(self.WIDTH / 3 - 175 + x_offset, self.HEIGHT / 2,self.cardDict.get(card.get_card_in_int()))
            x_offset += 70
        pool_surface = self.CLIENT_FONT.render(str(self.pool), True, (0, 0, 0))
        lock.release()
        self.window.blit(pool_surface, (0, 0))
        pygame.draw.rect(self.window, self.BLACK, self.BORDER)

    def enable_buttons(self):
        # te przyciski zawze mozna wcisnac
        self.fold_btn.enable_btn()
        self.all_in_btn.enable_btn()
        lock.acquire()
        max_bet = self.game_info.biggest_bet
        lock.release()
        if max_bet == self.player.tokens_in_pool:
            self.check_btn.enable_btn()
        if max_bet > self.player.tokens_in_pool and self.game_info.biggest_bet - self.player.tokens_in_pool < self.player.tokens:
            self.call_btn.enable_btn()
        if max_bet < self.player.tokens:
            self.raise_btn.enable_btn()

    # wyłączenie wszystkich przycisków
    def disable_buttons(self):
        self.check_btn.disable_btn()
        self.call_btn.disable_btn()
        self.fold_btn.disable_btn()
        self.all_in_btn.disable_btn()
        self.raise_btn.disable_btn()

    def draw_buttons(self, events):
        self.call_btn.listen(events)
        self.call_btn.draw()
        self.fold_btn.listen(events)
        self.fold_btn.draw()
        self.check_btn.listen(events)
        self.check_btn.draw()
        self.all_in_btn.listen(events)
        self.all_in_btn.draw()
        self.raise_btn.listen(events)
        self.raise_btn.draw()
        self.slider.listen(events)
        self.slider.draw()
        self.raise_text_box.setText(self.slider.getValue())
        self.raise_text_box.draw()
        if self.raise_btn.enable:
            self.raise_btn.setOnClick(self.raise_btn.action, [self.slider.getValue()])

    def main(self):
        run = True
        while run:
            pygame.time.Clock().tick(self.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    # tutaj mamy obsluge rozlaczenia sie z serwerem
                    self.client.to_disconnect = True
                    if self.client.your_move and not self.client.game_end:
                        self.client.disconnect_at_move()
                    pygame.quit()
                    quit()
            # tu wybieram co ma zostac wyświetlone, gra czy widok końcowy
            if self.client.game_end:
                self.end()
            else:
                self.draw_window()
                self.stat_window.draw_history(self.window)
                self.draw_buttons(events)
            pygame.display.update()

    def end(self):
        self.window.fill(self.BACKGROUND)
        player_tokens_surface = self.OPPONENTS_FONT.render("You have: " + str(self.player.tokens) + "tokens",True,self.BLACK)
        self.window.blit(player_tokens_surface, (self.WIDTH / 3, self.HEIGHT/2 - 16))

    # widok logowania
    def login(self):
        width = 800
        height = 32
        base_font = pygame.font.Font(None, height)
        nick = ''
        msg = 'Enter your name and then press enter:'
        nick_input = pygame.Rect(self.WIDTH / 2 - width / 2, self.HEIGHT / 2 - height / 2, width, height)
        run = True
        while run:
            pygame.time.Clock().tick(self.FPS)
            self.window.fill(self.BACKGROUND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        nick = nick[0:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(nick) != 0:
                            # zwracam nick jaki wpisał gracz
                            return nick
                    else:
                        nick += event.unicode

            pygame.draw.rect(self.window, self.WHITE, nick_input)
            nick_surface = base_font.render(nick, True, self.BLACK)
            self.window.blit(nick_surface, (nick_input.x, nick_input.y + 5))
            msg_surface = base_font.render(msg, True, self.BLACK)
            self.window.blit(msg_surface, (nick_input.x, nick_input.y - height))
            pygame.display.update()

    # wykonuje sie w nieskonczonosc, az do momentu przyslania przez serwer dicta z przeciwnikami.
    def wait_for_players(self):
        run = True
        msg = "WAITING FOR PLAYERS"
        height = 50
        width = 500
        msg_input = pygame.Rect(self.WIDTH / 3, self.HEIGHT / 2, width, height)
        while run:
            pygame.time.Clock().tick(self.FPS)
            self.window.fill(self.BACKGROUND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.client.to_disconnect = True
                    if self.client.your_move and not self.client.game_end:
                        self.client.disconnect_at_move()
                    pygame.quit()
                    quit()

            msg_surface = self.CLIENT_FONT.render(msg, True, self.BLACK)
            self.window.blit(msg_surface, (msg_input.x, msg_input.y - height))
            if len(self.opponents) != 0:
                return
            pygame.display.update()

if __name__ == "__main__":
    game_window = GameWindow(None)
    game_window.login()
    game_window.main()