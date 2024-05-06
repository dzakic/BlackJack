from login import LoginWindow
from bjack import BlackJack
from board import BlackJackWindow

# Main
login = LoginWindow()
playerName = login.getUsername()

if playerName:
    print(f"Hello {playerName}, welcome to a game of Black Jack")

    game = BlackJack(numPacks = 2)
    game.addPlayer(playerName, 200)

    board = BlackJackWindow(game)
    board.play()
