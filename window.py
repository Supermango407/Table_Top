import pygame
from pygame import Vector2


class GameObject(object):
    """basic object with an update start and window"""
    childeren = []
    window:pygame.Surface = None
    font:pygame.font.Font = None

    def __init__(self):
        GameObject.childeren.append(self)

    def start(self) -> None:
        "called when game starts"
        pass

    def update(self) -> None:
        """called once per frame"""
        pass


class Sprite(GameObject):
    """GameOjbects that are drawn to the screen"""
    childeren = []

    def __init__(self):
        Sprite.childeren.append(self)
        super().__init__()
    
    def update(self):
        super().update()
        self.draw()

    def draw(self) -> None:
        pass


class Text(object):
    """for displaying text to window"""

    def __init__(self, value:str, color:tuple[int, int, int]=(0, 0, 0), anchor:str="top left", position:Vector2=Vector2(0, 0)):
        """
        `value`: the text that will be on the screen
        `color`: the color of the text
        `anchor`: the anchor of the text_rect
            eg: top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `position`: the position of the text_rect
        """
        self.value = value
        self.color = color
        
        self.text = GameObject.font.render(self.value, True, color)
        self.text_rect = self.text.get_rect()

        # set anchor
        if 'top' in anchor:
            if 'left' in anchor:
                self.text_rect.topleft = position
            elif 'right' in anchor:
                self.text_rect.topright = position
            else:
                self.text_rect.top = position[1]
                self.text_rect.centerx = position[0]
        elif 'bottom' in anchor:
            if 'left' in anchor:
                self.text_rect.bottomleft = position
            elif 'right' in anchor:
                self.text_rect.bottomright = position
            else:
                self.text_rect.bottom = position[1]
                self.text_rect.centerx = position[0]
        elif 'left' in anchor:
                self.text_rect.left = position[0]
                self.text_rect.centery = position[1]
        elif 'right' in anchor:
                self.text_rect.right = position[0]
                self.text_rect.centery = position[1]
        else:
            self.text_rect.center = position

            

    def draw(self):
        """write text on screen."""
        GameObject.window.blit(self.text, self.text_rect)
