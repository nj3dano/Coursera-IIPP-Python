#http://www.codeskulptor.org/#user31_1AaGrSUoAf_3.py
########################################################
# Mini-project #6 - Blackjack
# D. Kessler IIPP Spring 2014
########################################################

import simplegui
import random

#_debug = True
_debug = False

#_debug2 = True
_debug2 = False

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
dealer_status = ""
score = 0

########################################################
# define globals for cards
########################################################
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

########################################################
# define card class
########################################################
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

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

########################################################        
# define hand class
########################################################
class Hand:
    def __init__(self):
        """ WHAT: create Hand object, has an empty list of cards """
        self.hand = []
        self.has_ace = False
        
    def __str__(self):
        """ WHAT: return a string representation of a hand
            call the str for each card using list comprehension """
        return( "Hand contains " + \
                (' '.join([str(card) for card in self.hand])) )
      
    def add_card(self, card):
        """ WHAT add a card object to a hand """
        self.hand.append(card)
        
        # is this card an ace ?, if so indicate Hand has an ace
        if card.get_rank() == 'A':
            self.has_ace = True

    def get_value(self):
        """ WHAT: compute the value of a hand """
        
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for cardobject in self.hand:
            value += VALUES[cardobject.get_rank()]
        
        if self.has_ace and (value + 10) <= 21:
            value += 10
        
        return value  
            
    def draw(self, canvas, pos):
        """ WHAT: draw a hand on the canvas, use the draw method for cards """
        for cardobject in self.hand:
            cardobject.draw( canvas, pos )
            pos[0] += (CARD_SIZE[0] + 12) # move x size of a card and white space
 
########################################################        
# define deck class
########################################################
class Deck:
    def __init__(self):
        """ WHAT: create Deck object, has an list of 52 cards """
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        
        if _debug:
            print str(self)
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal_card(self):
        # deal (remove) a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
       # return a string representing the deck
       return( "Deck contains " + \
                (' '.join([str(card) for card in self.deck])) )


########################################################
#define event handlers for buttons
########################################################
def deal():
    global outcome, dealer_status, score, in_play
    global dealerHand, playerHand, myDeck
    
    forfeit = False
    
    # if a game is already in play, forfeit the game
    if in_play:
        score -= 1
        forfeit = True
    
    # create and shuffle the deck
    myDeck = Deck()
    myDeck.shuffle()

    # create a hand for the dealer and the player
    dealerHand = Hand()
    playerHand = Hand()
    
    # deal 2 cards alternating to player, then dealer
    playerHand.add_card(myDeck.deal_card())
    dealerHand.add_card(myDeck.deal_card())
    playerHand.add_card(myDeck.deal_card())
    dealerHand.add_card(myDeck.deal_card())
    
    if _debug:
        print "Player", playerHand
        print "Dealer", dealerHand
  
    # global values
    dealer_status = "Game underway"
    outcome = "You have " + str(playerHand.get_value()) + ". Hit or stand ?"
    in_play = True
    
    if forfeit:
         dealer_status += ", last game was a forfeit"

def hit():
    """ WHAT: If PLAYER hand is <= 21, add card, otherwise, bust """
    global playerHand, myDeck
    global outcome, dealer_status, score, in_play
    
    # is the hand in play
    if not in_play:
        outcome = "Cannot hit no game in play, new deal?"
        return

    # HIT: player
    playerHand.add_card(myDeck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    # don't want to check if player has 21 here, if dealer also
    # has 21, then dealer wins, since dealer wins ties
    if playerHand.get_value() > 21:
        outcome = "Busted with " + str(playerHand.get_value()) + " you lose"
        dealer_status = "Game over, new deal?"
        score -= 1
        in_play = False
    else:
        outcome = "You have " + str(playerHand.get_value()) + ". Hit or stand ?"
        in_play = True      
       
def stand():
    """ WHAT: Player chooses to stand """
    global playerHand, dealerHand, myDeck
    global outcome, dealer_status, score, in_play
    
    # is hand in play 
    if not in_play:
        outcome = "Cannot stand no game in play, new deal?"
        return

    # HIT: repeatedly hit DEALER until hand has value 17 or more
    while dealerHand.get_value() < 17:
        dealerHand.add_card(myDeck.deal_card())
            
    # STAND: game is over, who won ?
    dealer_value = dealerHand.get_value()
    player_value = playerHand.get_value()
    
    if _debug:
        print "dealer_value is", dealer_value
        print "player_value is", player_value
        
    # what is the outcome
    if dealer_value > 21:
        outcome = "You win, Dealer is busted with " + str(dealer_value)
        score += 1
    elif dealer_value == 21:
        outcome = "You lose, Dealer has blackjack!"
        score -= 1
    elif player_value == 21:
        outcome = "You win, you have blackjack!"
        score += 1
    elif player_value == dealer_value:
        outcome = "Game tied with " + str(player_value) + " you lose."
        score -= 1
    elif player_value > dealer_value:
        outcome = "You win with " + str(player_value) + ". Dealer has " + str(dealer_value)
        score += 1
    else:
        outcome = "You lose with " + str(player_value) + ". Dealer has " + str(dealer_value)
        score -= 1
   
    # assign a message to outcome, update in_play and score
    in_play = False
    dealer_status = "Game Over, new deal?"

# draw handler    
def draw(canvas):
    canvas.draw_text( "BLACKJACK", [20,100], 32, 'Aqua' )
    canvas.draw_text( ("Score: " + str(score)), [320,100], 32, 'Black' )
    canvas.draw_text( "Dealer:", [20,180], 32, 'Black' )
    canvas.draw_text( dealer_status, [140, 180], 28, 'Black' )
    canvas.draw_text( "Player:", [20, 380], 32, 'Black' )
    canvas.draw_text( outcome, [140, 380], 28, 'Black' )
    
    # draw the card images
    dealerHand.draw(canvas, [20, 200])
    playerHand.draw(canvas, [20, 400])
    
    # hide the dealer hole card if a game is in play   
    if in_play:
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])       
        canvas.draw_image( card_back, card_loc, CARD_BACK_SIZE,
                           [20  + CARD_BACK_CENTER[0],
                           200 + CARD_BACK_CENTER[1]],
                           CARD_BACK_SIZE )
    if _debug2:
        card = Card("S", "A")
        card.draw(canvas, [300, 400])

########################################################
# initialization frame
########################################################
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

if _debug2:
    mydeck = Deck()
    print mydeck

    c1 = Card("S", "2")
    c2 = Card("C", "A")
    c3 = Card("H", "T")
    print c1, c2, c3
    dealerHand.add_card(c1)
    dealerHand.add_card(c2)
    dealerHand.add_card(c3)
    print dealerHand.get_value()
    print dealerHand
      
    bc1 = Card("S", "A")
    bc2 = Card("D", "A")
    bc3 = Card("H", "9")
    playerHand.add_card(bc1)
    playerHand.add_card(bc2)
    playerHand.add_card(bc3)
    print playerHand.get_value()
    print playerHand
    
    ac1 = Card("S", "A")
    ac2 = Card("C", "A")
    ac3 = Card("H", "A")
    ac4 = Card("C", "5")
    testHand3 = Hand()
    testHand3.add_card(ac1)
    testHand3.add_card(ac2)
    testHand3.add_card(ac3)
    testHand3.add_card(ac4)
    print testHand3.get_value()
    print testHand3
    
# remember to review the gradic rubric