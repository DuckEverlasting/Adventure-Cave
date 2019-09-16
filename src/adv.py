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
from logic import parse_list, parse_command, action_synonyms
from definitions import item, room, mob, player, action

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

# Initialize colorama
color_init()

#
# Main loop
#

end_game = False
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
while not end_game:

    # Before player's turn
    if time_passed:
        for i in mob:
            if mob[i].alive == False:
                continue
            result = mob[i].moveRand()
            if result and mob[i].loc == player.loc:
                print(f"{mob[i].text['enter']}\n")
                # Brief pause included for flavor
                pause()
            elif mob[i].loc == player.loc and player_moved == False:
                idle_text = random.choice(mob[i].text["idle"])
                print(f"{idle_text}\n")
                # Brief pause included for flavor
                pause()
            elif result and mob[i].prev_loc == player.loc and player_moved == False:
                print(f"{mob[i].text['exit']}{result}\n")
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
    act = command["act"]
    adv = command["adv"]
    d_obj = command["d_obj"]
    prep = command["prep"]
    i_obj = command["i_obj"]
    error = command["error"]

    # Check for synonyms in actions. This check happens here as opposed
    # to in "logic" to preserve the parsed command for actions where
    # the wording is important. 
    if act in action_synonyms:
        act = action_synonyms[act]

    # Resolve player action
    print()

    if error:
        print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))

    if act in action:
        result = action[act].run(
            command = command,
            player = player,
            item = item,
            mob = mob
        )

        if result != None:  
            if "time_passed" in result:
                time_passed = True
            if "player_moved" in result:
                player_moved = True
            if "end_game" in result:
                end_game = True
        
    else:
        print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))
        

    # Brief pause included for flavor
    pause()

    if item["amulet_of_yendor"] in player.items:
        # set game to end after this loop
        end_game = True
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

