import sqlite3
import datetime
from player import Player


def save_record(game_name:str, players_playing_game:tuple[Player], winner:str, record:str):
    """
    `game_name`: the name of the game.
    `players_playing_game`: the players playing `game`.
    `winner`: the turn index of the winner.
    `record`: the record (aka history) of game played.
    """
    # gets the player names and ai record names if ai is used
    player_names = [
        player.record_name if player.is_ai 
        else player.name.lower() 
        for player in players_playing_game
    ]

    now = datetime.datetime.now(datetime.timezone.utc)
    conn = sqlite3.connect('data.db')
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

    conn.execute(sql)
    conn.commit()
    conn.close()

