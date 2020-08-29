#http://www.codeskulptor.org/#user31_s6XJfgGI0XOaVkf_0.py
##########################################
# implementation of card game - Memory
# D. Kessler 5/1/14 IIPP Spring 2014
##########################################

import simplegui
import random

##########################################
# define global variables
##########################################

#_debug = True
_debug = False

# state of the game
state = 0
last_exposed = 0
nexttolast_exposed = 0

# deck and turns in a game
deck = range(8) + range(8)
turns = 0

# 16 cards, canvas is 800x100
CARDHEIGHT = 100
CARDWIDTH = int(800 / 16)
exposed_card_position = []
unexposed_card_position = []
line_position = []

# Concatenation of Copies of one Sequence
# Returns the concatenation of n copies of False
exposed = [False] * 16

##########################################
#  HELPER functions
##########################################

def initialize():
    """ WHAT: Set STATIC nonchanging data """
    global exposed_card_position, unexposed_card_position, line_position
    
    for i in range( len(deck) ):
        # EXPOSED CARDS: positions to print card numbers if card is exposed
        # subtract 2 pixels to paint the lines for width
        # add 16 to height as you add half the height to the center
        # will be drawn with draw_text, takes one point
        tocenter_height = (CARDHEIGHT / 2) + 16
        tocenter_width  = (CARDWIDTH / 2) - ((frame.get_canvas_textwidth("0", 48)) / 2)
        tocenter_width -= 2
        exposed_card_position.append([(CARDWIDTH * i) + tocenter_width, tocenter_height])
        
        # NON EXPOSED: positions to print back of the card if card is not exposed
        # start at  middle of first card, down the center the width of the card
        # will be drawn with draw_line, takes two points
        unexposed_card_position.append([[(CARDWIDTH * i) + (CARDWIDTH / 2), 0],
                                        [(CARDWIDTH * i) + (CARDWIDTH / 2), CARDHEIGHT]] )
    
        # LINES: position of the lines, draw one less line than cards
        #for i in range( len(deck) - 1 ):
        line_position.append([[(CARDWIDTH * i) + CARDWIDTH, 0],
                              [(CARDWIDTH * i) + CARDWIDTH, CARDHEIGHT]] )
    if _debug:
        print "deck is", deck
        print "length of the deck is", len(deck)
        print "canvas text width alone is ", frame.get_canvas_textwidth("0", 48)
        print "canvas tocenter width is ", tocenter_width
        print "canvas tocenter height is ", tocenter_height
        print "exposed_card_position is", exposed_card_position
        print "unexposed_card_position is", unexposed_card_position
        print "line_position is", line_position
        print "exposed is", exposed
        
def new_game():
    """ WHAT: initialize for a new game """
    
    global state, turns
    global last_exposed, nexttolast_exposed, exposed
            
    state = 0
    turns = 0
    last_exposed = 0
    nexttolast_exposed = 0
    exposed = [False] * 16
    
    # shuffle the deck, all not exposed
    random.shuffle(deck)
    
    if _debug:
        print "deck is", deck
    
##########################################
# EVENT HANDLERS
##########################################

def mouseclick(pos):
    global state, turns
    global last_exposed, nexttolast_exposed, exposed
    
    card_position = pos[0] // 50
        
    # if card is already exposed, nothing more to do
    if exposed[card_position]:
        return
 
    # expose the card currently selected
    exposed[card_position] = True;

    if _debug:
        print "on Turn", turns, "card selected is at index", card_position
        print "state is ", state
        print "last_exposed is ", last_exposed
        print "nexttolast_exposed is ", nexttolast_exposed
        
    # increment turns after the FIRST card is selected for a new turn
    if state == 0 or state == 2:
        turns += 1
    
    # if it is the END OF the last turn
    if state == 2:
        if deck[nexttolast_exposed] != deck[last_exposed]:
            exposed[nexttolast_exposed] = exposed[last_exposed] = False
    
    # uppdate state for the next mouse click
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
    else:
        state = 1
   
    # update last and next to last selected
    nexttolast_exposed = last_exposed
    last_exposed = card_position
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
       
    # paint the cards
    for i in range( len(deck) ):
       if exposed[i]:
            canvas.draw_text( str(deck[i]), exposed_card_position[i], 48, 'White' )
       else:
            canvas.draw_line( unexposed_card_position[i][0],
                              unexposed_card_position[i][1], CARDWIDTH, "Green" )
        
    # paint the lines, one less line than the number of cards
    for i in range( (len(deck) - 1) ):
        canvas.draw_line( line_position[i][0], line_position[i][1], 1, "Silver" )
           
    # update the number of turns
    label.set_text("Turns = " + str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
initialize()
new_game()
frame.start()


# Always remember to review the grading rubric