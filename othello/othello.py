import pygame
import threading
import time
from pygame import Vector2
from dataclasses import dataclass
import sys
sys.path.append('../table_top')
import othello.game_settings as game_settings
from game import Game, Game_Table, GameVars
import ai as AI
from board import Board, Piece
from window import GameObject, Sprite
from player import Player


@dataclass
class Table(Game_Table):
    """curent set up of board
        `turn`: whos turn it currently is.
        `pieces`: pieces on board.
    """
    pieces:list[Piece]


@dataclass
class Move(object):
    """a piece being placed by a player.
        `tile`: where the piece is being placed.
        `player`: player placeing `piece`.
    """
    tile:Vector2
    player:int


class Othello_Piece(Piece):
    """a piece for othello."""

    def __init__(self, tile:Vector2, player:int):
        self.player = player
        super().__init__(tile, None, game_settings.piece_colors[player], False)

    # TODO: Add flip animation
    def flip(self):
        """flips the piece and gives it to the other player."""
        self.player = 1 if self.player == 0 else 0
        self.color = game_settings.piece_colors[self.player]


class Othello(Game):
    game_vars:GameVars = GameVars("othello", 2)
    colors:tuple[str, str] = ('B', 'W')

    def __init__(self):
        super().__init__()
        self.board = Board(
            tile_size=game_settings.board['tile_size'],
            tile_border_width=game_settings.board['border_width'],
            tile_colors=game_settings.board['baground_color'],
            tile_border_color=game_settings.board['border_color']
        )

        self.table = Table(-1, [])

    def start_game(self, *players:tuple[Player], save_record=False):
        self.set_board()
        self.no_valid_moves = False
        super().start_game(*players, save_record=save_record)

    def set_board(self) -> None:
        """sets up the board in the starting position"""
        # delete previuos game if it exsists
        if len(self.table.pieces) > 0:
            for piece in self.table.pieces:
                piece.destroy()
            self.table.pieces = []
            self.board.pieces = dict()


        self.place_piece(Vector2(3, 3), 0)
        self.place_piece(Vector2(3, 4), 1)
        self.place_piece(Vector2(4, 3), 1)
        self.place_piece(Vector2(4, 4), 0)
        # print(self.table.pieces)
        
    def next_turn(self, last_turn_skipped=False):
        super().next_turn()

        # no valid move for current player
        if len(self.moves) == 0:
            if last_turn_skipped:
                # if the last player was skipped then
                # there are no valid moves for either player
                # and the game ends.
                self.no_valid_moves = True
                self.end_game(self.get_winner())
            else:
                self.skip_turn()
        else:
            self.set_turn_color(self.table.turn)
            if self.players[self.table.turn].is_ai:
                self.ai_play_move()

    def set_turn_color(self, player:int) -> None:
        """sets the color of Turn Text, if it exsits, to `player`'s color."""
        if GameObject.window != None:
            self.turn_text.set_color(game_settings.piece_colors[player])

    def valid_move(self, move:Move):
        return valid_move(move, self.table)

    def get_winner(self):
        # if no player has a valid move
        # or the board is filled up
        if self.no_valid_moves or len(self.table.pieces) >= 64:
            player_pieces = [0, 0]

            # count the number of pieces for each player
            for piece in self.table.pieces:
                player_pieces[piece.player] += 1
            
            if player_pieces[0] > player_pieces[1]:
                return 0
            elif player_pieces[1] > player_pieces[0]:
                return 1
            else:
                return 'tie'
        else:
            return None

    def skip_turn(self) -> None:
        """skips the turn of the current player."""
        self.next_turn(True)

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and not self.players[self.table.turn].is_ai:
                tile_pos = self.board.get_tile_at(pygame.mouse.get_pos())
                if tile_pos != None:
                    move = Move(tile_pos, self.table.turn)
                    if self.valid_move(move):
                        self.play_move(move)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                self.set_board()
                # self.start_game()

    def set_moves(self):
        self.moves = []
        tiles = self.board.get_all_tiles()

        # add the moves that are valid
        for tile in tiles:
            move = Move(tile, self.table.turn)

            if self.valid_move(move):
                self.moves.append(move)

    def play_move(self, move:Move):
        self.place_piece(move.tile, move.player)
        super().play_move(move)

    def ai_play_move(self):
        """called when its on ais turn,"""
        self.play_move(self.moves[self.players[self.table.turn].calculate_move(self.moves, self.table)])

    def record_move(self, move:Move):
        self.history += Othello.colors[self.table.turn]
        self.history += str(self.board.get_tile_index(move.tile))

    def place_piece(self, tile:Vector2, player:int) -> None:
        """places a peice on the board, and flips pieces."""
        piece = Othello_Piece(tile, player)
        self.board.place_piece(tile, piece)
        self.table.pieces.append(piece)
        for piece in get_flip_pieces(Move(tile, player), self.table):
            piece.flip()

    def split_record(self, record:str) -> list[str]:
        """returns split record into move list."""
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

    def show_record(self, players, record:str):
        self.players = players
        moves = self.split_record(record)
        self.set_board()

        for move_string in moves:
            self.play_move_string(move_string)

        # set `no_valid_moves` to True to make sure the game ends
        self.no_valid_moves = True
        self.set_winner_text(self.get_winner())

    def show_game(self, players, record):
        self.players = players
        moves = self.split_record(record)
        self.set_board()

        self.set_turn_text(0)
        self.set_turn_color(0)
        
        for move in moves:
            time.sleep(0.1)
            self.set_turn_text(self.table.turn)
            self.set_turn_color(self.table.turn)
            self.play_move_string(move)
        
        # set `no_valid_moves` to True to make sure the game ends
        self.no_valid_moves = True
        self.set_winner_text(self.get_winner())

    def play_move_string(self, move_string:str) -> None:
        """playes move based off `move_string`"""
        player = move_string[0]
        self.table.turn = Othello.colors.index(player)
        tile_pos = self.board.get_tile_from_index(int(move_string[1:]))
        self.place_piece(tile_pos, self.table.turn)

    def set_winner_text(self, winner) -> None:
        super().set_winner_text(winner)
        if GameObject.window != None:
            if type(winner) == int:
                self.turn_text.set_color(game_settings.piece_colors[winner])
            elif type(winner) == str:
                self.turn_text.set_color(game_settings.tie_color)


def valid_move(move:Move, table:Table) -> bool:
    """whether making `move` on `table` is a valid move."""
    # isn't valid if a piece is already there
    if get_piece_at(move.tile, table) != None:
        # print('Piece There')
        return False
    
    # isn't valid if it doesn't flip any pieces
    if len(get_flip_pieces(move, table)) == 0:
        # print('None Flipped')
        return False
    
    return True


def get_piece_at(tile:Vector2, table:Table) -> Piece:
    """returns piece on table, at `tile`, if it exsists."""
    for piece in table.pieces:
        if piece.tile == tile:
            return piece
        
    return None


def get_flip_pieces(move:Move, table:Table) -> list[Piece]:
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
                piece_at_point_checking:Othello_Piece = get_piece_at(move.tile + offset*i, table)
                
                # if no peice is at the `piece_at_point_checking`
                # then break out of nested loop 
                # and move of to the next direction
                if piece_at_point_checking == None:
                    break

                # if piece found is the same color as player
                # add `pieces_along_direction` to `pieces`
                # then move to the next direction
                if piece_at_point_checking.player == move.player:
                    pieces.extend(pieces_along_direction)
                    break

                # if piece found is a difernt color than player
                # then add it to `piece_at_point_checking`
                else:
                    pieces_along_direction.append(piece_at_point_checking)
        
        return pieces

