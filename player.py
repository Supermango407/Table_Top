import pygame
from ai import Game_AI
from dataclasses import dataclass 


@dataclass
class Player(object):
    """`name`: the name of the player
    `controller`: the thing that make decisions.
        if left None will be controlled by user"""
    name:str = 'Player'
    controller:Game_AI = None

