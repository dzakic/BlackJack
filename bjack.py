from typing import List
from deck import Deck
from round import Round
from player import Player

class BlackJack:
    deck: Deck
    dealer: Player
    players: List[Player]

    def __init__(self, numPacks: int = 1):
        self.dealer = Player('<Dealer>')
        self.players = []
        self.deck = Deck(numPacks)

    def showStats(self, count: int):
        print("====== Game #", count, "  Deck: ", len(self.deck.cards))
        print(self.dealer)
        for player in self.players:
            print(player)


    def addPlayer(self, name: str, money: float):
        player = Player(name, money)
        self.players.append(player)

    def play(self):
        count = 0
        while True:
            count += 1
            round = Round(self.deck, self.dealer, self.players)
            # Any players with money?
            if round.play():
                self.showStats(count)
            else:
                return
