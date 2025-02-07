import sqlite3
import datetime
from player import Player


# TODO: have the connection inputed,
# so it doesn't have to reconnect
# each time the function is called
def save_record(game_name:str, players_playing_game:tuple[Player], winner:str, record:str):
    """
    `game_name`: the name of the game.
    `players_playing_game`: the players playing `game`.
    `winner`: the turn index of the winner.
    `record`: the record (aka history) of game played.
    """
    # gets the player name and ai record names if ai is used
    player_names = [
        player.record_name if player.is_ai 
        else player.name.lower() 
        for player in players_playing_game
    ]
    now = datetime.datetime.now(datetime.timezone.utc)

    with sqlite3.connect('data.db') as conn:
        sql = f"""INSERT INTO 
            `game_records`(
                `game`,
                `players`,
                `winner`,
                `date`,
                `record`
            ) 
            VALUES (
                '{game_name}',
                '{','.join(player_names)}',
                '{winner}',
                '{now}',
                '{record}');
        """
        # print(sql)
        conn.commit()


def wins_for_pvp(player_1, player_2, game_name):
    """get how many wins, losses and draws there are for
    player_1 vs player_2 in game `game`"""
    # the possible winners for a 1 on 1 game
    games_won = dict()

    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()

        for winner in ['0', 'tie', '1']:
            sql = f"""SELECT COUNT() from `game_records`
            WHERE `players` LIKE '{player_1.name}(%),{player_2.name}(%)'
            AND `winner` == '{winner}' AND `game` = '{game_name}';"""
        
            cursor.execute(sql)
            games_won[winner] = cursor.fetchall()[0][0]
        
    return games_won

