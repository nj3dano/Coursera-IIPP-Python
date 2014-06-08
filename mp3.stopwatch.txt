#http://www.codeskulptor.org/#user30_XnFIYlrAXFRCutP.py
##########################################
# template for "Stopwatch: The Game"
# D. Kessler 4/15/14 IIPP Spring 2014
##########################################

import simplegui
import math

##########################################
# define global variables
##########################################

#_debug = True
_debug = False

# count of elapsed time in 0.1 sec interval
elapsed_time_counter = 0

# counters for game attempts and wins
game_attempts = 0
game_wins = 0

##########################################
#  HELPER functions
##########################################

# format function that converts time in
# tenths of seconds into formatted string A:BC.D
def format(t):
    """ WHAT: format time string """
    
    # format and return a string of the form A:BC.D where
    # A, C and D are digits in the range 0-9
    # and B is in the range 0-5 (seconds do not go beyond 59)
    # A = the amount of minutes in that number
    # B = the amount of tens of seconds
    # C = the amount of seconds in excess of tens of seconds
    # D = the amount of the remaining tenths of seconds
   
    # elapsed_time_counter is in tenths of seconds
    total_seconds = t // 10
    remaining_tenths = t % 10
    minutes = total_seconds // 60
    seconds_remaining = total_seconds % 60
    
    A = str(minutes)
    
    if seconds_remaining < 10:
        B = str(0)
        C = str(seconds_remaining)
    else:
        B = str((seconds_remaining / 10 ))
        C = str((seconds_remaining % 10 ))
    
    D = str(remaining_tenths)

    return A + ":" + B + C + "." + D

# construct the string for the game attempts and wins
def format_gamestring():
    """ WHAT: format game Win/Attempts string"""
    gamestring = "Wins/Attempts " + str(game_wins) + "/" + str(game_attempts)
    return gamestring
    
    
##########################################
# EVENT HANDLERS
##########################################

def start_mytimer():
    """ WHAT: Start Button: start the timer """
    timer.start()
    if _debug:
        print "start_mytimer: timer started"

def stop_mytimer():
    """ WHAT: Stop Button: stop the timer, check game results """
    global game_attempts
    global game_wins
    
    if not timer.is_running():
        if _debug:
            print "Stop button pressed, timer was not running"
        return
       
    # timer is running, stop it
    timer.stop()
    
    # increment counter for the game attempts
    game_attempts += 1
    
    # check if you managed to stop the timer on a
    # whole second (1.0, 2.0, 3.0, etc.),l if so count a win
    if elapsed_time_counter % 10 == 0:
        game_wins += 1
        
    if _debug:
        if elapsed_time_counter % 10 == 0:
            print "stop_mytimer: won elapsed_time_counter ", elapsed_time_counter
        else:
            print "stop_mytimer: lost elapsed_time_counter ", elapsed_time_counter

def reset_mytimer():
    """ WHAT: Reset Button: start over """
    global elapsed_time_counter
    global game_attempts
    global game_wins
    
    if timer.is_running():
        timer.stop()
    
    elapsed_time_counter = 0
    game_attempts = 0
    game_wins = 0
    
    if _debug:
        print "reset_mytimer: reset all variables to 0"
 
# define event handler for timer with 0.1 sec interval
# should change global states, but not draw
def tick():
    """ WHAT: handle timer going off """
    global elapsed_time_counter
    elapsed_time_counter +=1
    
# define draw handler to draw on canvas
# should only draw, not perform logic
def draw(canvas):
    """ WHAT: draw the canvas """
    canvas.draw_text(format_gamestring(),[70, 30], 24, "Red")
    canvas.draw_text(format(elapsed_time_counter),[position_width, position_height], 48, "Red")
    #canvas.draw_circle([150, 150], 100, 6, "Red" )
    
##########################################
# create frame
##########################################
frame = simplegui.create_frame("Stop Watch", 300, 300)

# for width 300/2 or 150 is the midpoint, go to midpoint
# then back up by one half of the text width size
position_width = (300 / 2) - ((frame.get_canvas_textwidth("0:00.0", 48)) / 2)
position_height = (300 / 2) + 12

if _debug:
    print "canvas text width alone is ", frame.get_canvas_textwidth("0:00.0", 48)
    print "canvas midpoint width is ", position_width
    print "canvas midpoint height is ", position_height

##########################################
# register event handlers
##########################################

# buttons
frame.add_button("Start", start_mytimer, 100)
frame.add_button("Stop",  stop_mytimer,  100)
frame.add_button("Reset", reset_mytimer, 100)

# draw
frame.set_draw_handler(draw)

# timer: timer interval in miliseconds
# requirement is .1 seconds, which is 100 miliseconds
timer = simplegui.create_timer(100, tick)

##########################################
# start frame
##########################################
frame.start()


# Please remember to review the grading rubric
