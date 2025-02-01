import pygame
from pygame import Vector2


class GameObject(object):
    """basic object with an update start and window"""
    childeren = []
    window:pygame.Surface = None
    font:pygame.font.Font = None

    def __init__(self):
        GameObject.childeren.append(self)

    def update(self) -> None:
        """called once per frame"""
        pass

    def destroy(self) -> None:
         """Deletes `self` and removes it from GameOjbect's children."""
         if self in GameObject.childeren:
            GameObject.childeren.remove(self)
         del(self)


class Sprite(GameObject):
    """GameOjbects that are drawn to the screen"""
    childeren = []

    def __init__(self, hidden=False):
        """
        `hidden`: if True it will not draw the object
        """
        self.hidden = hidden
        Sprite.childeren.append(self)
        super().__init__()
    
    def update(self):
        super().update()
        if not self.hidden:
            self.draw()

    def draw(self) -> None:
        pass

    def destroy(self):
         if self in Sprite.childeren:
            Sprite.childeren.remove(self)
         super().destroy()


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
        self.position = position
        
        self.text = GameObject.font.render(self.value, True, color)
        self.text_rect = self.text.get_rect()
        
        self.set_anchor(anchor)

    def set_text(self, value:str):
         """sets value of text"""
         self.value = value
         self.text = GameObject.font.render(self.value, True, self.color)

    def set_color(self, color:tuple[int, int, int]):
         """sets color of text"""
         self.color = color
         self.text = GameObject.font.render(self.value, True, self.color)

    def set_anchor(self, new_anchor:str):
        """sets the anchor of `self`"""
        self._anchor = new_anchor

        if 'top' in new_anchor:
                self.text_rect.top = self.position[1]
        elif 'bottom' in new_anchor:
                self.text_rect.bottom = self.position[1]
        else:
             self.text_rect.centery = self.position[1]
        
        if 'left' in new_anchor:
                self.text_rect.left = self.position[0]
        elif 'right' in new_anchor:
                self.text_rect.right = self.position[0]
        else:
             self.text_rect.centerx = self.position[0]

    def get_anchor(self):
        """returns value of `anchor`"""
        return self._anchor

    def draw(self):
        """write text on screen."""
        GameObject.window.blit(self.text, self.text_rect)

