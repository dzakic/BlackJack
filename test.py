from bjack import BlackJack
from board import BlackJackWindow

# Test
game = BlackJack(numPacks = 3)
game.addPlayer("Zak", 1000)
game.addPlayer("Danilo", 2000)
board = BlackJackWindow(game)
board.play()
