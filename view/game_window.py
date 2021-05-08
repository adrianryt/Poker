import pygame
import os
from view.button import button
import sys
from io import StringIO
import math


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
    def __init__(self):
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.FPS = 5
        self.BACKGROUND = (241,245,215)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.BORDER = pygame.Rect(self.WIDTH/3 * 2,0,2, self.HEIGHT)
        self.ACTION = None

        self.player = None
        self.opponents = None
        self.tableCards = None

        self.callButton = button(self.WHITE,500,650,100,50,"Call!")
        self.foldButton = button(self.WHITE,400,650,100,50,"Fold!")
        self.checkButton = button(self.WHITE,300,650,100,50,"Check!")
        self.allInButton = button(self.WHITE,200,650,100,50,"All In!")


        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("PokerGame!")

    def reset_buttons(self):
        self.callButton.disabled = False
        self.callButton.disabled = False
        self.checkButton.disabled = False
        self.allInButton.disabled = False
        self.ACTION = None

    def update_opponent(self,l_player):
        self.opponents.update({l_player.id:l_player})

    def transform_img(self, img, a,b):
        img = pygame.transform.scale(img, (a,b))
        return img

    def draw_window(self):
        self.window.fill(self.BACKGROUND)
        pygame.draw.circle(self.window, (0,255,0), (self.WIDTH/3, self.HEIGHT/2), 250)
        if self.player is not None:
            card1 = pygame.image.load(os.path.join('../Assets/cards', cardDict.get(self.player.cards[0].get_card_in_int())))
            card1 = self.transform_img(card1,70,105)
            self.window.blit(card1,(self.WIDTH/3 - 70, self.HEIGHT - 155))
            card2 = pygame.image.load(
                os.path.join('../Assets/cards', cardDict.get(self.player.cards[1].get_card_in_int())))
            card2 = self.transform_img(card2, 70, 105)
            self.window.blit(card2, (self.WIDTH/3, self.HEIGHT - 155))

        if self.opponents is not None:
            for key, val in self.opponents.items():
                pass
                #print(val)
                #tutaj już iteruje po DICT'IE !! nie koniecznie posortowanym

        if self.tableCards is not None:
            x_offset = 0
            for card in self.tableCards:
                card = pygame.image.load(os.path.join('../Assets/cards', cardDict.get(card.get_card_in_int())))
                card = self.transform_img(card, 70, 105)
                self.window.blit(card, (self.WIDTH / 3 - 175 + x_offset, self.HEIGHT/2 - 105))
                x_offset += 70

        pygame.draw.rect(self.window, self.BLACK, self.BORDER)


        self.callButton.draw(self.window,self.BLACK)
        self.foldButton.draw(self.window, self.BLACK)
        self.callButton.draw(self.window, self.BLACK)
        self.checkButton.draw(self.window, self.BLACK)
        self.allInButton.draw(self.window, self.BLACK)

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
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
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


if __name__ == "__main__":
    game_window = game_window()
    game_window.main()