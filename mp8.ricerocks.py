#http://www.codeskulptor.org/#user33_feFyDksvRa_11.py
##################################################
# program template for RiceRocks week 8
# D. Kessler IIPP Spring 2014
##################################################
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
last_game_score = 0
games_played = 0
score = 0
lives = 3
time = 0
started = False

# CONSTANTS
MAX_ROCKS = 12

##################################################
# ImageInfo Class
##################################################
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

##################################################
# helper functions to handle transformations
##################################################
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group (group, canvas ):
    # create a copy of group, so not iterating over set you are changing
    for item in set(group):
        item.draw(canvas)
        if item.update(): # true if lifespan exceeded
            group.discard(item)

def group_collide(group, other_object):
    global explosion_group
    collision = False
    for item in set(group):
        if item.collide(other_object):
            new_explosion = Sprite( item.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(new_explosion)
            group.discard(item)
            collision = True
    return collision

def group_group_collide(group_a, group_b):
    collision_count = 0
    for item in set(group_a):
        if group_collide(group_b, item):
            collision_count += 1
            group_a.discard(item)          
    return collision_count

def set_initial_state():
    global started, lives, score, last_game_score
    global rock_group, missile_group, explosion_group
       
    # stop any new rocks from spawning
    if timer.is_running():
        timer.stop()
        
    # destroy any rocks and missiles
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
 
    # reset variables and the ship's position/velocity
    started = False
    lives = 3
    last_game_score = score
    score = 0
    my_ship.reset()
    
    # rewind the soundtrack
    soundtrack.rewind()
    
def start_new_game():
    global started
    started = True
    timer.start()
    soundtrack.play()
    
##################################################
# Ship class
##################################################
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
        # constants
        # Angular Velocity to increment and decrement the angular velocity by a fixed amount
        # so the spaceship slows down on the clockwise and counter clockwise rotation.
        # Fraction Forward to update velocity by small fraction of forward acceleration if thrust
        # example:self.ANGULAR_VELOCITY = 0.09, self.FRACTION_FORWARD = 0.50
        self.ANGULAR_VELOCITY = 0.05
        #self.FRACTION_FORWARD = 0.10
        self.FRACTION_FORWARD = 0.15

    # ORIENTATION
    def orient_counterclockwise(self):
        self.angle_vel -= self.ANGULAR_VELOCITY
        
    def orient_clockwise(self):
        self.angle_vel += self.ANGULAR_VELOCITY
    
    # THRUST
    def thrusters_on(self):
        self.thrust = True
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()
        
    def thrusters_off(self):
        self.thrust = False
        ship_thrust_sound.rewind()
        
    # HELPER FUNCTIONS
    def get_position(self):
        return self.pos      
    
    def get_radius(self):
        return self.radius
    
    def reset(self):
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.vel = [0, 0]
        self.angle = 0
        self.angle_vel = 0
        self.thrusters_off()
            
    # DRAW
    # ship imaged is tiled, first position is without thrust flames
    # you only need to increment the x to get to the second tile
    def draw(self,canvas):
        tiled_pos = [self.image_center[0], self.image_center[1]]
        if self.thrust:
            tiled_pos = [ self.image_center[0] + self.image_size[0],
                          self.image_center[1] ]

        canvas.draw_image(self.image, tiled_pos, self.image_size,
                          self.pos, self.image_size, self.angle)

    # UPDATE
    # velocity = velocity + thrust + friction
    # velocity = (1 - c) * velocity + thrust
    def update(self):
        
        # ANGULAR VELOCITY
        self.angle += self.angle_vel
        
        # POSITION UPDATE (position += velocity) with wrap around
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # THRUST
        # If thrusting, accelerate in direction of forward_vector.
        # And update the velocity vector by a small fraction of the forward
        # acceleration vector so that the ship does not accelerate too fast.
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * self.FRACTION_FORWARD
            self.vel[1] += forward[1] * self.FRACTION_FORWARD

        # CONSTANT 
        # let c be a small constant, for example, c = 0.05
        c = 0.01
        
        # FRICTION 
        # the velocity should always be multiplied by a constant factor c
        # less than one, to slow the ship down. It will then come to a stop
        # eventually after you stop the thrusters. Thrust will not be present
        # all the time but friction will. Friction applies the whole time.
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
          
    # SHOOT
    def shoot(self):
        global missile_group
        
        forward = angle_to_vector(self.angle)

        # position should be the tip of your ship's "cannon"
        # You can find the distance (a scalar) between
        # the ship center and the tip of the cannon. Multiply the facing
        # vector by this amount (and add to the ship position)
        # to find the tip of the cannon regardless of the ship orientation
        # missile_pos = ship_pos + (radius * sine/cosine of current angle)
        pos = [self.pos[0] + (self.radius * forward[0]),
               self.pos[1] + (self.radius * forward[1])]       

        # velocity is sum of the ship's velocity and a multiple of ship's forward vector
        vel = [self.vel[0] + (forward[0] * 6),
               self.vel[1] + (forward[1] * 6)]    
      
        # spawn the missile
        a_missile = Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add( a_missile )
  
###################################################    
# Sprite class
##################################################
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    # HELPER FUNCTIONS
    def get_position(self):
        return self.pos      
    
    def get_radius(self):
        return self.radius
   
    # DRAW
    def draw(self, canvas): 
        if self.animated:
            # choose correct tile in image based on age
            explosion_index = [self.age % self.lifespan // 1, self.age % self.lifespan // 1]
            explosion_center = [self.image_center[0] + explosion_index[0] * self.image_size[0],
                                self.image_center[1] ]
                                
            canvas.draw_image(self.image, explosion_center,self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    # UPDATE
    def update(self):
        # ANGULAR VELOCITY
        self.angle += self.angle_vel
        
        # POSITION UPDATE (position += velocity) with wrap around
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # AGE the sprite
        self.age +=1
        return self.age >= self.lifespan
        
    # COLLIDE
    # if distance is < r1 + r2, then they collided
    def collide(self, other_object):
        distance_between = dist( self.get_position(), other_object.get_position() )
        return ( distance_between < (self.get_radius() + other_object.get_radius()) )

##################################################
# event handlers
##################################################
def keydown(key):
    if not started:
        return
    if key == simplegui.KEY_MAP["left"]:
        my_ship.orient_counterclockwise()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.orient_clockwise()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters_on()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def keyup(key):
    if not started:
        return
    if key == simplegui.KEY_MAP["left"]:
        my_ship.orient_clockwise()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.orient_counterclockwise()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters_off()
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        start_new_game()

##################################################
# frame and drawing
##################################################
def draw(canvas):
    global time, lives, score, games_played
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # update and draw ship
    my_ship.draw(canvas)
    my_ship.update()
        
    # update and draw rocks and missiles and explosions
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # if the ship collided with any rock you lose a life
    if group_collide(rock_group, my_ship ):
        lives -= 1
        
    # if the missiles destroyed any rocks, you get points
    destroyed = group_group_collide(missile_group, rock_group )
    score += destroyed
    
    # are you out of lives ?
    if lives <= 0 and started:
        games_played += 1
        set_initial_state()
        
    # if score is a multiple of x, speed up the rocks, the game will never end...
    if score % 8:
        for item in rock_group:
            item.vel[0] *= .85
            item.vel[1] *= .85
    
    # draw score and lives, UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # draw splash screen if not started
    if not started:
        if games_played > 0:
            info_string = "Game over. Number of games played is " + str(games_played)+ \
                          ". Last game score " + str(last_game_score)
            canvas.draw_text(info_string, [50, 125], 28, "Red")
            
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
       
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    if len(rock_group) >= MAX_ROCKS:
        return
    
    # position
    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    # random velocity
    vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    
    # random angular velocity
    angular_vel = random.random() * .2 - .1
    
    # set a_rock to be a new rock on every tick, maximum 12
    # do not allow if the rock is too close to the spaceship
    a_rock = Sprite(pos, vel, 0, angular_vel, asteroid_image, asteroid_info)
    distance_between = dist(a_rock.get_position(), my_ship.get_position())
    if distance_between >= ( (my_ship.get_radius() + a_rock.get_radius()) / 2 ):
        rock_group.add(a_rock)
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)
set_initial_state()

# get things rolling
frame.start()
