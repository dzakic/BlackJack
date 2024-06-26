from typing import List

class Card:
    Suits = "\u2660\u2663\u2665\u2666" ## "♡♢♣♠"
    Ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
    card: int
    hidden: bool = False

    def __init__(self, card: int):
        self.card = card

    def getSuit(self) -> int:
        return self.card // 13
    
    def getRank(self) -> int:
        return self.card % 13

    def __str__(self):
        if self.hidden:
            return "??"
        else:
            return Card.Ranks[self.getRank()] + Card.Suits[self.getSuit()]
    
class CardList:
    cards: List[Card]

    def __init__(self):
        self.cards = []

    def __getitem__(self, index) -> Card:
        return self.cards[index]
    
    def __str__(self) -> str:
        #str = ""
        #for index in range(len(self.cards)):
        #    str = str + f"{self[index]} "
        #return str
        return " ".join(map(lambda index: str(self[index]), range(len(self.cards))))

    def add(self, card: Card):
        self.cards.append(card)

    def public(self):
        return not any(map(lambda index: self[index].hidden, range(len(self.cards))))