import pygame
import threading
import time
import os
import settings
from game import Game
from othello.othello import Othello
from window import GameObject, Sprite
from board import Board
from player import Player
import othello.othello_ais as AI


def start() -> None:
    """called once when game starts up"""
    GameObject.window = window
    GameObject.font = pygame.font.SysFont('Consolas', settings.font_size)
    
    start_game(Othello)


def update() -> None:
    """called once per frame"""
    window.fill(settings.background_color)
    check_events()

    for gameobject in GameObject.childeren:
        gameobject.update()

    pygame.display.update()


def check_events() -> None:
    """processes events that happened last frame"""
    global run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif open_game != None:
            open_game.check_events(event)


def start_game(game:Game):
    global open_game
    open_game = game()
    seed = 9947

    # ties
    # seed = 55
    # seed = 98
    # seed = 117

    # unfilled boards
    # seed = 111
    # seed = 159
    # seed = 164
    
    players = (
        # Player("Player 1"),
        AI.Immanuel(seed),
        # Player("Player 2"),
        AI.Randy(seed),
    )

    open_game.start_game(*players)

    # game_record = 'B43W26B19W42B37W38B33W44B49W10B12W18B2W25B53W34B30W5B39W32B24W62B51W41B40W46B55W48B56W45B50W17B61W3B16W20B13W14B1W57B58W54B21W0B6W29B4W7B47W9B63W23B22W11B8W60B59W31B15W52'
    # game_record = 'B43W26B20W45B44W42B34W12B13W19B18W25B32W10B52W59B17W51B4W11B41W6B3W48B50W40B21W29B38W16B24W57B49W58B14W47B61W22B15W5B7W60B46W1B56W37B39W23B53W33B9W55B54W8B63W62B30W31B0B2'
    # game_record = 'B20W37B46W19B26W17B10W29B24W11B44W34B42W52B12W55B30W38B51W41B60W50B43W31B22W21B23W14B57W18B47W3B13W4B40W53B54W45B39W63B15W2B62W59B9W16B33W7B58W32B25W6B1W49B8W61B5W56W0W48'
    
    # game_record = "B20W19B18W11B26W17B16W25B2W29B37W9B24W45B42W34B10W13B12W33B54W53B14W4B43W21B22W5B3W7B52W49B8W1B0W63B15W51B32W23B30W31B56W50B58W48B39W47B60W38B46W40B62W59B41W6B44W55B61W57"
    # game_record = "B34W44B53W33B41W26B17W19B20W49B11W62B18W37B52W3B54W8B25W21B22W60B38W43B40W39B45W55B31W23B16W46B13W5B48W12B0W30B57W24B50W10B32W51B29W42B59W58B4W2B6W56B9W1B61W14B15W7B63B47"
    # game_record = "B34W26B18W25B32W41B19W12B17W24B20W9B16W44B42W8B40W49B50W43B45W37B4W13B22W52B10W11B3W53B2W51B59W58B62W61B29W14B6W48B46W54B56W33B5W30B0W63B57W55B23W60B1W31B47W38B21W7B15W39"
    
    # thread = threading.Thread(target=open_game.show_game, args=(players, game_record))
    # thread.start()

    # open_game.show_record(players, game_record)


if __name__ == '__main__':
    # move window to second monitorf
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # initiate window
    pygame.init()
    pygame.display.set_caption("Table Top")

    # Set global vars
    open_game:Game = None; """game currently playing"""
    window = pygame.display.set_mode(settings.window_size)
    clock = pygame.time.Clock()
    start()

    # main loop
    run = True
    while run:
        clock.tick(settings.fps)
        update()

    pygame.quit()

