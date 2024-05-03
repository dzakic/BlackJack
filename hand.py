from typing import List
from cards import Card
from cards import CardList
from player import Player

class Hand(CardList):
    betAmount: int
    player: Player

    def __init__(self, player: Player):
        self.cards = []
        self.player = player
        self.betAmount = 0

    def getValue(card: Card) -> int:
        value = card.getRank() + 1
        return value if value < 10 else 10

    def getValues(self):
        # return a list of integers of all possible interpretations 
        # for A being 1 or 11
        count = 1
        result = [0]
        for card in self.cards:
            cardValue = Hand.getValue(card)
            for i in range(0, len(result)):
                result[i] += cardValue
            if cardValue == 1:
                ace_result = []
                for res in result:
                    ace_result.append(res + 10)
                result += ace_result;
        return result
    
    def getBestValue(self) -> int:
        # of all possible values, get the one closest but not over 21
        values = self.getValues()
        best = 0
        for value in values:
            if value <= 21:
                if value > best:
                    best = value
        return best
    
    def isBlackJack(self) -> bool:
        return self.getBestValue() == 21

    def isBust(self) -> bool:
        return self.getBestValue() == 0

    def bet(self, amount: int) -> bool:
        canBet = self.player.money >= amount
        if canBet:
            self.player.money -= amount
            self.betAmount += amount
        return canBet

    def doubleDown(self) -> bool:
        return self.bet(self.betAmount)

    def clear(self):
        self.betAmount = 0

    def add(self, card: Card):
        self.cards.append(card)

    def unhide(self):
        for card in self.cards:
            card.hidden = False

    def dump(self):
        print("{name:<10} ${money:>3}: {hand:<18} ({value:>2}) ${bet}"
            .format(
                name = self.player.name,
                money = self.player.money,
                hand = str(self),
                value = self.getBestValue(),
                bet = self.betAmount))
