import threading
import time
from multiprocessing import Pool
import ai as AI
from game import Game
from othello.othello import Othello


# how many games each proccesser handels (1/4 games total)
games_per_proccesser = 2500


def proccess_game(proccesser):
    for i in range(1, games_per_proccesser+1):
        seed = proccesser*i
        game = Othello(
            # Player("Player 1"),
            AI.Randy(seed),
            # Player("Player 2"),
            AI.Randy(seed),
        )

        if seed % 10 == 0:
            print(seed)
        game.start_game()


if __name__ == '__main__':
    items = [1, 2, 3, 4]
    with Pool(processes=4) as pool:
        pool.map(proccess_game, items)

