__author__ = 'dare7'
# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
#import section
import random

def name_to_number(name):
    # delete the following pass statement and fill in your code below
    # convertion of number to eleme
    if name == 'rock':
        number = 0
    elif name == 'Spock':
        number = 1
    elif name == 'paper':
        number = 2
    elif name == 'lizard':
        number = 3
    elif name == 'scissors':
        number = 4
    else:
        print("no such element in game: %s" % name)
        #default is rock if something goes wrong
        number = 0
    return number

    # convert name to number using if/elif/else
    # don't forget to return the result!


def number_to_name(number):
    # delete the following pass statement and fill in your code below
    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard'
    elif number == 4:
        name = 'scissors'
    else:
        print("no such element in game: %s" % str(number))
        #default is rock if something goes wrong
        name = 'rock'
    return name

    # convert number to a name using if/elif/else
    # don't forget to return the result!


def rpsls(player_choice):
    # game main function
    # delete the following pass statement and fill in your code below
    # print a blank line to separate consecutive games
    print("")
    # print out the message for the player's choice
    print("Player chooses %s" % player_choice)
    # convert the player's choice to player_number using the function name_to_number()
    name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print("Computer chooses %s" % comp_choice)
    # compute difference of comp_number and player_number modulo five
    game_result = (comp_number-name_to_number(player_choice)) % 5
    print(game_result)
    # use if/elif/else to determine winner, print winner message
    if game_result in [1,2]:
        # Humanity is doomed!
        print("Computer wins!")
    if game_result == 0:
        print("Player and computer tie!")
    if game_result in [3,4]:
        # Humanity is saved!
        print("Player wins!")

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
if __name__ == '__main__':
# for future import as module usage
    rpsls("rock")
    rpsls("Spock")
    rpsls("paper")
    rpsls("lizard")
    rpsls("scissors")

# always remember to check your completed program against the grading rubric