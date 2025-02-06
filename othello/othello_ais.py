import pygame
from pygame import Vector2
from dataclasses import dataclass
import sys
sys.path.append('../table_top')
import othello.othello as othello
import ai as AI
from ai import Randy


class Immanuel(AI.Immanuel):

    def calculate_move(self, options:list[othello.Move], table):
        biggest_move = 0
        moves = []

        for i, move in enumerate(options):
            # how many pieces will be flipped
            flip_count = len(othello.get_flip_pieces(move, table))
            if flip_count > biggest_move:
                biggest_move = flip_count
                moves = [i]
            elif flip_count == biggest_move:
                moves.append(i)
        
        # for move in moves:
        #     print(options[move])
        # print()

        return self.generator.choice(moves)

