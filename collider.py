from __future__ import annotations
from typing import Union
from collections.abc import Callable
import pygame
from pygame import Vector2
from window import GameObject, Sprite, Component


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


class Draggable(Component):
    """a component that make sprites able to be clicked and dragged."""

    sprite_dragging = None
    click_position:Vector2 = Vector2(0, 0)
    click_offset:Vector2 = Vector2(0, 0)

    def __init__(self, sprite:Sprite, collider:Collider, locked:bool=False):
        """
        `sprite`: the sprite `self` is aplied to.
        `collider`: the collider of the sprite.
        `locked`: if true, piece isn't draggable.
            the coliders position will be in relation
            to the sprite (eg: [0, 0] will be centered).
        """

        self.locked = locked
        super().__init__(sprite)

    def update(self):
        super().update()
        if self.sprite_dragging == self:
            self.set_position(self.mouse_pos+self.click_offset)

    def onclick(self):
        """called when clicked"""
        super().onclick()
        if not self.locked:
            self.move_to_top()
            self.click_position = self.mouse_pos
            self.click_offset = self.position - self.mouse_pos
            self.sprite_dragging = self

    def onlifted(self, sprite_start:Vector2, sprite_end:Vector2):
        """called when sprite is lifted.
            `sprite_start` where sprite started dragging
            `sprite_end`: where the sprite ended up.
        """
        self.click_position = Vector2(0, 0)
        self.click_offset = Vector2(0, 0)
        self.sprite_dragging = None

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.sprite_dragging == self:
                self.onlifted(self.click_offset+self.click_position, self.position)

