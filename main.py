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
import ai as AI


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
    open_game = game(
        # Player("Player 1"),
        AI.Randy(),
        # Player("Player 2"),
        AI.Randy(),
    )
    open_game.start_game()
    # open_game.show_record('B43W26B19W42B37W38B33W44B49W10B12W18B2W25B53W34B30W5B39W32B24W62B51W41B40W46B55W48B56W45B50W17B61W3B16W20B13W14B1W57B58W54B21W0B6W29B4W7B47W9B63W23B22W11B8W60B59W31B15W52')
    # open_game.show_record('B43W26B20W45B44W42B34W12B13W19B18W25B32W10B52W59B17W51B4W11B41W6B3W48B50W40B21W29B38W16B24W57B49W58B14W47B61W22B15W5B7W60B46W1B56W37B39W23B53W33B9W55B54W8B63W62B30W31B0B2')
    # open_game.show_record('B20W37B46W19B26W17B10W29B24W11B44W34B42W52B12W55B30W38B51W41B60W50B43W31B22W21B23W14B57W18B47W3B13W4B40W53B54W45B39W63B15W2B62W59B9W16B33W7B58W32B25W6B1W49B8W61B5W56W0W48')
    
    thread = threading.Thread(target=open_game.show_game, args=("B20W37B46W19B26W17B10W29B24W11B44W34B42W52B12W55B30W38B51W41B60W50B43W31B22W21B23W14B57W18B47W3B13W4B40W53B54W45B39W63B15W2B62W59B9W16B33W7B58W32B25W6B1W49B8W61B5W56W0W48",))
    thread.start()


if __name__ == '__main__':
    # move window to second monitorf
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

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

