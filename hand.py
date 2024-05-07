from cards import Card, CardList
from player import Player
from enum import Enum

class Hand(CardList):

    class Status(Enum):
        LOSE = -1
        PLAYING = 0
        EVEN = 1
        WIN = 2

    player: Player
    betAmount: int
    result: Status

    def __init__(self, player: Player):
        CardList.__init__(self)
        self.player = player
        self.betAmount = 0
        self.result = Hand.Status.PLAYING

    def getCardValue(card: Card) -> int:
        value = card.getRank() + 1
        return value if value < 10 else 10

    def getValue(self) -> int:
        handValue = 0
        numAces = 0
        for card in self.cards:
            value = Hand.getCardValue(card)
            if value == 1:
                numAces += 1
                handValue += 10
            handValue += value        
        while handValue > 21 and numAces > 0:
            handValue -= 10
            numAces -= 1
        
        return handValue if handValue <= 21 else 0

    def isBlackJack(self) -> bool:
        return self.getValue() == 21

    def isNatural(self) -> bool:
        return len(self.cards) == 2 and self.isBlackJack()

    def isBust(self) -> bool:
        return self.getValue() == 0
    
    def isSplittable(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].getRank() == self.cards[1].getRank()

    def isPlaying(self) -> bool:
        return self.result == Hand.Status.PLAYING

    def bet(self, amount: int) -> bool:
        canBet = self.player.money >= amount
        if canBet:
            self.player.money -= amount
            self.betAmount += amount
        return canBet

    def doubleDown(self) -> bool:
        return self.bet(self.betAmount)

    def unhide(self):
        for card in self.cards:
            card.hidden = False

    def dump(self):
        print("{name:<10} ${money:>3}: {hand:<18} ({value:>2}) ${bet}"
            .format(
                name = self.player.name,
                money = self.player.money,
                hand = str(self),
                value = self.getValue(),
                bet = self.betAmount))
