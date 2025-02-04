from multiprocessing import Pool
import ai as AI
from game import Game
from othello.othello import Othello, Immanuel


# how many games each proccesser handels (1/4 games total)
games_per_proccesser = 250
offset = 9000

# AIs
ais = (
    AI.Randy,
    Immanuel,
)


def proccess_game(proccesser):
    if proccesser % 2 == 0:
        ai_list = ais
    else:
        ai_list = (ais[1], ais[0])
    
    for i in range(games_per_proccesser):
        seed = proccesser+(i*4)+offset
        game = Othello(
            ai_list[0](seed),
            ai_list[1](seed),
        )

        if seed % 25 == 0:
            print(seed)

        game.start_game(True)


if __name__ == '__main__':
    items = [1, 2, 3, 4]
    with Pool(processes=4) as pool:
        pool.map(proccess_game, items)

