# Implementation of classic arcade game Pong
__author__ = 'dare7'
# for development in external local IDE and to be complied with Codeskulptor at the same time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True

import random, math

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
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [1, 1] # pixels per update (1/60 seconds)
time = 0
paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
game_run = False
ai = False
score1 = 0
score2 = 0
ball_acc = 1.3
pad_acc = 4
difficulty = 30

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == 'RIGHT':
        ball_vel = [(random.randrange(120, 240)/60), -(random.randrange(60, 180)/60)]
    if direction == 'LEFT':
        ball_vel = [-(random.randrange(120, 240)/60), -(random.randrange(60, 180)/60)]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    if RIGHT:
        spawn_ball('RIGHT')
    if LEFT:
        spawn_ball('LEFT')


def start_handler():
    global game_run
    game_run = True


def reset_handler():
    global game_run, score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, LEFT, RIGHT
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    score1 = 0
    score2 = 0
    paddle1_vel = 0
    paddle2_vel = 0
    game_run = False
    LEFT = False
    RIGHT = True
    new_game()


def multiplayer_handler():
    global ai
    ai = False
    reset_handler()


def singlplayer_handler():
    global ai
    ai = True
    reset_handler()


def normalball_handler():
    global ball_acc
    ball_acc = 1.3


def fastball_handler():
    global ball_acc
    ball_acc = 2.0


def normaldif_handler():
    global difficulty, ai
    difficulty = 30
    ai = True


def harddif_handler():
    global difficulty, ai
    difficulty = 90
    ai = True


def ai_move():
    # ai to move left paddle
    global ball_pos, paddle1_pos, paddle1_vel, pad_acc, difficulty
    paddle1_vel = 0
    if ball_pos[1] < paddle1_pos+HALF_PAD_HEIGHT:
        paddle1_vel += -(pad_acc*difficulty)/60
    if ball_pos[1] > paddle1_pos+HALF_PAD_HEIGHT:
        paddle1_vel += (pad_acc*difficulty)/60


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, game_run, paddle1_vel, paddle2_vel
    global ball_acc, pad_acc, ai, RIGHT, LEFT
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    if game_run:
        # update ball
        ball_pos[0] += ball_vel[0]*ball_acc
        ball_pos[1] += ball_vel[1]*ball_acc
        # ball_border = [ball_pos[0] + BALL_RADIUS, ball_pos[1] + BALL_RADIUS]
        # distance = math.sqrt(((ball_pos[0]+BALL_RADIUS) - p1[0])**2 + (p0[1] - p1[1])**2)
        if ((ball_pos[1] + BALL_RADIUS) >= HEIGHT) or ((ball_pos[1] - BALL_RADIUS) <= 0):
            ball_vel[1] = -ball_vel[1]
        elif (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
            distance1 = math.sqrt((((ball_pos[0]) - PAD_WIDTH)**2 +
                                  ((ball_pos[1]) - (paddle1_pos+HALF_PAD_HEIGHT))**2))
            if distance1 <= BALL_RADIUS+HALF_PAD_HEIGHT:
                ball_vel[0] = -ball_vel[0] * 1.1
            else:
                score2 += 1
                RIGHT = True
                LEFT = False
                new_game()
        elif (ball_pos[0] + BALL_RADIUS) >= (WIDTH-PAD_WIDTH):
            distance2 = math.sqrt((((ball_pos[0]) - (WIDTH-PAD_WIDTH))**2 +
                                  ((ball_pos[1]) - (paddle2_pos+HALF_PAD_HEIGHT))**2))
            if distance2 <= BALL_RADIUS+HALF_PAD_HEIGHT:
                ball_vel[0] = -ball_vel[0] * 1.1
            else:
                score1 += 1
                LEFT = True
                RIGHT = False
                new_game()
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'White', 'White')
    # update paddle's vertical position, keep paddle on the screen
    if game_run:
        if ai:
            ai_move()
        if (paddle1_pos+paddle1_vel >= 0) and (paddle1_pos+paddle1_vel+PAD_HEIGHT <= HEIGHT):
            paddle1_pos += paddle1_vel
        if (paddle2_pos+paddle2_vel >= 0) and (paddle2_pos+paddle2_vel+PAD_HEIGHT <= HEIGHT):
            paddle2_pos += paddle2_vel
    # draw paddles
    canvas.draw_line([PAD_WIDTH/2, paddle1_pos],
                     [PAD_WIDTH/2, paddle1_pos+PAD_HEIGHT], PAD_WIDTH, 'White')
    canvas.draw_line([WIDTH-PAD_WIDTH/2, paddle2_pos],
                     [WIDTH-PAD_WIDTH/2, paddle2_pos+PAD_HEIGHT], PAD_WIDTH, 'White')
    # draw scores
    canvas.draw_text(str(score1), (WIDTH*0.25, HEIGHT*0.25), 75, 'White', 'monospace')
    canvas.draw_text(str(score2), (WIDTH*0.75-PAD_WIDTH-20, HEIGHT*0.25), 75, 'White', 'monospace')


def keydown(keydown):
    global paddle1_vel, paddle2_vel, ai, pad_acc, difficulty
    acc = pad_acc
    if keydown==simplegui.KEY_MAP["up"]:
        paddle2_vel = -acc*difficulty/60
    elif keydown==simplegui.KEY_MAP["down"]:
        paddle2_vel = acc*difficulty/60
    elif keydown==simplegui.KEY_MAP["w"] and not ai:
        paddle1_vel = -acc*difficulty/60
    elif keydown==simplegui.KEY_MAP["s"] and not ai:
        paddle1_vel = acc*difficulty/60


def keyup(keyup):
    global paddle1_vel, paddle2_vel
    acc = 0
    if keyup==simplegui.KEY_MAP["up"]:
        paddle2_vel = -acc
    elif keyup==simplegui.KEY_MAP["down"]:
        paddle2_vel = acc
    elif keyup==simplegui.KEY_MAP["w"]:
        paddle1_vel = -acc
    elif keyup==simplegui.KEY_MAP["s"]:
        paddle1_vel = acc


def init():
    # create frame
    frame = simplegui.create_frame("Pong by Dare7", WIDTH, HEIGHT)
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    # buttons
    frame.add_button(">>Start game!<<", start_handler, 150)
    frame.add_button("Reset!", reset_handler, 150)
    frame.add_button("Play with AI on the left", singlplayer_handler, 150)
    frame.add_button("2 player mode", multiplayer_handler, 150)
    frame.add_button("Normal ball speed", normalball_handler, 150)
    frame.add_button("Fast ball!", fastball_handler, 150)
    frame.add_button("Normal AI+slow pad", normaldif_handler, 150)
    frame.add_button("Hard AI+fast pad!", harddif_handler, 150)
    frame.add_button("Quit", frame.stop, 150)
    frame.add_label("Controls:")
    frame.add_label("Player1(left, AI): W, S")
    frame.add_label("Player2(right): up, down arrows")
    frame.add_label("Play with AI difficulty and speed!")
    frame.add_label("To start just press start!")

    # start frame
    frame.start()
    #new_game()

if __name__ == '__main__':
    # for future import as module usage
    init()