from multiprocessing import Pool
import ai as AI
import data
from othello.othello import Othello, Immanuel


# how many games each proccesser handels (1/4 games total)
games_played = 100
seed_start_index = 0
winner_options = ['0', 'tie', '1']

# Settings
processers = 4
ais = (
    Immanuel,
    AI.Randy,
)
game = Othello()

def process_game(processer:int):
    print(f"Processer {processer} started")
    
    for i in range(games_played//processers):
        seed = processer+(i*processers)+seed_start_index
        if processer % 2 == 0:
            players = (ais[0](seed), ais[1](seed))
        else:
            players = (ais[1](seed), ais[0](seed))

        if seed % 25 == 0:
            print(seed)

        game.start_game(*players)
    
    print(f"Processer {processer} finished")


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


# winrate = analize_winrate(ais)
# print(winrate)
# print(skill_score(winrate))

if __name__ == '__main__':
    if processers > 1:
        items = list(range(1, processers+1))
        print(items)
        with Pool(processes=4) as pool:
            pool.map(process_game, items)
    else:
        process_game(1)

