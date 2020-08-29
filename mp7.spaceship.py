#http://www.codeskulptor.org/#user32_feFyDksvRa_5.py
##################################################
# program template for Spaceship
# D. Kessler IIPP Spring 2014
##################################################
import simplegui
import math
import random

#_debug = True
_debug = False

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

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
        self.ANGULAR_VELOCITY = 0.09
        self.FRACTION_FORWARD = 0.50

    # ORIENTATION
    def orient_counterclockwise(self):
        self.angle_vel -= self.ANGULAR_VELOCITY
        
    def orient_clockwise(self):
        self.angle_vel += self.ANGULAR_VELOCITY
    
    def maintain_orientation(self):
        my_ship.angle_vel = 0
    
    # THRUST
    def thrusters_on(self):
        self.thrust = True
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()
        
    def thrusters_off(self):
        self.thrust = False
        ship_thrust_sound.rewind()
    
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

        # CONSTANT 
        # let c be a small constant
        c = 0.05
        
        # FRICTION 
        # the velocity should always be multiplied by a constant factor c
        # less than one, to slow the ship down. It will then come to a stop
        # eventually after you stop the thrusters. Thrust will not be present
        # all the time but friction will. Friction applies the whole time.
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
          
        # THRUST
        # If thrusting, accelerate in direction of forward_vector.
        # And update the velocity vector by a small fraction of the forward
        # acceleration vector so that the ship does not accelerate too fast.
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * self.FRACTION_FORWARD
            self.vel[1] += forward[1] * self.FRACTION_FORWARD
              
        # ANGULAR VELOCITY
        self.angle += self.angle_vel
        
        # POSITION UPDATE (position += velocity) with wrap around
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        if _debug:
            print "Ship.update: vel is", self.vel[0], self.vel[1], "angular_velocity is", self.angle
        
    # SHOOT
    def shoot(self):
        global a_missile
        """ WHAT: a new missle """
        
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
        vel = [self.vel[0] + (forward[0] * 5),
               self.vel[1] + (forward[1] * 5)]    
      
        # spawn the missle
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
  
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
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
 
    def update(self):
        # ANGULAR VELOCITY
        self.angle += self.angle_vel
        
        # POSITION UPDATE (position += velocity) with wrap around
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT      

##################################################
# event handlers
##################################################
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.orient_counterclockwise()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.orient_clockwise()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters_on()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.maintain_orientation()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.maintain_orientation()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters_off()

##################################################
# frame and drawing
##################################################
def draw(canvas):
    global time
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw score and lives, UI
    canvas.draw_text("Lives", [70, 70], 22, "White")
    canvas.draw_text("Score", [680, 70], 22, "White")
    canvas.draw_text(str(lives), [70, 100], 22, "White")
    canvas.draw_text(str(score), [680, 100], 22, "White")
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    """ WHAT: a new rock appearing each second, only one rock on the canvas at a time """
    
    # position
    pos = [random.randrange(0, (WIDTH - 1)), random.randrange(0, (HEIGHT - 1))] 

    # random velocity
    #vel = [ (random.choice([1,-1]) * (random.random() * .1)), 
    #        (random.choice([1,-1]) * (random.random() * .1)) ]  
    vel = [ random.randint(-1, 1), random.randint(-1, 1) ]
    
    #ang = 0
    ang = float( random.random() * (2 * math.pi) )
    
    # random angular velocity
    #angular_vel = random.choice([1,-1]) * 0.05
    angular_vel = float((random.choice([-1,1]) * random.random()) / 10)
 
    # set a_rock to be a new rock on every tick
    a_rock = Sprite(pos, vel, ang, angular_vel, asteroid_image, asteroid_info)
     
    if _debug:
        print "rock_spawner, vel is", vel, "angular_velocity is", angular_vel
 
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
rock_spawner()  # so rock starts spinning right off the bat
timer.start()
frame.start()