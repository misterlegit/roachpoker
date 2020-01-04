from game import *

players = [Player(isCPU=False)]
for i in range(4):
    players.append(Player(sleepDuration=1))

game = Game(players)
game.run()
