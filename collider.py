from __future__ import annotations
from typing import Union
from collections.abc import Callable
import pygame
from pygame import Vector2
from window import GameObject, Sprite


class ClickableSprite(Sprite):
    
    def __init__(self, position, collider_type:type[Collider], onclick:Callable=None, show_collider:bool=False, hidden=False, check_events=False):
        """
        `position`: the position of sprite.
        `collider_type`: the type of collider of the sprite.
        """
        super().__init__(position=position, hidden=hidden, check_events=check_events)
        self.collider = collider_type(position=self, onclick=onclick, show=show_collider)
    
    def set_position(self, position):
        super().set_position(position)
        self.collider.position = position

    def destroy(self):
        self.collider.destroy()
        return super().destroy()


class Collider(GameObject):

    def __init__(self, position:Union[Vector2, Sprite]=None, onclick:Callable=None, show:bool=False):
        """
        `position`: the position of the collider.
            if adding it to Sprite use sprite
            if global collider use Vector2
        `onclick`: funtion to be called when clicked.
        `show`: if True it will show outline of `self` on screen.
        """
        super().__init__(check_events=True)
        self.onclick = onclick
        self.position, self.sprite = self.get_pos_and_sprite(position)
        self.mouse_over = self.collides_at(self.mouse_pos)
        self.show = show
    
    def get_pos_and_sprite(self, value:Union[Vector2, Sprite]):
        """if value is a sprite, returns a tuple with `position` of sprites and sprite.
        otherwise returns value and None"""
        if isinstance(value, Sprite):
            try:
                return (value.position, value)
            except AttributeError:
                print(value, "doesn't have position")
                return(Vector2(0, 0), value)
        else:
            return (value, None)

    def update(self):
        super().update()
        if self.show and self.position != None:
            self.draw()
    
    def draw(self) -> None:
        """draws outline of `self` to screen."""
        pass

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_over = self.collides_at(self.mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.onclick != None and self.mouse_over:
                self.onclick()

    def collides_at(self, position:Vector2) -> bool:
        """whether the collider covers point `position`"""
        return False


class CircleCollider(Collider):

    def __init__(self, position, onclick:Callable=None, radius:float=0, show=False):
        self.radius = radius
        super().__init__(position, onclick=onclick, show=show)

    def draw(self):
        color = (255, 0, 0) if self.mouse_over else (0, 255, 0)
        # draw circle
        pygame.draw.circle(self.window, color, self.position, self.radius, 1)
        # draw vertical line
        pygame.draw.line(self.window, color, self.position+Vector2(0, self.radius), self.position+Vector2(0, -self.radius))
        # draw horizantal line
        pygame.draw.line(self.window, color, self.position+Vector2(self.radius, 0), self.position+Vector2(-self.radius, 0))

    def collides_at(self, position):
        if self.position != None:
            return self.position.distance_to(position) <= self.radius

