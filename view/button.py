import pygame
from pygame_widgets import Button

B_WIDTH = 100
B_HEIGHT = 50
B_FONT = 50
B_MARGIN = 20
B_INACTIVE_COLOR = (121, 226, 237)
B_HOVER_COLOR = (19, 52, 171)
B_PRESSED_COLOR = (237, 62, 62)
B_RADIUS = 20
B_DISABLE_COLOR = (122, 122, 120)

class ActionButton(Button) :
    def __init__(self, win, xPos, yPos, text, game_window):
        self.action_text = text.lower()
        self.game_window = game_window
        self.action = self.action_based_on_text(text)
        super().__init__(win, xPos, yPos, B_WIDTH, B_HEIGHT, text=text,
                         fontSize=B_FONT, margin=B_MARGIN,
                         inactiveColour=B_INACTIVE_COLOR,
                         hoverColour=B_HOVER_COLOR,
                         pressedColour=B_PRESSED_COLOR, radius=B_RADIUS,
                         onClick=self.action)

    def action_based_on_text(self, text):
        if text == "Raise":
            return self.raise_action
        else:
            return self.normal_action

    def normal_action(self):
        self.game_window.client.send(self.action_text)

    def raise_action(self):
        pass

    def disable_btn(self):
        self.setInactiveColour(B_DISABLE_COLOR)
        self.setHoverColour(B_DISABLE_COLOR)
        self.setPressedColour(B_DISABLE_COLOR)
        self.setOnClick(lambda : print("Btn disabled"))


    def enable_btn(self):
        self.setInactiveColour(B_INACTIVE_COLOR)
        self.setHoverColour(B_HOVER_COLOR)
        self.setPressedColour(B_PRESSED_COLOR)
        self.setOnClick(self.action)


