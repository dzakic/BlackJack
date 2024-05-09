from tkinter import *
from bjack import BlackJack
from hand import Hand
from enum import Enum

FONT = "Segoe UI"
HAND_FONT_SIZE = 20
BGCOL = "light sea green" # SkyBlue3
class Stage(Enum):
    VIEWING = 0
    PLACING_BETS = 1
    PLAYING = 2

class BlackJackWindow(Tk):

    game: BlackJack
    stage: Stage

    def __init__(self, game: BlackJack):
        Tk.__init__(self)
        self.game = game
        self.playerFrames = []

        # Layout    
        self.title("Black Jack")
        self.config(bg="skyblue")
        self.geometry("800x400")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        self.bind('<Escape>', self.cancel)
        
        Label(self, text="Black Jack",font=("Perpetua", 32), background="deepskyblue2").pack(side = TOP, fill = X)
        
        left = Frame(self, background = "SkyBlue3", width = 150)
        left.pack(side = LEFT, fill = Y, padx = 5, pady = 5)        
        left.pack_propagate(False) 

        for player in self.game.players:
            frame = Frame(left, height = 75, background = "SkyBlue2", borderwidth = 10)
            frame.pack(side = BOTTOM, fill = X, pady = 2, padx = 2)
            frame.pack_propagate(False) 
            frame.player = player
            frame.playerMoney = Label(frame, font = (FONT, 12), background = "SkyBlue3")
            frame.playerMoney.pack(side = BOTTOM, fill = X, padx = 5)
            frame.playerName = Label(frame, font = (FONT, 14), background = "SkyBlue2")
            frame.playerName.pack(side = BOTTOM, fill = X, padx = 5)
            self.playerFrames.append(frame)

        right = Frame(self, background = "SkyBlue3", width = 150)
        right.pack(side = RIGHT, fill = Y, padx = 5, pady = 5)
        right.pack_propagate(False) 

        middle = Frame(self, background = BGCOL)
        middle.pack(fill = BOTH, expand = True, pady = 5)
        middle.pack_propagate(False) 

        self.dealerHand = Label(middle, height = 2, font = (FONT, HAND_FONT_SIZE), background="sea green")
        self.dealerHand.pack(side = TOP, fill = X)

        dealerStatus = Frame(middle, background = BGCOL)
        dealerStatus.pack(side = TOP, fill = X)      
        self.dealerValue = Label(dealerStatus, width = 4, background=BGCOL, font = ("Serif", 12), foreground="white")
        self.dealerValue.pack(side = RIGHT)

        self.playerHand = Label(middle, height = 2, font = (FONT, HAND_FONT_SIZE), background="forest green")
        self.playerHand.pack(side = BOTTOM, fill = X)

        playStatus = Frame(middle, background = BGCOL)
        playStatus.pack(side = BOTTOM, fill = X)        
        self.handBet = Label(playStatus, font = (FONT, 16), background=BGCOL)
        self.handBet.pack(side = LEFT)
        self.handValue = Label(playStatus, width = 4, background=BGCOL, font = (FONT, 12), foreground="white")
        self.handValue.pack(side = RIGHT)       
        self.currentPlayer = Label(playStatus, font = (FONT, 16), background=BGCOL)
        self.currentPlayer.pack()

        self.banner = Label(middle, font = (FONT, 28), background=BGCOL, foreground="greenyellow")
        self.banner.pack(side = BOTTOM, fill = X, pady = 40)

        # Buttons
        self.btnContinue = Button(right, text = "Stand", command = self.advance, default = "active", font = (FONT, 12))
        self.btnContinue.pack(side = BOTTOM, fill = X, padx = 5, pady = 5)
        self.bind("<Return>", self.advance)

        self.btnHit = Button(right, text = "Hit", command = self.hit, font = (FONT, 12))
        self.btnHit.pack(side = BOTTOM, fill = X, padx = 5, pady = 2)
        self.bind("<plus>", self.hit)

        self.btnDouble = Button(right, text = "Double", command = self.double, font = (FONT, 12))
        self.btnDouble.pack(side = BOTTOM, fill = X, padx = 5, pady = 2)
        self.bind("<Home>", self.double)

        self.btnSplit = Button(right, text = "Split", command = self.split, font = (FONT, 12))
        self.btnSplit.pack(side = BOTTOM, fill = X, padx = 5, pady = 2)
        self.bind("<End>", self.split)
        
    def updateBoard(self):
        self.dealerHand.config(text = self.game.dealerHand)
        self.playerHand.config(text = self.game.playerHand())

        for frame in self.playerFrames:
            frame.config(background = "sea green" if frame.player == self.game.playerHand().player else "SkyBlue3")
            frame.playerName.config(text = frame.player.name)
            frame.playerMoney.config(text = f"${frame.player.money}")
            frame.config()

        self.currentPlayer.config(text = self.game.playerHand().player.name)
        self.handBet.config(text = f"${self.game.playerHand().betAmount}")

        if self.stage == Stage.PLACING_BETS:
            self.banner.config(text = "Place bets")
            self.btnHit.config(text = "Increase")
            self.btnContinue.config(text = "Deal")
            self.dealerValue.config(text = "")
            self.handValue.config(text = "")
            self.btnHit.pack(side = BOTTOM, fill = X, padx = 5, pady = 2)
            self.btnDouble.pack_forget()
            self.btnSplit.pack_forget()

        if self.stage == Stage.PLAYING:
            self.handValue.config(text = self.game.playerHand().getValue())
            self.btnHit.pack(side = BOTTOM, fill = X, padx = 5, pady = 2)
            self.btnDouble.pack(side = BOTTOM, fill = X, padx = 5, pady = 2)
            if self.game.playerHand().isSplittable():
                self.btnSplit.pack(side = BOTTOM, fill = X, padx = 5, pady = 2)
            else:
                self.btnSplit.pack_forget()
            self.btnHit["text"] = "Hit"
            self.banner["text"] = ""
            self.btnContinue["text"] = "Stand"
    
        if self.stage == Stage.VIEWING:
            self.handValue.config(text = self.game.playerHand().getValue())
            self.dealerValue.config(text = self.game.dealerHand.getValue() if self.game.dealerHand.public() else "")
            self.btnSplit.pack_forget()
            self.btnDouble.pack_forget()
            self.btnHit.pack_forget()
            match self.game.playerHand().result:
                case Hand.Status.WIN:
                    self.banner["text"] = "Win!"
                case Hand.Status.LOSE:
                    self.banner["text"] = "Lose"
                case Hand.Status.EVEN:
                    self.banner["text"] = "Even"
            self.btnContinue["text"] = "Continue"

        if self.stage == Stage.PLAYING:
            self.banner.pack_forget()
        else:
            self.banner.pack(side = BOTTOM, fill = BOTH, pady = 40)

    def cancel(self, event):
        self.quit()

    def hit(self, event = None):
        playerHand = self.game.playerHand()
        match self.stage:
            case Stage.PLACING_BETS:
                playerHand.bet(BlackJack.DEFAULT_BET)
            case Stage.PLAYING:
                self.game.draw(playerHand)
                #if playerHand.isBlackJack() or playerHand.isBust():
                #    self.advance()
        self.updateBoard()

    def double(self, event = None):
        playerHand = self.game.playerHand()
        playerHand.bet(playerHand.betAmount)
        self.game.draw(playerHand)
        self.advance()

    def split(self, event = None):
        playerHand = self.game.playerHand()
        self.game.split(playerHand)
        self.updateBoard()

    # go to next stage
    def advance(self, event = None):      
        match self.stage:
            case Stage.PLACING_BETS:
                if not self.game.nextHand(False):
                    self.game.current_hands = 0
                    # 2a. Deal Cards
                    self.game.deal()                
                    self.stage = Stage.PLAYING
                    if not self.game.playerHand().isPlaying():
                        self.advance()
            case Stage.PLAYING:
                # if no more hands, dealer plays and settles/reveals all hands            
                if not self.game.nextHand(True):
                    # 3a. Dealer plays
                    self.game.playDealer();
                    # 3b Settle hands
                    self.game.finalise()
                    self.game.current_hands = 0
                    self.stage = Stage.VIEWING
            case Stage.VIEWING:
                # finished viewing
                if self.game.playerHand():
                    self.game.settle(self.game.playerHand())
                if self.game.nextHand(False):
                    if self.game.playerHand():
                        if self.game.playerHand().isPlaying():
                            self.stage = Stage.PLAYING
                else:
                    self.stage = Stage.PLACING_BETS
                    # 1a. Init Bets
                    self.game.initRound()
                    self.game.placeBets()

        self.updateBoard()

    def play(self):
        self.stage = Stage.VIEWING
        self.advance()
        self.mainloop()
