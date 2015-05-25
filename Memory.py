# implementation of card game - Memory
__author__ = 'dare7'
# for development in external local IDE and to be complied with Codeskulptor at the same time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True

import random
# constants
WIDTH = 800
HEIGHT = 100

# global vars
cards = []
exposed = []
state = 0
last_card = -1
current_card = -1
turns = 0
winner = ("Good job!", "Great move!", "Supermemory!", "Photomemory!")
looser = ("Try harder!", "Maybe next time!", "Oops!", "Just bad luck!")


# helper function to initialize globals
def new_game():
    global cards,exposed, turns, state
    exposed = []
    cards = []
    cards = list(range(8))+list(range(8))
    random.shuffle(cards)
    turns = 0
    state = 0
    v = False
    i = 1
    label.set_text("Turns = %s" % str(turns))
    label2.set_text("System info:")
    while i <=16:
        exposed.append(v)
        i += 1


# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, current_card, last_card,turns
    s = int(pos[0])//50
    if not exposed[s]:
        if state == 0:
            exposed[s] = True
            current_card = s
            state = 1
        elif state == 1:
            exposed[s] = True
            last_card = current_card
            current_card = s
            state = 2
            turns += 1
            label.set_text("Turns = %s" % str(turns))
        elif state == 2:
            if cards[last_card] != cards[current_card]:
                exposed[last_card] = False
                exposed[current_card] = False
                label2.set_text("System info: %s" % random.choice(looser))
            else:
                label2.set_text("System info: %s" % random.choice(winner))
            exposed[s] = True
            current_card = s
            state = 1
                        

# cards are logically 50x100 pixels in size
def draw(canvas):
    card_width = WIDTH/16
    card_height = HEIGHT
    current = 0
    for card, ex in zip(cards,exposed):
        if ex:
            canvas.draw_text(str(card), (current-2, card_height-20), card_height-10, 'white', 'monospace')
        else:
            canvas.draw_polygon([(current, 0),
                                 (current+card_width, 0),
                                 (current+card_width, card_height),
                                 (current, card_height)],
                                5, 'Black', 'White')
        current += card_width


# create frame and add a button and labels
def init():
    global label, label2
    frame = simplegui.create_frame("Memory by dare7", 800, 100)
    frame.add_button("Reset", new_game, 50)
    #frame.add_button("Quit", frame.stop, 50)
    label = frame.add_label("Turns = %s" % str(turns))
    label2 = frame.add_label("System info:")

    # register event handlers
    frame.set_mouseclick_handler(mouseclick)
    frame.set_draw_handler(draw)

    # get things rolling
    new_game()
    frame.start()


if __name__ == '__main__':
    # for future import as module usage
    init()