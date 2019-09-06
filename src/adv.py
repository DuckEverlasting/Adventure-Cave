import time
from colorama import init as color_init
import os

from definitions import item, room, mob, player
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
from logic import parse_list

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

# Opening sequence
print(
    title_text(
        """
⎸‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾⎹
⎸    █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗   ⎹
⎸   ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝   ⎹
⎸   ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗     ⎹
⎸   ██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝     ⎹
⎸   ██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗   ⎹
⎸   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ⎹
⎸                                                                                   ⎹
⎸                         ██████╗ █████╗ ██╗   ██╗███████╗                          ⎹
⎸                        ██╔════╝██╔══██╗██║   ██║██╔════╝                          ⎹
⎸                        ██║     ███████║██║   ██║█████╗                            ⎹
⎸                        ██║     ██╔══██║╚██╗ ██╔╝██╔══╝                            ⎹
⎸                        ╚██████╗██║  ██║ ╚████╔╝ ███████╗                          ⎹
⎸                         ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝                          ⎹
⎸___________________________________________________________________________________⎹

"""
    )
)

time.sleep(2)

os.system("cls" if os.name == "nt" else "clear")

time.sleep(0.5)

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
                time.sleep(0.5)
            elif result and mob[i].prev_loc == player.loc and player_moved == False:
                print(f"{mob[i].exit_text}{result}\n")
                # Brief pause included for flavor
                time.sleep(0.5)

    spacers = ""
    for i in range(len(player.loc.name)):
        spacers += "-"

    print(spacers)
    print(player.loc.name)
    print(spacers)
    print(f"{player.loc.desc}\n")

    mobs_here = [i for i in mob if mob[i].alive and mob[i].loc == player.loc]

    if len(player.loc.items) > 0:
        print(f"You see {parse_list(player.loc.items)} here.")
        if len(mobs_here) == 0:
            print()

    if len(mobs_here) > 0:
        print(f"You see {parse_list(mobs_here)} here.\n")

    # Reset variables
    time_passed = False
    player_moved = False

    # Player's turn
    command = input("> ").lower().split()

    # Resolve player action
    print()

    if len(command) > 2:
        print(error_text("ERROR: USE TWO WORDS OR LESS\n"))

    elif command[0] in ("h", "help"):
        print("==============\nBasic Controls\n==============")
        print(
            f"Move around: \"{item_text('n')}orth\", \"{item_text('s')}outh\", \"{item_text('e')}ast\", \"{item_text('w')}est\", \"{item_text('d')}own\", \"{item_text('u')}p\""
        )
        print(
            f"Interact with things: \"{item_text('l')}ook\", \"get\", \"drop\", \"use\""
        )
        print(f"Check inventory: \"{item_text('i')}nv\"")
        print(f"Exit game: \"{item_text('q')}uit\"")
        print()

    elif command[0] in (
        "n",
        "s",
        "e",
        "w",
        "d",
        "u",
        "north",
        "south",
        "east",
        "west",
        "down",
        "up",
    ):
        dir = command[0][0]
        result = player.move(dir)
        if result:
            time_passed = True
            player_moved = True

    elif command[0] in ("i", "inv", "inventory") and len(command) == 1:
        if len(player.items) > 0:
            print(f"You have {parse_list(player.items)} in your inventory.\n")
        else:
            print("You have no items in your inventory.\n")

    elif command[0] in ("l", "look"):
        if len(command) == 1:
            print("What would you like to look at?\n")
        elif command[1] in item:
            selected = item[command[1]]
            result = player.look_item(selected)
            if result:
                print(f"{selected.desc}\n")
                if hasattr(selected, "on_look"):
                    selected.on_look()
                time_passed = True
            else:
                print(error_text("ERROR: NOTHING HERE BY THAT NAME\n"))
        elif command[1] in mob and mob[command[1]].loc == player.loc:
            selected = mob[command[1]]
            print(f"{selected.desc}\n")
        else:
            print(error_text("ERROR: NOTHING HERE BY THAT NAME\n"))

    elif command[0] in ("get", "take"):
        if len(command) == 1:
            print(f"What would you like to {command[0]}?\n")
        elif command[1] in item:
            selected = item[command[1]]
            result = player.loc.remove_item(selected)
            if result[0]:
                player.add_item(selected)
                print(f"You pick up the {selected.name}.\n")
                time_passed = True
            else:
                print(result[1])
        else:
            print(error_text("ERROR: NOTHING HERE BY THAT NAME\n"))

    elif command[0] in ("drop", "leave"):
        if len(command) == 1:
            print(f"What would you like to {command[0]}?\n")
        elif command[1] in item:
            selected = item[command[1]]
            result = player.remove_item(selected)
            if result:
                player.loc.add_item(selected)
                print(f"You set down the {selected.name}.\n")
                time_passed = True
            else:
                print(error_text("ERROR: NO SUCH ITEM IN INVENTORY\n"))
        else:
            print(error_text("ERROR: NO SUCH ITEM IN INVENTORY\n"))

    elif command[0] == "use":
        if len(command) == 1:
            print(f"What would you like to {command[0]}?\n")
        elif len(command) > 1 and command[1] in item:
            player.use_item(item[command[1]])
            time_passed = True

    elif command[0] == "swing" and command[1] == "sword":
        if len(command) == 1:
            print(f"What would you like to {command[0]}?\n")
        else:
            player.use_item(item[command[1]])
            time_passed = True

    elif command[0] in ("q", "quit"):
        print("Exiting game...\n")
        game_on = False

    else:
        print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))

    # Brief pause included for flavor
    time.sleep(0.5)
