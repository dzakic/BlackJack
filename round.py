from typing import List
from cards import Deck
from hand import Hand
from player import Player

class Round:
    deck: Deck
    dealerHand: Hand
    hands: List[Hand]
    players: List[Player]

    def __init__(self, deck: Deck, dealer: Player, players: List[Player]):
        self.deck = deck
        self.dealerHand = Hand(dealer)
        self.hands = []
        self.placeBets(players)

    def draw(self, hand: Hand, hidden: bool = False):
        card = self.deck.draw()
        card.hidden = hidden
        hand.add(card)

    # Fold hands, bet lost
    def fold(self, hand: Hand):
        # Dealer takes the bet
        self.dealerHand.player.money += hand.betAmount;
        hand.clear()

    # Hands won the bet
    def win(self, hand: Hand):
        # natural win is half the bet
        if len(hand.cards) == 2:
            winamount = hand.betAmount // 2
        else:
            winamount = hand.betAmount
        # Dealer pays the winamount
        self.dealerHand.player.money -= winamount;
        # Player pockets original bet, plus dealer's payment
        hand.player.money += hand.betAmount + winamount
        hand.clear()

    # Equal to dealer, noone wins
    def even(self, hand: Hand):
        # Return money to player
        hand.player.money += hand.betAmount;
        hand.clear()

    # Deal one card to each hand and the dealer
    def deal1(self, dealerHidden: bool):
        for hand in self.hands:
            self.draw(hand);        
        self.draw(self.dealerHand, dealerHidden);

    def deal(self):
        # Deal 2 cards
        self.deal1(False)
        self.deal1(True)

    def showStats(self):
        print("===")
        self.dealerHand.dump()
        for hand in self.hands:
            hand.dump()
       
    def drawUntil(self, hand: Hand, until: int):
        while True:
            value = hand.getBestValue()
            if value == 0 or value >= until:
                break
            self.draw(hand)
        return value

    def basicStrategy(upcard) -> int:
        if upcard >= 7:
            return 17
        if upcard <= 3:
            return 13
        else:   
            return 12

    def playPlayer(self, hand: Hand):
        if len(hand.cards) == 2 and hand.cards[0].getRank() == hand.cards[1].getRank():
            # OPTION to split [Y/N]
            index = self.hands.index(hand);
            splitHand = Hand(hand.player)
            splitHand.add(hand.cards.pop())
            splitHand.bet(hand.betAmount)
            self.hands.insert(index + 1, splitHand)

        player = hand.getBestValue()
        if len(hand.cards) == 2 and player >=9 and player <= 11:
            # OPTION to double down, if player has money
            if hand.doubleDown():
                self.draw(hand, True)
                return    
        upcard = Hand.getValue(self.dealerHand[0]);
        playTo = Round.basicStrategy(upcard);
        self.drawUntil(hand, playTo)

    def playDealer(self):
        self.dealerHand.unhide()
        self.drawUntil(self.dealerHand, 17)

    def finalise(self):
        dealer = self.dealerHand.getBestValue()
        for hand in self.hands:
            hand.unhide()
            player = hand.getBestValue()
            if player > dealer:
                self.win(hand)
            elif player == dealer:
                self.even(hand)
            else:
                self.fold(hand)

    def placeBets(self, players: List[Player]):
        DEFAULT_BET = 2
        for player in players:
            hand = Hand(player)
            # Only players with enough money can place bets
            if hand.bet(DEFAULT_BET):                
                self.hands.append(hand)

    def activeHands(self) -> int:
        count = 0
        for hand in self.hands:
            if hand.betAmount:
                count += 1
        return count

    def play(self) -> bool:
        if not self.hands:
            return False

        self.deal()       
        self.showStats()

        if self.dealerHand.isBlackJack():
            # fold all hands that don't have black jack
            for hand in self.hands:
                if not hand.isBlackJack():
                    self.fold(hand)
                    self.showStats()

        for hand in self.hands:
            if hand.isBlackJack():
                self.win(hand)
                self.showStats()

        for hand in self.hands:
            if hand.betAmount:
                self.playPlayer(hand);
                if hand.isBust():
                    self.fold(hand)
                    self.showStats()

        if self.activeHands() > 0:
            self.playDealer();
            self.showStats()

        # settle hands
        self.finalise()
        self.showStats()      
        
        return True