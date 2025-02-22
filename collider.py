from __future__ import annotations
from typing import Union
from collections.abc import Callable
import pygame
from pygame import Vector2
from window import GameObject, Sprite


class Collider(Sprite):
    """a sprite than can see if mouse is over it and detected other collisions."""

    def __init__(self, position:Vector2, onclick:Callable=None, hidden:bool=True, parrent:Sprite=None):
        """
        `position`: the location of the sprite onscreen.
        `onclick`: funtion to be called when clicked.
        `hidden`: if true, sprite will not be drawn to screen.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        """
        super().__init__(position=position, hidden=hidden, check_events=True, parrent=parrent)
        self.onclick = onclick
        self.is_mouse_over = self.collides_at(self.mouse_pos)

    def set_position(self, position=None, anchor=None):
        super().set_position(position, anchor)

        # make sure `is_mouse_set` is still correct.
        self.is_mouse_over = self.collides_at(self.mouse_pos)

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_mouse_over = self.collides_at(self.mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.onclick != None and self.is_mouse_over:
                self.onclick()

    def collides_at(self, position:Vector2) -> bool:
        """whether the collider covers point `position`"""
        return False


class CircleCollider(Collider):
    """a circular collider."""
    
    def __init__(self, position:Vector2, radius:float, onclick:Callable=None, hidden:bool=True, parrent:Sprite=None):
        """
        `position`: the location of the sprite onscreen.
        `radius`: the radius of circle collider.
        `onclick`: funtion to be called when clicked.
        `hidden`: if true, sprite will not be drawn to screen.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        """
        self.radius = radius
        super().__init__(position=position, onclick=onclick, hidden=hidden, parrent=parrent)

    def draw(self):
        color = (255, 0, 0) if self.is_mouse_over else (0, 255, 0)
        # draw circle
        pygame.draw.circle(self.window, color, self.position, self.radius, 1)
        # draw vertical line
        pygame.draw.line(self.window, color, self.position+Vector2(0, self.radius), self.position+Vector2(0, -self.radius))
        # draw horizantal line
        pygame.draw.line(self.window, color, self.position+Vector2(self.radius, 0), self.position+Vector2(-self.radius, 0))

        super().draw()

    def collides_at(self, position:Vector2):
        if self.position != None:
            return self.position.distance_to(position) <= self.radius


class ClickableSprite(Sprite):
    
    def __init__(self, position, collider:Collider, show_collider:bool=False, hidden=False, parrent:Sprite=None, check_events=False):
        """
        `position`: the location of the sprite onscreen.
        `collider`: the collider of the sprite.
            the coliders position will be in relation
            to the sprite (eg: [0, 0] will be centered).
        `show_collider`: if true will display the collider.
        `hidden`: if true, sprite will not be drawn to screen.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        `check_events`: if True will check events,
            eg: key_presses, mouse clicks ect.
        """
        self.show_collider = show_collider
        self.collider = collider
        
        # how far away collider is from the position of the sprite
        self.collider_position = Vector2(*self.collider.position)

        # sets the collider to be realitive to sprite
        self.collider.position += position

        # disable collider drawing so it can be hanndled by the sprite
        self.collider.hidden = True
        
        super().__init__(position=position, hidden=hidden, parrent=parrent, check_events=check_events)

        # add collider to sprite
        self.add_child(self.collider)
        self.set_position()

    def set_position(self, position = None, anchor = None):
        Sprite.set_position(self, position, anchor)
        print(self.children)

    def draw(self):
        if self.show_collider:
            self.collider.draw()
        super().draw()

    def onclick(self):
        """called when sprite is clicked"""
        pass

    def destroy(self):
        self.collider.destroy()
        return super().destroy()


class DraggableSprite(ClickableSprite):
    sprite_dragging = None
    click_position:Vector2 = Vector2(0, 0)
    click_offset:Vector2 = Vector2(0, 0)

    def __init__(self, position:Vector2, collider:Collider, locked=False, show_collider=False, hidden=False, parrent:Sprite=None):
        """
        `position`: the location of the sprite onscreen.
        `collider`: the collider of the sprite.
        `locked`: if true, piece isn't draggable.
            the coliders position will be in relation
            to the sprite (eg: [0, 0] will be centered).
        `show_collider`: if true will display the collider
        `hidden`: if true, sprite will not be drawn to screen.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
            eg: key_presses, mouse clicks ect.
        """

        self.show_collider = show_collider
        self.locked = locked
        super().__init__(position=position, collider=collider, show_collider=show_collider, hidden=hidden, parrent=parrent, check_events=True)
        
        self.collider.onclick = self.onclick

    def update(self):
        super().update()
        if DraggableSprite.sprite_dragging == self:
            self.set_position(self.mouse_pos+DraggableSprite.click_offset)

    def onclick(self):
        """called when clicked"""
        super().onclick()
        if not self.locked:
            self.move_to_top()
            DraggableSprite.click_position = self.mouse_pos
            DraggableSprite.click_offset = self.position - self.mouse_pos
            DraggableSprite.sprite_dragging = self

    def onlifted(self, sprite_start:Vector2, sprite_end:Vector2):
        """called when sprite is lifted.
            `sprite_start` where sprite started dragging
            `sprite_end`: where the sprite ended up.
        """
        self.click_position = Vector2(0, 0)
        self.click_offset = Vector2(0, 0)
        DraggableSprite.sprite_dragging = None

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if DraggableSprite.sprite_dragging == self:
                self.onlifted(DraggableSprite.click_offset+DraggableSprite.click_position, self.position)

