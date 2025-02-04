import threading
import time
import ai as AI
from game import Game
from othello.othello import Othello


for i in range(0, 1):
    game = Othello(
        # Player("Player 1"),
        AI.Randy(i),
        # Player("Player 2"),
        AI.Randy(i),
    )

    print(i)
    game.start_game()
    print()

