from typing import List
from deck import Deck
from hand import Hand
from player import Player


class BlackJack:
    DEFAULT_BET = 2
    deck: Deck
    dealer: Player
    dealerHand: Hand
    players: List[Player]
    hands: List[Hand]

    def __init__(self, numPacks: int = 1):
        self.dealer = Player('## Dealer')
        self.players = []
        self.deck = Deck(numPacks)
        self.initRound() 
        
    def addPlayer(self, name: str, money: float):
        player = Player(name, money)
        self.players.append(player)

    def initRound(self):
        ## init round
        self.dealerHand = Hand(self.dealer)
        self.hands = []
        self.current_hands = 0   

    def placeBets(self):        
        for player in self.players:
            hand = Hand(player)
            # Only players with enough money can place bets
            if hand.bet(self.DEFAULT_BET):
                self.hands.append(hand)

    def draw(self, hand: Hand, hidden: bool = False):
        card = self.deck.draw()
        card.hidden = hidden
        hand.add(card)

    def split(self, hand:Hand):
        card = hand.cards.pop()
        newHand = Hand(hand.player)
        newHand.bet(hand.betAmount)
        newHand.add(card);
        self.hands.insert(self.current_hands + 1, newHand)
        self.draw(hand)
        self.draw(newHand)

    def playerHand(self) -> Hand:
        return self.hands[self.current_hands] \
            if self.current_hands < len(self.hands) else None

    def settle(self, hand: Hand):
        match hand.result:
            case Hand.Status.LOSE:
                # Dealer takes the bet
                self.dealerHand.player.money += hand.betAmount;

            case Hand.Status.WIN:
                # natural win is half the bet
                if hand.isNatural():
                    winamount = hand.betAmount // 2
                else:
                    winamount = hand.betAmount
                # Dealer pays the winamount
                self.dealerHand.player.money -= winamount;
                # Player pockets original bet, plus dealer's payment
                hand.player.money += hand.betAmount + winamount

            case Hand.Status.EVEN:
                # Return money to player
                hand.player.money += hand.betAmount;

    # Deal one card to each hand and the dealer
    def deal1(self, dealerHidden: bool):
        for hand in self.hands:
            self.draw(hand);        
        self.draw(self.dealerHand, dealerHidden);

    def deal(self):
        # Deal 2 cards
        self.deal1(False)
        self.deal1(True)
        if self.dealerHand.isBlackJack():
            self.dealerHand.unhide()
            # all non black jack hands lose            
            for hand in self.hands:
                if not hand.isBlackJack():
                    hand.result = Hand.Status.LOSE

    def drawUntil(self, hand: Hand, until: int):
        while True:
            value = hand.getValue()
            if value == 0 or value >= until:
                break
            self.draw(hand)
        return value

    def playDealer(self):
        self.dealerHand.unhide()
        self.drawUntil(self.dealerHand, 17)

    def finalise(self) -> int:
        dealer = self.dealerHand.getValue()
        for hand in self.hands:
            hand.unhide()
            player = hand.getValue()
            if player > dealer:
                hand.result = Hand.Status.WIN                
            elif player == dealer:
                hand.result = Hand.Status.EVEN
            else:
                hand.result = Hand.Status.LOSE

    # find next active hands and set active, else return false
    def nextHand(self, active = False) -> bool:
        while True:
            self.current_hands += 1
            if self.current_hands >= len(self.hands):
                return False
            if active:
                if self.playerHand().isPlaying():
                    return True
                # else continue
            else:
                return True
