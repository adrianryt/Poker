import pygame
import os
from view.button import button
import sys
from io import StringIO
import math
from pygame_widgets import Slider


cardDict = {None: 'red_joker.png', 8:'2_of_spades.png',9: '2_of_clubs.png',10: '2_of_diamonds.png',11:'2_of_hearts.png',
            12: '3_of_spades.png', 13: '3_of_clubs.png', 14: '3_of_diamonds.png', 15: '3_of_hearts.png',
            16: '4_of_spades.png', 17: '4_of_clubs.png', 18: '4_of_diamonds.png', 19: '4_of_hearts.png',
            20: '5_of_spades.png', 21: '5_of_clubs.png', 22: '5_of_diamonds.png', 23: '5_of_hearts.png',
            24: '6_of_spades.png', 25: '6_of_clubs.png', 26: '6_of_diamonds.png', 27: '6_of_hearts.png',
            28: '7_of_spades.png', 29: '7_of_clubs.png', 30: '7_of_diamonds.png', 31: '7_of_hearts.png',
            32: '8_of_spades.png', 33: '8_of_clubs.png', 34: '8_of_diamonds.png', 35: '8_of_hearts.png',
            36: '9_of_spades.png', 37: '9_of_clubs.png', 38: '9_of_diamonds.png', 39: '9_of_hearts.png',
            40: '10_of_spades.png', 41: '10_of_clubs.png', 42: '10_of_diamonds.png', 43: '10_of_hearts.png',
            44: 'jack_of_spades.png', 45: 'jack_of_clubs.png', 46: 'jack_of_diamonds.png', 47: 'jack_of_hearts.png',
            48: 'queen_of_spades.png', 49: 'queen_of_clubs.png', 50: 'queen_of_diamonds.png', 51: 'queen_of_hearts.png',
            52: 'king_of_spades.png', 53: 'king_of_clubs.png', 54: 'king_of_diamonds.png', 55: 'king_of_hearts.png',
            56: 'ace_of_spades.png', 57: 'ace_of_clubs.png', 58: 'ace_of_diamonds.png', 59: 'ace_of_hearts.png',
            }

