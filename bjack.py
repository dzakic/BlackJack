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
        
    def addPlayer(self, name: str, money: float):
        player = Player(name, money)
        self.players.append(player)

    def initRound(self):
        ## init round
        self.dealerHand = Hand(self.dealer)
        self.hands = []

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
        newHand.add(card);
        self.hands.append(newHand)
        self.draw(hand)
        self.draw(newHand)

    def playerHand(self) -> Hand:
        # TODO: Cycle through all hands
        current_hands = 0   
        return self.hands[current_hands]    

    # Fold hands, bet lost
    def lose(self, hand: Hand):
        # Dealer takes the bet
        self.dealerHand.player.money += hand.betAmount;
        hand.result = Hand.Status.LOSE
        hand.clear()

    # Hands won the bet
    def win(self, hand: Hand):
        # natural win is half the bet
        if len(hand.cards) == 2 and hand.isBlackJack():
            winamount = hand.betAmount // 2
        else:
            winamount = hand.betAmount
        # Dealer pays the winamount
        self.dealerHand.player.money -= winamount;
        # Player pockets original bet, plus dealer's payment
        hand.player.money += hand.betAmount + winamount
        hand.result = Hand.Status.WIN
        hand.clear()

    # Equal to dealer, noone wins
    def even(self, hand: Hand):
        # Return money to player
        hand.player.money += hand.betAmount;
        hand.result = Hand.Status.EVEN
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
                self.win(hand)
            elif player == dealer:
                self.even(hand)
            else:
                self.lose(hand)

    def activeHands(self) -> int:
        count = 0
        for hand in self.hands:
            if hand.betAmount:
                count += 1
        return count
    
    # ------------------------------------------#
    # -- --- Only needed for CONSOLE PLAY --- --#

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

        player = hand.getValue()
        if len(hand.cards) == 2 and player >=9 and player <= 11:
            # OPTION to double down, if player has money
            if hand.doubleDown():
                self.draw(hand, True)
                return    
        upcard = Hand.getValue(self.dealerHand[0]);
        playTo = BlackJack.basicStrategy(upcard);
        self.drawUntil(hand, playTo)

    def showStats(self):
        print("===")
        self.dealerHand.dump()
        for hand in self.hands:
            hand.dump()
       
    def showPlayers(self, count: int):
        print("====== Game #", count, "  Deck: ", len(self.deck.cards))
        print(self.dealer)
        for player in self.players:
            print(player)

    def playRound(self) -> bool:
        
        self.placeBets()

        if not self.hands:
            return False

        self.deal()       
        self.showStats()

        if self.dealerHand.isBlackJack():
            self.dealerHand.unhide()
            # all non black jack hands lose
            
            for hand in self.hands:
                if not hand.isBlackJack():
                    self.lose(hand)
                    self.showStats()

        for hand in self.hands:
            if hand.isBlackJack():
                self.win(hand)
                self.showStats()

        for hand in self.hands:
            if hand.betAmount:
                self.playPlayer(hand);

        if self.activeHands() > 0:
            self.playDealer();
            self.showStats()

        # settle hands
        self.finalise()
        self.showStats()
        return True
        
    def play(self):
        count = 0       
        while True:
            count += 1
            if self.playRound():
                self.showStats(count)
            else:
                return
