__author__ = 'dare7'
# program template for Spaceship
# web interface http://www.codeskulptor.org/#user39_NoSxHRjw1Dy0mQt.py
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
time = 0
message = "Asteroids!"

# globals for leveling
ship_upgrades = 0
missile_count = 1
level = 1
upgrade_cost = 10
rock_acc = 1
missile_range = 1
asteroid_cost = level

# globals for ship
SHIP_ANG_VEL_INC = 0.05
SHIP_VEL_ACC = 0.1
SHIP_FRICTION = 0.99

# globals for missile
missile_group = set()

# globals for rock
ROCK_SPEED = 0.001
rock_group = set()
rock_group_wipe = set()
rock_limit = 12
rock_counter = 0
explosion_group = set()

#globals for game
started = False


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
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

    def set_lifespan(self, value):
        self.lifespan *= value


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
missile_info = ImageInfo([5,5], [10, 10], 3, 30)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# animated explosion of ship
# __init__(self, center, size, radius=0, lifespan=None, animated=False):
explosion_ship_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.animated = info.get_animated()

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
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        if self.thrust:
            self.vel[0] += angle_to_vector(self.angle)[0]*SHIP_VEL_ACC
            self.vel[1] += angle_to_vector(self.angle)[1]*SHIP_VEL_ACC
        self.vel[0] *= SHIP_FRICTION
        self.vel[1] *= SHIP_FRICTION

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
        global missile_group, missile_count, missile_range
        # __init__(self, pos, vel, ang, ang_vel, image, info, sound = None)
        for i in range(missile_count):
            gen = i*30
            a_missile = Sprite([self.pos[0] + (self.radius + gen)*angle_to_vector(self.angle)[0],
                                self.pos[1] + (self.radius + gen)*angle_to_vector(self.angle)[1]],
                               [(self.vel[0] + angle_to_vector(self.angle)[0]*6),
                                (self.vel[1] + angle_to_vector(self.angle)[1]*6)],
                               self.angle, 0, missile_image, missile_info, missile_sound)
            missile_group.add(a_missile)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


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
        global explosion_group, time
        if self.animated:
            current_exp_index = (time % self.get_radius()) // 1
            current_exp_center = [self.image_center[0] + current_exp_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_exp_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)



    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other):
        # dist = math.sqrt((circle1.x-circle2.x)**2 + (circle1.y-circle2.y)**2) - circle1.r - circle2.r
        distance = math.sqrt((self.get_position()[0] - other.get_position()[0])**2 +
                             (self.get_position()[1] - other.get_position()[1])**2)
        if distance <= self.get_radius() + other.get_radius():
            return True
        else:
            return False


def draw(canvas):
    global time, started, lives, my_ship, rock_group, missile_group, score, upgrade_number, rock_counter, message,\
        explosion_group, upgrade_cost, ship_upgrades, asteroid_cost, upgrade_dist
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    # play the music
    if started:
        soundtrack.play()
    # draw ship and sprites
    my_ship.draw(canvas)
    #a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    #a_missile.update()
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    # score and lives
    col1 = group_group_collide(rock_group, missile_group)
    col2 = group_collide(rock_group, my_ship)
    if col1 > 0:
        score += col1 * asteroid_cost
    if col2:
        lives -= 1
    if started:
        if lives <= 0:
            full_reset()
            message = "You lost!"
        if len(rock_group) == 0 and rock_counter == rock_limit:
            next_level()
    # set button text
    upgrade_number.set_text("+1 missile for %s$" % str(upgrade_cost))
    upgrade_dist.set_text("+1 missile range %s$" % str(upgrade_cost))
    # set canvas text
    canvas.draw_text("%s" % message, (WIDTH*0.4, HEIGHT*0.1), 30, 'White', 'monospace')
    canvas.draw_text("money: %s$" % str(score), (WIDTH*0.75, HEIGHT*0.1), 30, 'White', 'monospace')
    canvas.draw_text("level: %s" % str(level), (WIDTH*0.75, HEIGHT*0.2), 30, 'White', 'monospace')
    canvas.draw_text("lives: %s" % str(lives), (WIDTH*0.05, HEIGHT*0.1), 30, 'White', 'monospace')
    canvas.draw_text("upgrades: %s" % str(ship_upgrades), (WIDTH*0.05, HEIGHT*0.2), 30, 'White', 'monospace')
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())


def key_down(key):
    global my_ship
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn_left()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.turn_right()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()


def key_up(key):
    global my_ship, ship_ang_vel
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    elif key ==simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    elif key ==  simplegui.KEY_MAP["up"]:
        my_ship.thrust_off()


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True


