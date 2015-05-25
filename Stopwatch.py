__author__ = 'dare7'
# for development in external local IDE and to be complied with Codeskulptor at the same time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    #simplegui.Frame._hide_status = True

import random, math

# "Stopwatch: The Game"

# define global variables
active = False
time = 0
tries = 0
wins = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    # get full minutes
    mins = t // 600
    # get milliseconds
    secs = t % 600
    # convert minutes to string
    mins_out = str(mins)
    # convert milliseconds to string, add leading zeroes
    secs_conv = '00' + str(secs)
    # substract seconds and miliseconds
    secs_out = secs_conv[-3:-1] + '.' + secs_conv[-1:]
    # merge minutes and milliseconds
    fomatted = mins_out + ':' + secs_out
    #print("formatted %s" % fomatted)
    return fomatted
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def handler_start():
    global active
    active = True


def handler_stop():
    global active, wins, tries
    if active and (str(time)[-1:] == "0"):
        tries += 1
        wins += 1
        active = False
    elif not active:
        print("Do not try to cheat, I'm watching you!")
    else:
        tries += 1
        active = False


def handler_reset():
    global active, time, wins, tries
    active = False
    time = 0
    wins = 0
    tries = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global time, active
    if active and time < 6000:
        time += 1
    elif time >= 6000:
        handler_reset()

# define draw handler
def draw(canvas):
    canvas.draw_text(format(time), (70,70), 30, "Green")
    result = str(wins) + '/' + str(tries)
    canvas.draw_text(result, (20,30), 20, "Green")

# init GUI
def init():
    # create frame
    frame = simplegui.create_frame("StopTimer, a megadev corp. blockbuster", 200, 120)

    # register event handlers
    #text = frame.add_input("Message:", update, 150)
    frame.set_draw_handler(draw)
    game_timer = simplegui.create_timer(100, tick)
    frame.add_button("Start", handler_start, 150)
    frame.add_button("Stop", handler_stop, 150)
    frame.add_button("Reset", handler_reset, 150)

    # start frame and timer
    frame.start()
    game_timer.start()

if __name__ == '__main__':
    # for future import as module usage
    init()