import time
import random
from colorama import init as color_init
import os

from text_style import (
    title_text,
    error_text,
    desc_text,
    item_text,
    item_in_desc_text,
    mob_text,
    mob_in_desc_text,
    dir_text,
    dir_in_desc_text,
)
from logic import parse_list, parse_command
from definitions import item, room, mob, player

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

# Initialize colorama
color_init()

#
# Main loop
#

game_on = True

time_passed = False
player_moved = False


def pause(num=0.75):
    time.sleep(num)


# Opening sequence
print(
    title_text(
        """
█‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾█
█    █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗   █
█   ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝   █
█   ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗     █
█   ██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝     █
█   ██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗   █
█   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   █
█                                                                                   █
█                         ██████╗ █████╗ ██╗   ██╗███████╗                          █
█                        ██╔════╝██╔══██╗██║   ██║██╔════╝                          █
█                        ██║     ███████║██║   ██║█████╗                            █
█                        ██║     ██╔══██║╚██╗ ██╔╝██╔══╝                            █
█                        ╚██████╗██║  ██║ ╚████╔╝ ███████╗                          █
█                         ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝                          █
█___________________________________________________________________________________█

"""
    )
)

pause(3)

os.system("cls" if os.name == "nt" else "clear")

pause()

# Start of loop
while game_on:

    # Before player's turn
    if time_passed:
        for i in mob:
            if mob[i].alive == False:
                continue
            result = mob[i].moveRand()
            if result and mob[i].loc == player.loc:
                print(f"{mob[i].enter_text}\n")
                # Brief pause included for flavor
                pause()
            elif mob[i].loc == player.loc and player_moved == False:
                idle_text = random.choice(mob[i].idle_text)
                print(f"{idle_text}\n")
                # Brief pause included for flavor
                pause()
            elif result and mob[i].prev_loc == player.loc and player_moved == False:
                print(f"{mob[i].exit_text}{result}\n")
                # Brief pause included for flavor
                pause()

    spacers = ""
    for i in range(len(player.loc.name)):
        spacers += "-"

    print(spacers)
    print(player.loc.name)
    print(spacers)
    if player.loc.dark and player.light_check() == False:
        print(f"{player.loc.dark_desc}\n")
    else:
        print(f"{player.loc.desc}\n")

    mobs_here = [mob[i] for i in mob if mob[i].alive and mob[i].loc == player.loc]

    if player.loc.dark == False or player.light_check():
        if len(player.loc.items) > 0:
            print(f"You see {parse_list(player.loc.items)} here.")
            if len(mobs_here) == 0:
                print()

        if len(mobs_here) > 0:
            print(f"You see {parse_list(mobs_here)} here.\n")
    else:
        if len(mobs_here) > 0:
            print(f"You hear {parse_list('something')} moving in the darkness.\n")

    # Reset variables
    time_passed = False
    player_moved = False

    # Player's turn
    command = input("> ").lower()

    # Parse command
    command = parse_command(command)

    # Resolve player action
    print()

    # One word handler
    if len(command) == 1:

        if command[0] == "help":
            print("==============\nBasic Controls\n==============")
            print(
                f"Move around: \"{item_text('n')}orth\", \"{item_text('s')}outh\", \"{item_text('e')}ast\", \"{item_text('w')}est\", \"down\", \"up\""
            )
            print(
                f"Interact with things: \"{item_text('l')}ook\", \"{item_text('g')}et\", \"{item_text('d')}rop\", \"{item_text('u')}se\""
            )
            print(f"Check inventory: \"{item_text('i')}nv\"")
            print(f"Do nothing: wait")
            print(f"Exit game: \"{item_text('q')}uit\"")
            print()

        elif command[0] in ("north", "south", "east", "west", "down", "up"):
            dir = command[0][0]
            result = player.move(dir)
            if result:
                time_passed = True
                player_moved = True

        elif command[0] == "inventory":
            if len(player.items) > 0:
                print(f"You have {parse_list(player.items)} in your inventory.\n")
            else:
                print("You have no items in your inventory.\n")

        elif command[0] == "wait":
            time_passed = True

        elif command[0] == "look":
            print("What would you like to look at?\n")

        elif command[0] in ("get", "drop", "use", "eat"):
            print(f"What would you like to {command[0]}?\n")

        elif command[0] == "quit":
            confirm = input('Are you sure? (Type "y" to confirm)\n> ')
            if confirm in ("y", "yes"):
                print("\nExiting game...\n")
                pause(.5)
                game_on = False
            else:
                print()
        else:
            print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))

    # Two word handler
    elif len(command) == 2:

        if command[0] == "look":
            if player.loc.dark and player.light_check() == False:
                print("Too dark for that right now.\n")
            elif command[1] in item:
                result = player.look_item(item[command[1]])
                if result:
                    time_passed = True
            elif command[1] in mob:
                result = player.look_mob(mob[command[1]])
                if result:
                    time_passed = True
            else:
                print("There's nothing here by that name.\n")

        elif command[0] == "get":
            if command[1] in item:
                result = player.get_item(item[command[1]])
                if result:
                    time_passed = True
            else:
                print("There's nothing here by that name.\n")

        elif command[0] in ("drop", "leave"):
            if command[1] in item:
                result = player.drop_item(item[command[1]])
                if result:
                    time_passed = True
            else:
                print("You don't have one of those in your inventory\n")

        elif command[0] == "use":
            if command[1] in item:
                result = player.use_item(item[command[1]])
                if result:
                    time_passed = True
            else:
                print("There's nothing here by that name.\n")

        elif command[0] == "wield" and command[1] == "sword":
            result = player.use_item(item[command[1]])
            if result:
                time_passed = True

        elif command[0] == "eat":
            if command[1] in item:
                result = player.eat_item(item[command[1]])
                if result:
                    time_passed = True
            elif command[1] in mob:
                if mob[command[1]].loc == player.loc:
                    print(f"That's... not food.\n")
                else:
                    print("There's nothing here by that name.\n")
            else:
                print("There's nothing here by that name.\n")


        else:
            print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))

    else:
        print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))

    # Brief pause included for flavor
    pause()

    if item["amulet_of_yendor"] in player.items:
        game_on = False
        print("You've won the game! Congratulations!!!")
        pause()
        print(
            title_text(
                """
█‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾█
█     ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗      █
█    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗     █
█    ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝     █
█    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗     █
█    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║     █
█     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝     █
█___________________________________________________________________________________█

"""
            )
        )

        pause(3)

