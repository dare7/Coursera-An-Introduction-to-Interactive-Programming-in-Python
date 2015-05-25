__author__ = 'dare7'
# program template for Spaceship
# for development in external local IDE and to be complied with Codeskulptor at the same time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

# globals for ship
SHIP_ANG_VEL_INC = 0.05
SHIP_VEL_ACC = 0.1
SHIP_FRICTION = 0.99

# globals for rock
ROCK_SPEED = 0.001
rocks = []


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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

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

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
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

    def draw(self, canvas):
        #canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest, rotation)
        if not self.thrust:
            canvas.draw_image(self.image, self.image_center, self.image_size, [self.pos[0], self.pos[1]],
                              self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]],
                              self.image_size, [self.pos[0], self.pos[1]], self.image_size, self.angle)
        #canvas.draw_image(self.image, self.image_center, self.image_size, [self.pos[0], self.pos[1]], self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        if self.thrust:
            self.vel[0] += angle_to_vector(self.angle)[0]*SHIP_VEL_ACC
            self.vel[1] += angle_to_vector(self.angle)[1]*SHIP_VEL_ACC
        self.vel[0] *= SHIP_FRICTION
        self.vel[1] *= SHIP_FRICTION
        if self.pos[0] < 0:
            self.pos[0] = WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0



    def turn_left(self):
        self.angle_vel -= SHIP_ANG_VEL_INC

    def turn_right(self):
        self.angle_vel += SHIP_ANG_VEL_INC

    def thrust_on(self):
        self.thrust = True
        ship_thrust_sound.play()

    def thrust_off(self):
        self.thrust = False
        ship_thrust_sound.rewind()

    def shoot(self):
        global a_missile
        # __init__(self, pos, vel, ang, ang_vel, image, info, sound = None)
        a_missile = Sprite([self.pos[0] + ship_info.get_radius()*angle_to_vector(self.angle)[0],
                            self.pos[1] + ship_info.get_radius()*angle_to_vector(self.angle)[1]],
                           [(self.vel[0] + angle_to_vector(self.angle)[0])*2,
                            (self.vel[1] + angle_to_vector(self.angle)[1])*2],
                           self.angle, 0, missile_image, missile_info, missile_sound)


# Sprite class
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
        # canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        #canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest, rotation)
        canvas.draw_image(self.image, self.image_center, self.image_size, [self.pos[0], self.pos[1]],
                          self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        #self.vel[0] += angle_to_vector(self.angle)[0]*ROCK_SPEED
        #self.vel[1] += angle_to_vector(self.angle)[1]*ROCK_SPEED
        if self.pos[0] < 0:
            self.pos[0] = WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0


def draw(canvas):
    global time, ship_ang_vel, rocks
    # animate background
    #my_ship.vel[0] += 1/60
    #my_ship.vel[1] += 1/60
    #my_ship.angle_vel += 1/60
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
    #for rock in rocks:
    #    rock.update()
    a_rock.update()
    a_missile.update()
    # score and lives
    canvas.draw_text("lives: %s" % str(lives), (WIDTH*0.05, HEIGHT*0.1), 30, 'White', 'monospace')
    canvas.draw_text("score: %s" % str(score), (WIDTH*0.75, HEIGHT*0.1), 30, 'White', 'monospace')


def key_down(key):
    global my_ship
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn_left()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.turn_right()
    elif key ==  simplegui.KEY_MAP["up"]:
        my_ship.thrust_on()
    elif key ==  simplegui.KEY_MAP["space"]:
        my_ship.shoot()



def key_up(key):
    global my_ship, ship_ang_vel
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    elif key ==simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    elif key ==  simplegui.KEY_MAP["up"]:
        my_ship.thrust_off()


# timer handler that spawns a rock
def rock_spawner():
    # locally ok, crazy rotation in chrome, sorry can't get what's wrong!
    global a_rock, rocks
    #rock_pos = []
    #rock_pos[0], rock_pos[1] = 0, 0
    rock_vel1 = random.randrange(-100,100)/100
    rock_vel2 = random.randrange(-100,100)/100
    rock_pos1 = random.randrange(0, WIDTH)
    rock_pos2 = random.randrange(0, HEIGHT)
    rock_ang = random.randrange(0,628)/100
    rock_ang_vel = random.randrange(-10,10)/100
    #__init__(self, pos, vel, ang, ang_vel, image, info, sound = None)
    #a_rock = Sprite([400, 300], [0.3, 0.4], 0, 0.1, asteroid_image, asteroid_info)
    a_rock = Sprite([rock_pos1, rock_pos2], [rock_vel1, rock_vel2], rock_ang, rock_ang_vel, asteroid_image, asteroid_info)
    rocks.append(a_rock)
    #a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 1, asteroid_image, asteroid_info)
    #print(rocks)


# quit handler
def quit():
    global frame
    frame.stop()
    timer.stop()


def init():
    # initialize frame
    global my_ship, a_rock, a_missile, frame, timer
    frame = simplegui.create_frame("Asteroids, by dare7", WIDTH, HEIGHT)
    frame.set_keydown_handler(key_down)
    frame.set_keyup_handler(key_up)
    frame.add_button("Quit", quit, 150)
    # initialize ship and two sprites
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
    a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

    # register handlers
    frame.set_draw_handler(draw)

    timer = simplegui.create_timer(1000.0, rock_spawner)

    # get things rolling
    timer.start()
    frame.start()

if __name__ == '__main__':
    # for future import as module usage
    init()