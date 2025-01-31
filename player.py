import pygame


class Player(object):
    """class for object that is allow to make moves."""

    def __init__(self, name:str = 'Player', is_ai:bool=False):
        """
        `name`: the name of the player
        `controller`: the thing that make decisions.
            if left None will be controlled by user
        """
        self.name = name
        self.is_ai = is_ai

