import pygame
from dataclasses import dataclass

@dataclass
class Player(object):
    """class for object that is allow to make moves.
        `name`: the name of the player.
        `is_ai`: whether the player is ai.
    """
    name:str
    is_ai:bool = False

