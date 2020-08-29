#http://www.codeskulptor.org/#user29_J0tWyOWnXmh8y8G_2.py
###################################################
# Rock-paper-scissors-lizard-Spock template
# D. Kessler 4/1/14 IIPP Spring 2014
###################################################

import random

###################################################
# help function name_to_number
###################################################
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
###################################################
def name_to_number(name):
    """ WHAT: convert name to number """
   
    # convert name to number using if/elif/else
    # don't forget to return the result!
    # input will be one of 5 valid values
    
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "name_to_number: invalid input entered:", name
        return -1
   
###################################################
# help function number_to_name
###################################################
def number_to_name(number):
    """ WHAT: convert number to name """
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    # input will be one of 5 valid values
    
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "number_to_name: invalid input entered:", number
        return "None"
   
    
###################################################
# function rpsls
###################################################
def rpsls(player_choice): 
    """ WHAT: play the rpsls game and print the winner"""
    
    # print a blank line to separate consecutive games
    print ""

    # print out the message for the player's choice
    # do not use string concatenation to print here because
    # you have not yet verified input is in fact type string
    print "Player chooses", player_choice

    # convert the player's choice to player_number using the function name_to_number()
    # check for an invalid return code
    player_number = name_to_number( player_choice )
    if player_number == -1:
        return "False"

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange( 0, 5 )
   
    # convert comp_number to comp_choice using the function number_to_name()
    # check for an invalid return code
    comp_choice = number_to_name( comp_number )
    if comp_choice == "None":
        return "False"
    
    # print out the message for computer's choice
    print "Computer chooses " + comp_choice

    # compute difference of comp_number and player_number modulo five
    myResult = ( player_number - comp_number ) % 5
        
    # use if/elif/else to determine winner, print winner message
    if 1 <= myResult <= 2:
        print "Player wins!"
    elif 3 <= myResult <= 4:
        print "Computer wins!"
    elif myResult == 0:
        print "Player and computer tie!"
    else:
        print "rpsls: Invalid result:", myResult
        return "False"
    
    return "TRUE"
    
    
###########################################################
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
###########################################################
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# test invalid input by Player
#rpsls("test")
#rpsls(-1)

# always remember to check your completed program against the grading rubric


