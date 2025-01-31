import pygame
from pygame import Vector2
from typing import Union
import os
import sys
sys.path.append('../table_top')
import othello.game_settings as game_settings
from game import Game
from board import Board, TilePosition
from window import GameObject, Sprite
from player import Player


class Piece(Sprite):
    childeren = []

    @staticmethod
    def get_piece_at(position:Vector2):
        for piece in Piece.childeren:
            if piece.position == position:
                return piece
            
        return None

    def __init__(self, player:int, position:Union[Vector2, TilePosition]):
        """
        `player`: the player who controls the piece.
        `position`: the position on the board the peice is on.
        """
        self.player = player

        if type(position) == Vector2:
            self.position = TilePosition(position)
        else:
            self.position = position

        self.childeren.append(self)
        super().__init__()

    def update(self) -> None:
        """called once per frame"""
        self.draw()

    def draw(self) -> None:
        pygame.draw.circle(
            self.window,
            game_settings.piece_colors[self.player],
            self.position.get_global_position(),
            game_settings.piece_size
        )

    def flip(self):
        """flips the piece and gives it to the other player."""
        self.player = 0 if self.player == 1 else 1


class Othello(Game):
    
    def __init__(self, *players:tuple[Player]):
        self.board = Board(
            tile_size=game_settings.board['tile_size'],
            tile_border_width=game_settings.board['border_width'],
            tile_colors=game_settings.board['baground_color'],
            tile_border_color=game_settings.board['border_color']
        )

        self.table = [
            Piece(0, Vector2(3, 3)),
            Piece(1, Vector2(3, 4)),
            Piece(1, Vector2(4, 3)),
            Piece(0, Vector2(4, 4)),
        ]

        super().__init__(*players)

    def update(self):
        super().update()

    def next_turn(self):
        super().next_turn()
        if len(self.moves) == 0:
            self.skip_turn()

    def get_winner(self):
        if len(Piece.childeren) >= 64:
            player_pieces = [0, 0]

            # count the number of pieces for each player
            for piece in Piece.childeren:
                player_pieces[piece.player] += 1
            
            if player_pieces[0] > player_pieces[1]:
                return 0
            else:
                return 1
        else:
            return None

    def skip_turn(self):
        """skips the turn of the current player."""
        print('turn skipped')
        self.next_turn()

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            tile_pos = self.board.get_tile_at(pygame.mouse.get_pos())
            if tile_pos != None:
                if event.button == 1:
                    self.play_move(tile_pos)

    def set_moves(self):
        self.moves = []
        moves = self.board.get_all_tiles()

        # delete the moves that arent valid
        for move in moves:
            # if a peice is already there its not valid.
            if self.valid_move(move):
                self.moves.append(move)

    def play_move(self, move:TilePosition):
        if self.valid_move(move):
            self.place_piece(move)
            super().play_move()

    def valid_move(self, move:TilePosition):
        # isn't valid if a piece is already there
        if Piece.get_piece_at(move) != None:
            return False
        
        # isn't valid if it doesn't flip any pieces
        if len(self.get_flip_pieces(move)) == 0:
            return False
        
        return True

    def place_piece(self, position:Vector2) -> None:
        """places a peice on the board if valid option."""
        if self.valid_move(position):
            Piece(self.turn, position)
            for piece in self.get_flip_pieces(position):
                piece.flip()

    def get_flip_pieces(self, position:Vector2) -> list[Piece]:
        """reutrns a list of pieces that will flip if a peice is placed at `position`"""
        pieces = [] # the reutrn value

        # `direction_offets`: the amount you add for each direcion
        # that needs to be checked.
        direction_offets = [
            Vector2(0, -1), # top
            Vector2(1, -1), # top right
            Vector2(1, 0), # right
            Vector2(1, 1), # bottom right
            Vector2(0, 1), # bottom
            Vector2(-1, 1), # bottom left
            Vector2(-1, 0), # left
            Vector2(-1, -1), # top left
        ]
        
        for offset in direction_offets:
            # `pieces_along_direction` will be thrown out
            # if it can't find a piece of the same color
            # as the current player.
            # if it does find one it will be added to `pieces`
            pieces_along_direction = []

            # does range 1-7 cause thats the most the pieces
            # that can be fliped in a specific direction
            for i in range(1, 8):
                piece_at_point_checking = Piece.get_piece_at(position + offset*i)
                
                # if no peice is at the `piece_at_point_checking`
                # then break out of nested loop 
                # and move of to the next direction
                if piece_at_point_checking == None:
                    break

                # if piece found is the same color as player
                # add `pieces_along_direction` to `pieces`
                # then move to the next direction
                if piece_at_point_checking.player == self.turn:
                    pieces.extend(pieces_along_direction)
                    break

                # if piece found is a difernt color than player
                # then add it to `piece_at_point_checking`
                else:
                    pieces_along_direction.append(piece_at_point_checking)
        
        return pieces
    