# timer handler that spawns a rock
def rock_spawner():
    global rock_group, rock_limit, rock_counter, started, my_ship, rock_acc
    rock_vel = [(random.random() * .6 - .3)*rock_acc, (random.random() * .6 - .3)*rock_acc]
    x = my_ship.get_position()
    # rock position generator to avoid spawning on ship
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    distance = math.sqrt((my_ship.get_position()[0] - rock_pos[0])**2 + (my_ship.get_position()[1] - rock_pos[1])**2)
    buffer = my_ship.get_radius()*3
    if distance < buffer and started:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_ang_vel = random.random() * .2 - .1
    # __init__(self, pos, vel, ang, ang_vel, image, info, sound = None)
    if rock_counter < rock_limit and started:
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        rock_counter += 1


def process_sprite_group(canvas, sprites):
    sprites_wipe = set()
    temp_set = sprites.copy()
    for sprite in temp_set:
        sprite.draw(canvas)
        if sprite.update():
            sprites_wipe.add(sprite)
        else:
            sprite.update()
    sprites.difference_update(sprites_wipe)


# collision handler: many to one
def group_collide(sprites, obj):
    global explosion_group
    result = False
    temp_set = sprites.copy()
    for sprite in temp_set:
        #def collide(self, other):
        if sprite.collide(obj):
            rock_group_wipe.add(sprite)
            #an_explosion = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
            #__init__(self, pos, vel, ang, ang_vel, image, info, sound = None)
            an_explosion = Sprite(sprite.pos, sprite.vel, 0, 0, explosion_image, explosion_info)
            explosion_group.add(an_explosion)
            result = True
    #s.difference_update(set([5, 6, 7]))
    sprites.difference_update(rock_group_wipe)
    return result


# collistion handler many to many rock - missile
def group_group_collide(group1, group2):
    count = 0
    temp_set = group2.copy()
    for el1 in temp_set:
        if group_collide(group1, el1):
            group1.discard(el1)
            count += 1
    return count


# quit handler
def quit():
    global frame
    frame.stop()
    timer.stop()


#reset handler
def reset():
    global soundtrack, lives, score, rock_group, rock_counter, started, frame, explosion_group, missile_group,\
        ship_upgrades
    #lives = 3
    #score = 0
    rock_counter = 0
    ship_upgrades = 0
    rock_group = set()
    explosion_group = set()
    missile_group = set()
    started = False
    frame.set_mouseclick_handler(click)


# reset all + money, lives, music
def full_reset():
    global score, lives, soundtrack, rock_limit, message, rock_acc, upgrade_cost, ship_upgrades,\
        missile_count, missile_range, level
    message = "Asteroids!"
    lives = 3
    score = 0
    rock_limit = 12
    soundtrack.rewind()
    reset()
    rock_acc = 1
    upgrade_cost = 10
    level = 1
    missile_range = 1
    missile_count = 1



# increase roxk count and speed
def next_level():
    global level, rock_acc, rock_limit, asteroid_cost
    level += 1
    asteroid_cost = level
    rock_acc += 1
    rock_limit += 1
    reset()


def upgrade_count():
    global missile_count, score, upgrade_cost, ship_upgrades
    if score >= upgrade_cost:
        ship_upgrades += 1
        missile_count +=1
        score -= upgrade_cost
        upgrade_cost += 10


def upgrade_range():
    global score, upgrade_cost, missile_range, ship_upgrades
    if score >= upgrade_cost:
        ship_upgrades += 1
        missile_range += 0.1
        missile_info.set_lifespan(missile_range)
        score -= upgrade_cost
        upgrade_cost += 10


def init():
    # initialize frame
    global my_ship, a_missile, frame, timer, upgrade_number, upgrade_dist
    frame = simplegui.create_frame("Asteroids, by dare7", WIDTH, HEIGHT)
    upgrade_number = frame.add_button("+1 missile for %s$" % str(upgrade_cost), upgrade_count, 180)
    upgrade_dist = frame.add_button("+1 missile range %s$" % str(upgrade_cost), upgrade_range, 180)
    frame.add_button("Reset all", full_reset, 180)
    frame.add_button("Quit", quit, 180)
    # initialize ship and two sprites
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    #a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
    #a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
    # register handlers
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(key_down)
    frame.set_keyup_handler(key_up)
    frame.set_mouseclick_handler(click)
    frame.add_label("Shoot stars!")
    frame.add_label("Earn money!")
    frame.add_label("Avoid collision!")
    frame.add_label("Upgrade ship!")
    frame.add_label("")
    frame.add_label("Controls:")
    frame.add_label("Up: accelerate")
    frame.add_label("Left, right: turn")
    frame.add_label("Space: shoot")

    timer = simplegui.create_timer(1000.0, rock_spawner)

    # get things rolling
    timer.start()
    frame.start()

if __name__ == '__main__':
    # for future import as module usage
    init()