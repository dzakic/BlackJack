from login import LoginWindow
from bjack import BlackJack

# Main
login = LoginWindow()
player = login.getUsername()
if player:
    print(f"Hello {player}, welcome to a game of Black Jack")
    game = BlackJack(numPacks = 2)
    game.addPlayer(player)
    game.play()