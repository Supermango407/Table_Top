import pygame
import threading
import time
from pygame import Vector2
from typing import Union
import os
import sys
sys.path.append('../table_top')
import othello.game_settings as game_settings
from game import Game
from board import Board
from window import GameObject, Sprite
from player import Player


class Piece(Sprite):

    def __init__(self, color:str, position:Vector2, board:Board, hidden=False):
        """
        `color`: the color of the piece.
        `position`: where on the board the piece is placed.
        `board`: the board the piece is on.
        `hidden`: if True it will not draw the object
        """
        self.color = color
        self.position = position
        self.board = board

        super().__init__(hidden)

    def draw(self) -> None:
        pygame.draw.circle(
            GameObject.window,
            game_settings.piece_colors[Othello.colors.index(self.color)],
            self.board.get_global_position(self.position),
            game_settings.piece_size
        )

    def flip(self):
        """flips the piece and gives it to the other player."""
        self.color = Othello.colors[1] if self.color == Othello.colors[0] else Othello.colors[0]


class Othello(Game):
    colors = ('B', 'W')

    def __init__(self, *players:tuple[Player]):
        super().__init__("Othello", *players)
        self.board = Board(
            tile_size=game_settings.board['tile_size'],
            tile_border_width=game_settings.board['border_width'],
            tile_colors=game_settings.board['baground_color'],
            tile_border_color=game_settings.board['border_color']
        )
        
        self.start_table = [
            Piece(Othello.colors[0], Vector2(3, 3), self.board, True),
            Piece(Othello.colors[1], Vector2(3, 4), self.board, True),
            Piece(Othello.colors[1], Vector2(4, 3), self.board, True),
            Piece(Othello.colors[0], Vector2(4, 4), self.board, True),
        ]
        self.table = []

    def start_game(self):
        self.set_board()
        self.no_valid_moves = False
        super().start_game()

    def update(self):
        super().update()

    def draw(self):
        super().draw()
        for piece in self.table:
            piece.draw()

    def set_board(self):
        """sets up the board in the starting position"""
        # delete previuos game if it exsists
        if len(self.table) > 0:
            for piece in self.table:
                piece.destroy()
            self.table = []

        for piece in self.start_table:
            self.table.append(Piece(piece.color, piece.position, self.board))

    def next_turn(self, last_turn_skipped=False):
        super().next_turn()
        if len(self.moves) == 0:
            if last_turn_skipped:
                print('no valid moves')
                self.no_valid_moves = True
                self.end_game(self.get_winner())
            else:
                self.skip_turn()
        else:
            self.turn_text.set_color(game_settings.piece_colors[self.turn])
            
            if self.players[self.turn].is_ai:
                self.play_move(self.moves[self.players[self.turn].calculate_move(self.moves, self.table)])

    def get_winner(self):
        if self.no_valid_moves or len(self.table) >= 64:
            player_pieces = [0, 0]

            # count the number of pieces for each player
            for piece in self.table:
                player_pieces[Othello.colors.index(piece.color)] += 1
            
            if player_pieces[0] > player_pieces[1]:
                return 0
            elif player_pieces[1] > player_pieces[0]:
                return 1
            else:
                return 'tie'
        else:
            return None

    def skip_turn(self):
        """skips the turn of the current player."""
        print('turn skipped')
        self.next_turn(True)

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and not self.players[self.turn].is_ai:
                tile_pos = self.board.get_tile_at(pygame.mouse.get_pos())
                if tile_pos != None and self.valid_move(tile_pos):
                        self.play_move(tile_pos)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                # self.set_board()
                self.start_game()

    def set_moves(self):
        self.moves = []
        moves = self.board.get_all_tiles()

        # delete the moves that arent valid
        for move in moves:
            # if a peice is already there its not valid.
            if self.valid_move(move):
                self.moves.append(move)

    def play_move(self, move:Vector2):
        self.place_piece(move)
        super().play_move(move)

    def record_move(self, move:Vector2):
        self.history += Othello.colors[self.turn]
        self.history += str(self.board.get_tile_index(move))

    def valid_move(self, move:Vector2):
        # isn't valid if a piece is already there
        if self.get_piece_at(move) != None:
            # print('Piece There')
            return False
        
        # isn't valid if it doesn't flip any pieces
        if len(self.get_flip_pieces(move)) == 0:
            # print('None Flipped')
            return False
        
        return True

    def place_piece(self, position:Vector2) -> None:
        """places a peice on the board"""
        piece = Piece(Othello.colors[self.turn], position, self.board)
        self.table.append(piece)
        
        for piece in self.get_flip_pieces(position):
            piece.flip()

    def get_piece_at(self, position:Vector2):
        for piece in self.table:
            if piece.position == position:
                return piece
            
        return None

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
                piece_at_point_checking = self.get_piece_at(position + offset*i)
                
                # if no peice is at the `piece_at_point_checking`
                # then break out of nested loop 
                # and move of to the next direction
                if piece_at_point_checking == None:
                    break

                # if piece found is the same color as player
                # add `pieces_along_direction` to `pieces`
                # then move to the next direction
                if piece_at_point_checking.color == Othello.colors[self.turn]:
                    pieces.extend(pieces_along_direction)
                    break

                # if piece found is a difernt color than player
                # then add it to `piece_at_point_checking`
                else:
                    pieces_along_direction.append(piece_at_point_checking)
        
        return pieces
    
    def split_record(self, record:str) -> list[str]:
        """splits the records into move list"""
        moves = []
        move_string = ''
        for char in record:
            # if showing player string
            # then add the last move string to moves if exist
            # then create the next move string
            # otherwise just add char to the exsiting move string
            if char in Othello.colors:
                if move_string != '':
                    moves.append(move_string)
                move_string = char
            else:
                move_string += char
        moves.append(move_string)
        
        return moves

    def show_record(self, record):
        self.set_board()
        moves = self.split_record(record)

        for move_string in moves:
            self.play_move_string(move_string)

    def show_game(self, record):
        moves = self.split_record(record)
        
        self.set_board()
        for move in moves:
            time.sleep(0.1)
            self.play_move_string(move)

    def play_move_string(self, move_string:str) -> None:
        """playes move based off `move_string`"""
        player = move_string[0]
        self.turn = Othello.colors.index(player)
        tile_pos = self.board.get_tile_from_index(int(move_string[1:]))
        self.place_piece(tile_pos)

    def debug_print_table(self):
        """prints the table to the console."""
        print('-'*80)
        for piece in self.table:
            print('\t', piece.position)
        print('-'*80)

