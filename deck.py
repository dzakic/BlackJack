from cards import Card, CardList
import random

class Deck(CardList):
    numPacks: int

    def __init__(self, numPacks: int = 1):
        self.numPacks = numPacks
        self.initialise()

    def initialise(self):
        self.cards = [None] * 52 * self.numPacks
        for pack in range(0, self.numPacks):
            for index in range(0, 52):
                self.cards[52 * pack + index] = Card(index)
        self.shuffle()

    def shuffle(self):
        num = len(self.cards)
        for index in range(0, num - 1):
            remain = num - index - 1
            other = index + 1 + random.randrange(remain)
            # swap index and other
            temp = self.cards[index]
            self.cards[index] = self.cards[other]
            self.cards[other] = temp

        print("Deck shuffled: ", self)

    def draw(self) -> Card:
        if not self.cards:
            self.initialise()
        return self.cards.pop()
