from __future__ import annotations
from typing import Union
from collections.abc import Callable
import pygame
from pygame import Vector2
from window import GameObject, Sprite, Component


class Collider(Sprite):
    """a sprite than can see if mouse is over it and detected other collisions."""
    
    collider_dragging = None
    drag_start_position:Vector2 = Vector2(0, 0)
    drag_click_offset:Vector2 = Vector2(0, 0)

    def __init__(self, position:Vector2, onclick:Callable=None, hidden:bool=True, draggable:bool=False, on_release:callable=None, parrent:Sprite=None):
        """
        `position`: the location of the sprite onscreen.
        `onclick`: funtion to be called when clicked.
        `hidden`: if true, sprite will not be drawn to screen.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        """
        super().__init__(local_position=position, hidden=hidden, check_events=True, parrent=parrent)
        self.onclick = onclick
        self.draggable = draggable
        self.on_release = on_release
        self.mouse_over = self.collides_at(self.mouse_pos)

    def update(self):
        super().update()
        if self.draggable:
            if self.collider_dragging == self:
                self.parrent.set_position(self.mouse_pos+self.click_offset)

    def set_position(self, position=None, anchor=None):
        super().set_position(position, anchor)

        # make sure `is_mouse_set` is still correct.
        self.mouse_over = self.collides_at(self.mouse_pos)

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_over = self.collides_at(self.mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.onclick != None and self.mouse_over:
                self.onclick()
            if self.draggable and self.mouse_over:
                self.parrent.move_to_top()
                self.click_position = self.mouse_pos
                self.click_offset = self.parrent.local_position - self.mouse_pos
                self.collider_dragging = self
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.collider_dragging != None and self.collider_dragging == self:
                if self.on_release != None:
                    self.on_release()
                self.click_position = Vector2(0, 0)
                self.click_offset = Vector2(0, 0)
                self.collider_dragging = None

    def collides_at(self, global_position:Vector2) -> bool:
        """whether the collider covers point `position`"""
        return False


class CircleCollider(Collider):
    """a circular collider."""
    
    def __init__(self, position:Vector2, radius:float, onclick:Callable=None, hidden:bool=True, draggable=False, parrent:Sprite=None):
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
        super().__init__(position=position, onclick=onclick, hidden=hidden, draggable=draggable, parrent=parrent)

    def draw(self):
        color = (255, 0, 0) if self.mouse_over else (0, 255, 0)
        # draw circle
        pygame.draw.circle(self.window, color, self.global_position, self.radius, 1)
        # draw vertical line
        pygame.draw.line(self.window, color, self.global_position+Vector2(0, self.radius), self.global_position+Vector2(0, -self.radius))
        # draw horizantal line
        pygame.draw.line(self.window, color, self.global_position+Vector2(self.radius, 0), self.global_position+Vector2(-self.radius, 0))

        super().draw()

    def collides_at(self, global_position:Vector2):
        if self.global_position != None:
            return self.global_position.distance_to(global_position) <= self.radius

