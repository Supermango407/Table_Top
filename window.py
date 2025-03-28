from __future__ import annotations
import pygame
from pygame import Vector2


class WindowSprite(object):
    """class to make the window a parrent for sprites."""
    def __init__(self, window:pygame.surface.Surface):
        self.window = window
        self.global_position = Vector2(0, 0)
    
    def get_width(self):
        return self.window.get_width()
    
    def get_height(self):
        return self.window.get_height()


class GameObject(object):
    """basic object with an update start and window"""
    instances:list[GameObject] = []
    window:pygame.Surface = None
    font:pygame.font.Font = None
    mouse_pos = Vector2(0, 0)

    # list of GameObjects that look for events.
    event_handlers:list[GameObject] = []

    @staticmethod
    def set_window(window) -> None:
        GameObject.window = window


    def __init__(self, check_events:bool=False):
        """
        `check_events`: if True will check events,
            eg: key_presses, mouse clicks ect.
        """

        if check_events:
            GameObject.event_handlers.append(self)
        GameObject.instances.append(self)

    def update(self) -> None:
        """called once per frame"""
        pass

    def check_event(self, event:pygame.event.Event):
        """called on event if `self` is an event_handler."""
        pass

    def destroy(self) -> None:
        """Deletes `self` and removes it from GameOjbect's instances."""
        if self in GameObject.instances:
            GameObject.instances.remove(self)
        
        if self in GameObject.event_handlers:
            GameObject.event_handlers.remove(self)
        
        del(self)


class Sprite(GameObject):
    """GameObjects that are drawn to the screen"""
    instances:list[Sprite] = []

    def __init__(self, position:Vector2=Vector2(0, 0), anchor:str='top_left', parrent:Sprite=None, hidden=False, check_events:bool=False):
        """
        `position`: the location of the sprite onscreen.
        `anchor`: where the board is placed on the screen eg:
            top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        `hidden`: if true, sprite will not be drawn to screen.
        `check_events`: if True will check events,
            eg: key_presses, mouse clicks ect.
        """
        self.hidden = hidden
        if not hasattr(self, 'components'):
            self.components = []

        self.children:list[Sprite] = []
        """the sprite who has this sprite as a parrent."""

        self.position:Vector2 = position
        self.anchor:str = anchor

        # needs a place holder value before setting it.
        self.global_position:Vector2 = Vector2(0, 0)

        if parrent == None:
            self.parrent = WindowSprite(self.window)
            self.set_position()
        else:
            self.parrent = parrent
            self.parrent.children.append(self)

        Sprite.instances.append(self)
        super().__init__(check_events=check_events)

    def draw(self) -> None:
        """draws sprite on `window`."""
        for child in self.children:
            child.draw()

    def move_to_top(self):
        """moves the above other sprites, so it gets drawn ontop."""
        Sprite.instances.remove(self)
        Sprite.instances.append(self)

    def set_position(self, position:Vector2=None, anchor:str=None) -> None:
        """sets the position of `self`, with relation to `anchor`."""
        if position != None:
            self.position = position

        if anchor != None:
            self.anchor = anchor
            
        # set `x` base on `self.anchor` and `self.offset`
        if 'left' in self.anchor:
            x = self.position.x
        elif 'right' in self.anchor:
            x = self.position.x+self.parrent.get_width()-self.get_width()
        else:
            x = self.position.x+self.parrent.get_width()//2-self.get_width()//2
            
        # set `y` base on `self.anchor`
        if 'top' in self.anchor:
            y = self.position.y
        elif 'bottom' in self.anchor:
            y = self.position.y+self.parrent.get_height()-self.get_height()
        else:
            y = self.position.y+self.parrent.get_height()//2-self.get_height()//2
        
        self.global_position = self.parrent.global_position+Vector2(x, y)

        for child in self.children:
            child.set_position()
        
    def get_width(self) -> int:
        """returns the width of sprite, in pixels."""
        return 0
        
    def get_height(self) -> int:
        """returns the height of sprite, in pixels."""
        return 0

    def add_child(self, child:Sprite):
        """appends child to self."""
        self.children.append(child)
        child.parrent = self

    def destroy(self):
         for child in self.children:
             child.destroy()
             
         if self in Sprite.instances:
            Sprite.instances.remove(self)
         super().destroy()


