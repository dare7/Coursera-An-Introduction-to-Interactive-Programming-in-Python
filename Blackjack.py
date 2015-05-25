# Mini-project #6 - Blackjack
__author__ = 'dare7'
# for development in external local IDE and to be complied with Codeskulptor at the same time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True

import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck_play = []
player_hand = []
dealer_hand = []
funds = 10000
casino = 10000
bet = 1000
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
# define strings
WIN = ("Good job!", "Lucky you!", "Counting, eh?")
LOST = ("Maybe next time!", "Oops!", "Just bad luck!")

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.list = []

    def __str__(self):
        # return a string representation of a hand
        card_list = "Hand contains "
        for i in range(len(self.list)):
            card_list += str(self.list[i]) + " "
        return card_list

    def add_card(self, card):
        # add a card object to a hand
        self.list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        total = 0
        for c in self.list:
            value = VALUES[c.get_rank()]
            total += value
        if "A" in str(self) and (total + 10) <= 21:
            total += 10
        return total
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for c in self.list:
            c.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.list = []
        for suit in SUITS:
            for rank in RANKS:
                cards = Card(suit, rank)
                self.list.append(cards)

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.list)
        pass    # use random.shuffle()

    def deal_card(self):
        # deal a card object from the deck
        out = self.list[random.randrange(len(self.list)-1)]
        self.list.remove(out)
        return out
    
    def __str__(self):
        # return a string representing the deck
        card_list = "Deck contains "
        for i in range(len(self.list)):
            card_list += str(self.list[i]) + " "
        return card_list

# define event handlers for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, deck_play, funds, bet, casino
    deck_play = Deck()
    deck_play.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        player_hand.add_card(deck_play.deal_card())
        dealer_hand.add_card(deck_play.deal_card())
    #print("player: %s" % player_hand)
    #print("dealer: %s" % dealer_hand)
    outcome = "Hit or stand??"
    if in_play:
        funds -= bet
        casino += bet
        label2.set_text("System info: %s" % random.choice(LOST))
    in_play = True


def hit():
    global outcome, in_play, player_hand, deck_play, funds, bet, casino, label2
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck_play.deal_card())

        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "Busted! You lost 1000$"
            funds -= bet
            casino += bet
            in_play = False
            label2.set_text("System info: %s" % random.choice(LOST))
    else:
        outcome = "New deal?"
    #print(player_hand)
    #print(outcome)
    #print(player_hand.get_value())

       
def stand():
    global outcome, in_play, dealer_hand, player_hand, deck_play, casino, funds, label2
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(deck_play.deal_card())

    # assign a message to outcome, update in_play and score
        if (dealer_hand.get_value() >= player_hand.get_value()) and (dealer_hand.get_value() <= 21):
            outcome = "You lost 1000$ New deal?"
            casino += bet
            funds -= bet
            in_play = False
            label2.set_text("System info: %s" % random.choice(LOST))
        else:
            outcome = "You won 1000$! New deal?"
            casino -= bet
            funds += bet
            in_play = False
            label2.set_text("System info: %s" % random.choice(WIN))
    else:
        outcome = "New deal?"
    #print(dealer_hand)
    #print(outcome)
    #print(dealer_hand.get_value())


# draw handler    
def draw(canvas):
    global outcome, in_play
    player_hand.draw(canvas, [10,10])
    dealer_hand.draw(canvas, [150,150])
    CARD_BACK_SIZE = (72, 96)
    CARD_BACK_CENTER = (36, 48)
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [150 + CARD_BACK_SIZE[0]/2,150 + CARD_BACK_SIZE[1]/2], CARD_BACK_SIZE)
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    canvas.draw_text(outcome, (30, 600-30), 30, 'White', 'monospace')
    canvas.draw_text("Casino balance: %s$" % str(casino), (30, 600-130), 30, 'White', 'monospace')
    canvas.draw_text("Your balance: %s$" % str(funds), (30, 600-80), 30, 'White', 'monospace')
    canvas.draw_text("Blacjack!", (30, 350), 60, 'White', 'monospace')
    if funds <= 0:
        outcome = "You lost! Try to recoup!"
        in_play = False
    elif casino <= 0:
        outcome = "Jackpot! Reset for more money!"
        in_play = False


# monymaker function
def money():
    global funds, outcome, casino
    funds = 10000
    casino = 10000
    outcome = "10k$ deducted from bank account"


# frame initialization
def init():
    # initialization frame
    global label2
    frame = simplegui.create_frame("Blackjack, by dare7", 600, 600)
    frame.set_canvas_background("Black")

    #create buttons and canvas callback
    frame.add_button("Deal", deal, 200)
    frame.add_button("Hit",  hit, 200)
    frame.add_button("Stand", stand, 200)
    frame.add_button("Reset funds", money, 200)
    frame.add_button("Quit", frame.stop, 200)
    frame.add_label("Each bet is %s$" % str(bet))
    label2 = frame.add_label("System info: Welcome!")
    frame.set_draw_handler(draw)


    # get things rolling
    deal()
    frame.start()


if __name__ == '__main__':
    # for future import as module usage
    init()