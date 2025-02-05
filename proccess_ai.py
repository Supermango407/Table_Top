from multiprocessing import Pool
import ai as AI
import data
from othello.othello import Othello, Immanuel


# how many games each proccesser handels (1/4 games total)
games_per_proccesser = 250
seed_start_index = 0
winner_options = ['0', 'tie', '1']

# AIs
ais = (
    Immanuel,
    AI.Randy,
)


def proccess_game(proccesser:int):
    if proccesser % 2 == 0:
        ai_list = ais
    else:
        ai_list = (ais[1], ais[0])
    
    for i in range(games_per_proccesser):
        seed = proccesser+(i*4)+seed_start_index
        game = Othello(
            ai_list[0](seed),
            ai_list[1](seed),
        )

        if seed % 25 == 0:
            print(seed)

        game.start_game(True)


def analize_winrate(players:tuple):
    p1_first = data.wins_for_pvp(players[0](), players[1](), "Othello")
    p2_first = data.wins_for_pvp(players[1](), players[0](), "Othello")
    
    player_winnrate = {
        '0': p1_first['0']+p2_first['1'],
        'tie': p1_first['tie']+p2_first['tie'],
        '1': p1_first['1']+p2_first['0'],
    }

    return player_winnrate


def add_winrates(winrate_1:dict, winrate_2:dict):
    """adds winns losses and ties for `winrate_1` and `winrate_2`."""
    winrate = dict()
    for option in winner_options:
        winrate[option] = winrate_1[option]+winrate_2[option]
    
    return winrate


def skill_score(winrate:dict):
    """caculate skill score based off of `winrate`"""
    if winrate['0'] >= winrate['1']:
        return winrate['0']/winrate['1'] - 1
    else:
        return 1 - winrate['1']/winrate['0']


winrate = analize_winrate(ais)
print(winrate)
print(skill_score(winrate))

# if __name__ == '__main__':
    # items = [1, 2, 3, 4]
    # with Pool(processes=4) as pool:
    #     pool.map(proccess_game, items)

