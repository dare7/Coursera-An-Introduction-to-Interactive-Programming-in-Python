__author__ = 'dare7'
# for development in external local IDE and to be complied with Codeskulptor at the same time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    simplegui.Frame._hide_status = True


import random, math

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
# default values for global vars
player_number = 0
secret_number = 0
game_mode = 100
current_count = 0
max_count = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global player_number
    global secret_number
    global game_mode
    global inp
    if game_mode == 1000:
        range1000()
    else:
        #default
        range100()
    # cheat mode below for a quick test
    #print(secret_number)
    tries_calc()
    print("==========================================")
    print("New game started!")
    print("Maximum number of tries for this game %s" % str(max_count))
    #default guess is 0
    inp.set_text("0")

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global secret_number
    global game_mode
    secret_number = random.randrange(0,100)
    game_mode = 100

def handler100():
    #handler for 100 range button
    range100()
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global secret_number
    global game_mode
    secret_number = random.randrange(0,1000)
    game_mode = 1000

def handler1000():
    #handler for 1000 range button
    range1000()
    new_game()

def handler_check():
    #handler for result check button
    global inp
    #forward number to guess func
    input_guess(inp.get_text())

def tries_calc():
    # calculate numbers of tries depending on game mode
    global game_mode
    global max_count
    global current_count
    max_count =  int(math.ceil(math.log(game_mode, 2)))
    current_count = max_count
    return max_count

def input_guess(guess):
    # main game logic goes here
    global player_number
    global secret_number
    global current_count
    try:
        # if no exceptions
        player_number = int(guess)
    except:
        # if user entered non digit
        print("Try to enter a number next time! Setting your choice to last choice or default")
    print("Guess was %s" % str(player_number))
    current_count -= 1
    if (player_number < secret_number) and (current_count > 0):
        print("Higher")
    elif (player_number > secret_number) and (current_count > 0):
        print("Lower")
    elif (player_number == secret_number) and (current_count > 0):
        print("Correct! You may now take that cookie")
        new_game()
    elif current_count == 0:
        print("You lost!")
        new_game()
    print("Guesses left: %s" % str(current_count))

if __name__ == '__main__':
    # for future import as module usage

    # create frame
    frame = simplegui.create_frame('Guess the number! (c) Epic Gamedev Corporation', 200, 200, 300)
    # register event handlers for control elements and start frame
    inp = frame.add_input('Enter your guess', input_guess, 50)
    frame.add_button("Check my number", handler_check, 150)
    frame.add_button("Reset", new_game, 150)
    frame.add_button("Range: 0 - 100", handler100, 150)
    frame.add_button("Range: 0 - 1000", handler1000, 150)
    frame.add_button('Quit', frame.stop, 150)
    # call new_game
    new_game()
    frame.start()