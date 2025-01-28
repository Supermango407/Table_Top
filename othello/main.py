import pygame
import os
import sys
sys.path.append('../table_top')
import game_settings
import settings


def start() -> None:
    """called once when game starts up"""
    pass


def update() -> None:
    """called once per frame"""
    window.fill(game_settings.background_color)
    check_events()
    pygame.display.update()


def check_events() -> None:
    """processes events that happened last frame"""
    global run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


if __name__ == '__main__':
    # move window to second monitorf
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # Set global vars
    window = pygame.display.set_mode(settings.window_size)
    clock = pygame.time.Clock()
    start()

    # main loop
    run = True
    while run:
        clock.tick(settings.fps)
        update()

    pygame.quit()