class game_window:
    def __init__(self, client):
        self.client = client
        pygame.init()
        self.WIDTH = 1200
        self.HEIGHT = 800
        self.FPS = 60
        self.BACKGROUND = (241,245,215)
        self.WHITE = (255,255,255)
        self.GREY = (128,128,128)
        self.BLACK = (0,0,0)
        self.BORDER = pygame.Rect(self.WIDTH/3 * 2,0,2, self.HEIGHT)
        self.ACTION = None
        self.TABLE_RADIUS = 250
        self.Y_CONF = 80

        self.player = None
        self.opponents = None
        self.tableCards = None


        self.client_font = pygame.font.Font(None, 50)
        self.opponents_font = pygame.font.Font(None, 32)

        self.callButton = button(self.GREY,500,665 + self.Y_CONF,100,50,"Call!")
        self.foldButton = button(self.GREY,400,665 + self.Y_CONF,100,50,"Fold!")
        self.checkButton = button(self.GREY,300,665 + self.Y_CONF,100,50,"Check!")
        self.allInButton = button(self.GREY,200,665 + self.Y_CONF,100,50,"All In!")




        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("PokerGame!")

    #TODO chyba lepiej te buttony do tablicy wrzucic
    def enable_buttons(self):
        self.callButton.disabled = False
        self.foldButton.disabled = False
        self.checkButton.disabled = False
        self.allInButton.disabled = False
        self.callButton.color = self.WHITE
        self.foldButton.color = self.WHITE
        self.checkButton.color = self.WHITE
        self.allInButton.color = self.WHITE
        self.ACTION = None

    #TODO nie wiem co tu sie dzieje w tym kodzie, kiedy te przyciski sa tak naprawde wylaczane
    #naraazie tylko zmieniam ich kolor
    def disable_buttons(self):
        self.allInButton.disabled = True
        self.callButton.color = self.GREY
        self.foldButton.color = self.GREY
        self.checkButton.color = self.GREY
        self.allInButton.color = self.GREY

    def update_opponent(self,l_player):
        self.opponents.update({l_player.id:l_player})

    def transform_img(self, img, a,b):
        img = pygame.transform.scale(img, (a,b))
        return img

    def wrap_angle(self,n):
        res = n % 180
        if res > 90:
            return 180 - res
        return res

    def calculate_position_for_oponnent(self, angle, R):
        alpha = self.wrap_angle(angle)
        t_x = self.WIDTH/3
        t_y = self.HEIGHT/2 + self.Y_CONF
        x =1
        y = 1
        if angle <= 90:
            x = t_x - R*math.sin(math.radians(alpha))
            y = t_y + R*math.cos(math.radians(alpha))
        elif angle <= 180 and angle > 90:
            x = t_x - R*math.sin(math.radians(alpha))
            y = t_y - R*math.cos(math.radians(alpha))
        elif angle > 180 and angle <= 270:
            x = t_x + R*math.sin(math.radians(alpha))
            y = t_y - R*math.cos(math.radians(alpha))
        elif angle >270 and angle <= 360:
            x = t_x + R*math.sin(math.radians(alpha))
            y = t_y + R*math.cos(math.radians(alpha))
        return x,y

    def draw_window(self):
        self.window.fill(self.BACKGROUND)
        pygame.draw.circle(self.window, (0,255,0), (self.WIDTH/3, self.HEIGHT/2 + self.Y_CONF), self.TABLE_RADIUS)
        if self.player is not None:
            card1 = pygame.image.load(os.path.join('../Assets/cards', cardDict.get(self.player.cards[0].get_card_in_int())))
            card1 = self.transform_img(card1,70,105)
            self.window.blit(card1,(self.WIDTH/3 - 70, self.HEIGHT - 240 + self.Y_CONF))
            card2 = pygame.image.load(
                os.path.join('../Assets/cards', cardDict.get(self.player.cards[1].get_card_in_int())))
            card2 = self.transform_img(card2, 70, 105)
            self.window.blit(card2, (self.WIDTH/3, self.HEIGHT - 240 + self.Y_CONF))
            tokens_surface = self.client_font.render(str(self.player.tokens), True, (0, 0, 0))
            self.window.blit(tokens_surface, (620, 650))
            tokens_pool_surface = self.opponents_font.render(str(self.player.tokens_in_pool), True, (0,0,0))
            self.window.blit(tokens_pool_surface, (self.WIDTH/3, self.HEIGHT - 275 + self.Y_CONF))

        if self.opponents is not None:
            no_opponents = len(self.opponents)
            angle = 360 / (no_opponents + 1)
            #TODO przydaloby sie chyba innej struktury uzyc, bo ciagle sortowanie nie ma sensu, chyba ze wystarczy raz na samym poczatku dunno
            dict(sorted(self.opponents.items(), key=lambda item: item[1].id))
            i = 1
            for key, val in self.opponents.items():
                X,Y = self.calculate_position_for_oponnent(angle*i, self.TABLE_RADIUS+30)
                pygame.draw.circle(self.window,(128, 119, 119),(X,Y), 50)
                #TODO karty wygranych się nie pokazują po końcu rundy, slider na raisa
                #oponent_circle + tokens
                id_surface = self.opponents_font.render(str(val.name), True, self.BLACK)
                tokens_surface = self.opponents_font.render(str(val.tokens),True,self.BLACK)
                tokens_pool_surface = self.opponents_font.render(str(val.tokens_in_pool), True,self.BLACK)
                self.window.blit(id_surface, (X,Y))
                self.window.blit((tokens_surface),(self.calculate_position_for_oponnent(angle*i, self.TABLE_RADIUS+70)))
                self.window.blit((tokens_pool_surface),(self.calculate_position_for_oponnent(angle*i, self.TABLE_RADIUS-70)))
                #end of oponent_circle + tokens
                #start_oponnent cards
                card1 = None
                card2 = None
                if hasattr(val, "cards"):
                    card1 = pygame.image.load(os.path.join('../Assets/cards', cardDict.get(val.cards[0].get_card_in_int())))
                    card2 = pygame.image.load(os.path.join('../Assets/cards', cardDict.get(val.cards[1].get_card_in_int())))
                else:
                    card1 = pygame.image.load(os.path.join('../Assets/cards', 'card_back.png'))
                    card2 = pygame.image.load(os.path.join('../Assets/cards', 'card_back.png'))

                card1 = self.transform_img(card1, 70, 105)
                self.window.blit(card1, (X-70, Y - 170))
                card2 = self.transform_img(card2, 70, 105)
                self.window.blit(card2, (X,Y-170))
                #end_oponennt cards
                i+=1


        if self.tableCards is not None:
            x_offset = 0
            for card in self.tableCards:
                card = pygame.image.load(os.path.join('../Assets/cards', cardDict.get(card.get_card_in_int())))
                card = self.transform_img(card, 70, 105)
                self.window.blit(card, (self.WIDTH / 3 - 175 + x_offset, self.HEIGHT/2))
                x_offset += 70

        pygame.draw.rect(self.window, self.BLACK, self.BORDER)


        self.callButton.draw(self.window,self.BLACK)
        self.foldButton.draw(self.window, self.BLACK)
        self.callButton.draw(self.window, self.BLACK)
        self.checkButton.draw(self.window, self.BLACK)
        self.allInButton.draw(self.window, self.BLACK)

        pygame.time.Clock().tick(self.FPS)
        pygame.display.update()

    def callAction(self):
        self.callButton.disabled = True
        self.ACTION = "call"

    def foldAction(self):
        self.foldButton.disabled = True
        self.ACTION = "fold"

    def checkAction(self):
        self.checkButton.disabled = True
        self.ACTION = "check"

    def allInAction(self):
        self.allInButton.disabled = True
        self.ACTION = "allIn"

    def main(self):
        run = True
        while run:
            pygame.time.Clock().tick(self.FPS)
            events = pygame.event.get()
            for event in events:
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
                    #TODO tu obsluzyc jak sie chce rozlaczyc bedzie uciazliwe to chyba zeby game loopa nie popsuc
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.callButton.isOver(pos):
                        self.callAction()
                    if self.foldButton.isOver(pos):
                        self.foldAction()
                    if self.checkButton.isOver(pos):
                        self.checkAction()
                    if self.allInButton.isOver(pos):
                        self.allInAction()


            self.draw_window()

    def login(self):
        width = 800
        height = 32
        base_font = pygame.font.Font(None, height)
        nick = ''
        msg = 'Enter your name and then press enter:'
        nick_input = pygame.Rect(self.WIDTH/2 - width/2, self.HEIGHT/2 - height/2, width, height)
        box_color = (255,255,255)
        run = True
        while run:
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
                            return nick
                    else:
                        nick += event.unicode


            pygame.draw.rect(self.window, box_color, nick_input)
            nick_surface = base_font.render(nick, True, self.BLACK)
            self.window.blit(nick_surface, (nick_input.x, nick_input.y + 5))

            msg_surface = base_font.render(msg, True, self.BLACK)
            self.window.blit(msg_surface, (nick_input.x, nick_input.y - height))

            pygame.time.Clock().tick(self.FPS)
            pygame.display.update()

    def wait_for_players(self):

        run = True
        msg = "WAITING FOR PLAYERS"
        height = 50
        width = 500
        msg_input = pygame.Rect(self.WIDTH / 2, self.HEIGHT / 2 , width, height)
        while run:
            self.window.fill(self.BACKGROUND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            msg_surface = self.client_font.render(msg, True, self.BLACK)
            self.window.blit(msg_surface, (msg_input.x, msg_input.y - height))
            if (self.opponents != None):
                return
            pygame.time.Clock().tick(self.FPS)
            pygame.display.update()


if __name__ == "__main__":
    game_window = game_window()
    game_window.login()
    game_window.main()