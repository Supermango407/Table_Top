import pygame
import os
import settings
from game import Game
from othello.othello import Othello
from window import GameObject, Sprite
from board import Board


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

