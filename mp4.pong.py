#http://www.codeskulptor.org/#user30_xhbbhxtjdn_3.py
##############################################
# Implementation of classic arcade game Pong
# D. Kessler IIPP 4/21/14, IIPP Spring 2014
##############################################

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# ball position, middle of table; and velocity
# these are lists, expressed as x,y
ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]
ball_vel = [0, 0]

# paddles, start in the middle of the gutter:
paddle1_pos = int(HEIGHT / 2)  # LEFT paddle
paddle2_pos = int(HEIGHT / 2)  # RIGHT paddle
paddle1_vel = paddle2_vel = 0

# these are integers, score 1 left, score 2 right
score1 = score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # place the ball in the middle of the screen
    ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]
    
    # give randon velocity, test use ball_vel = [2, 2]
    # suggestion was pixels per second, so divide by 60
    ball_vel = [random.randrange(120, 240) / 60, random.randrange(60, 180) / 60]
        
    # true is RIGHT, starting in center, decrease y to go right and up
    # else LEFT decrease both x and y to go left and up
    if (direction):  
        ball_vel[1] = -ball_vel[1]
    else:
        ball_vel[0] = -ball_vel[0]
        ball_vel[1] = -ball_vel[1]
   
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    
    # reset scores
    score1 = score2 = 0
    
    # keep track of the center of the paddle
    paddle1_pos = int(HEIGHT / 2) # LEFT
    paddle2_pos = int(HEIGHT / 2) # RIGHT
    paddle1_vel = paddle2_vel = 0
    
    spawn_ball( RIGHT )
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # did the ball hit the left gutter or left paddle
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        # is the ball y position in the paddle vertical range ?
        if (paddle1_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT):
            # # hit the left paddle, reflect the ball and increase velocity by 10%
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.10
            ball_vel[1] *= 1.10
        else:
            score2 += 1 # hit the left gutter
            spawn_ball( RIGHT )
        
    # did the ball hit the right gutter or right paddle
    if ball_pos[0] >= (WIDTH - 1) - (BALL_RADIUS + PAD_WIDTH):
        # is the ball y position in the paddle vertical range ?
        if (paddle2_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT):
            # hit the right paddle, reflect the ball and increase velocity by 10%
            ball_vel[0] =- ball_vel[0]
            ball_vel[0] *= 1.10
            ball_vel[1] *= 1.10
        else:  
            score1 += 1 # hit the right gutter
            spawn_ball( LEFT )
    
    # did the ball hit the bottom
    if ball_pos[1] >= ((HEIGHT - 1) - BALL_RADIUS):
         ball_vel[1] = -ball_vel[1]
        
    # did the ball hit the top
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update left paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) >= HALF_PAD_HEIGHT: # top
        if (paddle1_pos + paddle1_vel) <= (HEIGHT - HALF_PAD_HEIGHT): # bottom
            paddle1_pos += paddle1_vel # move is allowed
            
    # update right paddle's vertical position, keep paddle on the screen
    if (paddle2_pos + paddle2_vel) >= HALF_PAD_HEIGHT:
        if (paddle2_pos + paddle2_vel) <= (HEIGHT - HALF_PAD_HEIGHT):
            paddle2_pos += paddle2_vel # move is allowed
        
    # draw paddles: For draw line to draw a line with a width of PAD_WIDTH (8 pixels)
    # it draws 4 pixels on either side of the co-ordinates you give.
    
    # left paddle; position HALF_PAD_WIDTH to the X co-ordinate
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), PAD_WIDTH, 'White')
    
    # right paddle: subtract HALF_PAD_WIDTH from the canvas width
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), PAD_WIDTH, 'White')  
    
    # draw scores
    canvas.draw_text(str(score1),(225, 60), 40, 'White')
    canvas.draw_text(str(score2),(325, 60), 40, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    increment = 4
    
    # the paddle's velocity is updated in the key handlers
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -increment
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = increment
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -increment
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = increment

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # stop the paddle from moving
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()

# directions
print "w moves the left paddle up, s moves left paddle down"
print "up arrow moves the right paddle up, down arrow moves right paddle down"

