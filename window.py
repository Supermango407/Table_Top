from __future__ import annotations
import pygame
from pygame import Vector2
# from collider import Collider


class GameObject(object):
    """basic object with an update start and window"""
    childeren:list[GameObject] = []
    window:pygame.Surface = None
    font:pygame.font.Font = None
    mouse_pos = Vector2(0, 0)

    # list of GameObjects that look for events.
    event_handlers:list[GameObject] = []

    def __init__(self, check_events:bool=False):
        """
        `check_events`: if True will check events,
            eg: key_presses, mouse clicks ect.
        """

        if check_events:
            GameObject.event_handlers.append(self)
        GameObject.childeren.append(self)

    def update(self) -> None:
        """called once per frame"""
        pass

    def check_event(self, event):
        """called on event if `self` is an event_handler."""
        pass

    def destroy(self) -> None:
        """Deletes `self` and removes it from GameOjbect's children."""
        if self in GameObject.childeren:
            GameObject.childeren.remove(self)
        
        if self in GameObject.event_handlers:
            GameObject.event_handlers.remove(self)
        
        del(self)


class Sprite(GameObject):
    """GameOjbects that are drawn to the screen"""
    childeren:list[Sprite] = []

    def __init__(self, position:Vector2, hidden=False, check_events:bool=False):
        """
        `position`: the location of the sprite onscreen.
        `hidden`: if true, sprite will not be drawn to screen.
        `check_events`: if True will check events,
            eg: key_presses, mouse clicks ect.
        """
        self.hidden = hidden
        self.position = position
        Sprite.childeren.append(self)

        super().__init__(check_events=check_events)

    def draw(self) -> None:
        """draws sprite on `window`."""
        pass

    def move_to_top(self):
        """moves the above other sprites, so it gets drawn ontop."""
        Sprite.childeren.remove(self)
        Sprite.childeren.append(self)

    def set_position(self, position:Vector2) -> None:
        """sets the position of `self`"""
        self.position = position
        
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
        self.text_rect = self.text.get_rect()
        self.set_anchor(self.get_anchor())

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

