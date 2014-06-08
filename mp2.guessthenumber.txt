# http://www.codeskulptor.org/#user29_cUrIQR0Yphy6cP9.py
# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
#
# D. Kessler IIPP Spring 2014
##########################################################

import random
import math
import simplegui

#################################################
# initialize global variables
#################################################

# defaults
secret_number = 0
attempts = 7

# default the range
low = 0
high = 100

#################################################
# helper functions 
#################################################

# clear the input box   
def clear_input_box():
    """ WHAT: This function clears the text input field. """
    input_box.set_text("");

    
# to start or restart a new game
def new_game():
    """ WHAT: compute random secret number, assign to global """
    
    global secret_number
    global attempts
    
    # read only for these range limits
    #global low, high
    
    # set maximum number of attempts based on high and low
    attempts = int(math.ceil(math.log(high, 2)))
    
    # generate a different secret_number
    secret_number = random.randrange(low, high)
    
    # inform player game is starting and range to pick from
    print "\nGuess the Number, you have %s guesses" % attempts
    print "Pick a number between [%s - %s)" % (low, high)
    
    # clear out the input box
    clear_input_box()
    
    # FOR DEBUG
    #print "new_game, low is", low, "high is", high
    #print "new_game attempts_taken is reset to,", attempts_taken
    #print "new_game attempts_allowed is set to,", attempts_allowed
    #print "new_game: secret_number is:", secret_number
    

#################################################
# define event handlers for control panel
#################################################

# button press for range 0 - 100
def range100():
    """ WHAT: BUTTON HANDLER: make range 0 to 100 and restart """
    global low, high
    low = 0
    high = 100
    new_game()
    
# button press for range 0-1000
def range1000():
    """ WHAT: BUTTON HANDLER: make range 0 to 1000 and restart """
    global low, high
    low = 0
    high = 1000
    new_game()

# input control edit box to enter the guess
def input_guess(guess):
        
    # decrement counter
    global attempts
    attempts -= 1
    
    # is the game won on this guess, default to no
    game_won = "no"
    
    # validate, maybe user entered abc for example
    if not guess.isdigit():
        print guess + " is not a valid number. " \
              "You may guess %s more times." % attempts
    elif int(guess) < secret_number:
        print guess + " is incorrect, guess HIGHER. " \
              "You may guess %s more times." % attempts
    elif int(guess) > secret_number:
        print guess + " is incorrect, guess LOWER. " \
              "You may guess %s more times." % attempts
    else:
        game_won = "yes"
        print guess + " is CORRECT! " \
              "Secret number " + str(secret_number)    
   
    # SUCCESS ?
    if game_won == "yes":
        new_game()
        return "success"
   
    # FAILURE ? Out of attempts ?
    if attempts == 0:
        print "You are out of attempts, you lose. " + \
              "The secret number was:", secret_number
        new_game()
        return "failure"
            
    # you get another guess
    clear_input_box()
    return "continuing"
    

#################################################    
# create frame
#################################################
frame = simplegui.create_frame("Guess the number", 300, 300)

#################################################
# register event handlers for control elements
#################################################
input_box = frame.add_input("Guess the number", input_guess, 200)
frame.add_button("Range: 0 - 100", range100)