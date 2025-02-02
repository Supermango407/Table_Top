import sqlite3
import datetime
from player import Player


players = dict()


def set_players():
    global player_names
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `players`")

    rows = cursor.fetchall()
    for row in rows:
        players[row[1]] = row[0]

    conn.close()


def save_record(game_name:str, players_playing_game:tuple[Player], winner:str, record:str):
    """
    `game_name`: the name of the game.
    `players_playing_game`: the players playing `game`.
    `winner`: the turn index of the winner.
    `record`: the record (aka history) of game played.
    """
    player_ids = []
    for player in players_playing_game:
        if player.is_ai:
            player_name = player.name.upper()
        else:
            player_name = player.name.lower()
        player_ids.append(str(players[player_name]))

    now = datetime.datetime.now(datetime.timezone.utc)
    conn = sqlite3.connect('data.db')
    sql = f"INSERT INTO `game_records` VALUES (null, '{game_name}', '{','.join(player_ids)}', '{winner}', '{now}', '{record}');"
    
    conn.execute(sql)
    conn.commit()
    conn.close()


set_players()
print(players)