class Component(object):
    """the parrent class of objects added to Sprites to add specific funinatity."""
    
    def __init__(self, sprite:Sprite):
        """
        `sprite`: the sprite `self` is aplied to.
        """
        self.sprite = sprite


class Text(Sprite):
    """for displaying text to window"""

    def __init__(self, value:str, position:Vector2=Vector2(0, 0), anchor:str='top', parrent:Sprite=None, color:tuple[int, int, int]=(0, 0, 0)):
        """
        `value`: the text that will be on the screen
        `position`: the location of the sprite onscreen.
        `anchor`: where the board is placed on the screen eg:
            top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        `color`: the color of the text
        """
        self.value = value
        self.color = color
        
        self.text = GameObject.font.render(self.value, True, color)
        
        super().__init__(position=position, anchor=anchor, parrent=parrent)

    def get_width(self):
        return self.text.get_rect()[2]

    def get_height(self):
        return self.text.get_rect()[3]

    def set_text(self, value:str):
        """sets value of text"""
        self.value = value
        self.text = GameObject.font.render(self.value, True, self.color)
        
        # set position to realign after text width changes.
        self.set_position()

    def set_color(self, color:tuple[int, int, int]):
         """sets color of text"""
         self.color = color
         self.text = GameObject.font.render(self.value, True, self.color)

    def draw(self):
        """write text on screen."""
        rect = (
            self.global_position.x,
            self.global_position.y,
            self.get_width(),
            self.get_height(),
        )
        GameObject.window.blit(self.text, rect)

        super().draw()


class Button(Sprite):
    """class for button Widget."""

    def __init__(self, onclick:callable, text_value:str="", position:Vector2=Vector2(0, 0), anchor:str='top_left', text_color:tuple[int, int, int]=(0, 0, 0), bg_color:tuple[int, int, int]=(223, 223, 223), hover_bg_color:tuple[int, int, int]=(127, 127, 127), parrent:Sprite=None):
        """
        `onclick`: what to do when the button is clicked.
        `text_value`: the text of the button.
        `text_color`: the color of the text.
        `bg_color`: the color of the background, when mouse isn't over button.
        `hover_bg_color: the color of the background, when mouse is over button.
        `position`: the location of the sprite onscreen.
        `anchor`: where the board is placed on the screen eg:
            top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        """
        self.onclick = onclick
        self.text_value = text_value
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        
        super().__init__(position=position, anchor=anchor, parrent=parrent, check_events=True)
        
        self.text = Text(value=self.text_value, parrent=self, position=Vector2(0, 0), anchor='center', color=text_color)
        self.set_position()
        
    def get_width(self):
        try:
            return self.text.get_width()
        except AttributeError:
            return 0
    
    def get_height(self):
        try:
            return self.text.get_height()
        except AttributeError:
            return 0
        
    def draw(self):
        # draw background
        pygame.draw.rect(
            self.window,
            self.hover_bg_color if self.hovering() else self.bg_color,
            (
                self.global_position.x,
                self.global_position.y,
                self.get_width(),
                self.get_height()
            )
        )

        # draw text
        # self.text.draw()
        super().draw()
      
    def hovering(self) -> bool:
        """whethere the mouse is over button or not."""
        # the postion of the mouse relitive to the button
        reletive_mouse = self.mouse_pos-self.global_position

        return reletive_mouse.x >= 0 and reletive_mouse.x <= self.get_width() and reletive_mouse.y >= 0 and reletive_mouse.y <= self.get_height()

