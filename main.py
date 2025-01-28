import pygame
import os
import settings
from game import Game
from othello.othello import Othello


def start() -> None:
    """called once when game starts up"""
    start_game(Othello)


def update() -> None:
    """called once per frame"""
    window.fill(settings.background_color)
    check_events()
    open_game.update()
    pygame.display.update()


def check_events() -> None:
    """processes events that happened last frame"""
    global run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


def start_game(game:Game):
    global open_game
    open_game = game(window)


if __name__ == '__main__':
    # move window to second monitorf
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # Set global vars
    open_game = None; """game currently playing"""
    window = pygame.display.set_mode(settings.window_size)
    clock = pygame.time.Clock()
    start()

    # main loop
    run = True
    while run:
        clock.tick(settings.fps)
        update()

    pygame.quit()

