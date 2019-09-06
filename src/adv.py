import time
from colorama import init as color_init
import os

from room import Room
from player import Player
from item import Item
from mob import Mob
from text_style import (
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

# Declare the items
item = {
    "sword": Item(
        item_text("sword"),
        f"a {item_text('sword')}",
        desc_text(
            "This sword has seen better days, but it's probably got one or two good swings left in it."
        ),
    ),
    "lantern": Item(
        item_text("lantern"),
        f"an extinguished {item_text('lantern')}",
        desc_text(
            "The lantern is unlit. It has fuel though; you imagine you could get it lit if you had some matches."
        ),
    ),
    "rope": Item(
        item_text("rope"),
        f"some {item_text('rope')}",
        desc_text("Good, sturdy rope, about 50 feet long."),
    ),
    "goblin_corpse": Item(
        item_text("goblin_corpse"),
        f"a {item_text('goblin_corpse')}",
        desc_text(
            f"It's a dead goblin. You turn it over, looking for valuables, but all you can find is a\ncrumpled {item_in_desc_text('matchbook')}, which falls to the floor next to the corpse."
        ),
        False,
    ),
    "matchbook": Item(
        item_text("matchbook"),
        f"a {item_text('matchbook')}",
        desc_text(
            "At first glance, the crumpled matchbook appears to be empty, but looking closer,\nyou see it still has one match inside."
        ),
    ),
}

# Declare the rooms
room = {
    "outside": Room(
        "Outside Cave Entrance",
        desc_text(f"{dir_in_desc_text('North')} of you, the cave mouth beckons."),
        True,
    ),
    "foyer": Room(
        "Foyer",
        desc_text(
            f"Dim light filters in from the {dir_in_desc_text('south')}. Dusty passages run {dir_in_desc_text('north')} and {dir_in_desc_text('east')}."
        ),
        False,
        [item["sword"]],
    ),
    "overlook": Room(
        "Grand Overlook",
        desc_text(
            f"A steep cliff appears before you, falling into the darkness. Ahead to the {dir_in_desc_text('north')}, a light\nflickers in the distance, but there is no way across the chasm.\nA passage leads {dir_in_desc_text('south')}, away from the cliff."
        ),
        False,
        [item["lantern"], item["rope"]],
    ),
    "narrow": Room(
        "Narrow Passage",
        desc_text(
            f"The narrow passage bends here from {dir_in_desc_text('west')} to {dir_in_desc_text('north')}. The smell of gold permeates the air."
        ),
        False,
    ),
    "treasure": Room(
        "Treasure Chamber",
        desc_text(
            f"You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by\nearlier adventurers. The only exit is to the {dir_in_desc_text('south')}."
        ),
        False,
    ),
}

# Declare the mobs

mob = {
    "goblin": Mob(
        mob_text("goblin"),
        f"a {mob_text('goblin')}",
        desc_text(
            f"The {mob_in_desc_text('goblin')} is eyeing you warily and shuffling his weight from one foot to the other.\nA crude knife dangles from his belt."
        ),
        f"A {mob_text('goblin')} shuffles into the room. At the sight of you, he gives a squeal of surprise and bares his teeth.",
        f"The {mob_text('goblin')} skitters out of the room, heading ",
        room["foyer"],
    )
}

# Declare the player
player = Player(room["outside"])

# Link rooms together
room["outside"].n_to = (room["foyer"], "You step into the mouth of the cave.")
room["foyer"].s_to = (
    room["outside"],
    "You head south, and find yourself outside the cave.",
)
room["foyer"].n_to = (
    room["overlook"],
    "You make your way north, and the cave opens up suddenly, revealing a vast chasm before you.",
)
room["foyer"].e_to = (
    room["narrow"],
    "You take the eastern passage. It grows narrower until you have a hard time standing straight.",
)
room["overlook"].s_to = (
    room["foyer"],
    "You step back from the cliff's edge and head south.",
)
room["narrow"].w_to = (
    room["foyer"],
    "You move west through the cramped passage until it opens up a bit.",
)
room["narrow"].n_to = (room["treasure"], "You follow your nose and head north.")
room["treasure"].s_to = (room["narrow"], "You head south into the narrow passage.")

# Add functionality to items
def use_sword():
    if mob["goblin"].loc == player.loc:
        print(
            f"You swing the {item_text('sword')} wildly at the {mob_text('goblin')}, and somehow manage to connect. He cries out in shock,\nthen gives you a baleful glare that fades into a look of weary resignation as he slumps to the ground.\n"
        )
        mob["goblin"].kill()
        player.loc.add_item(item["goblin_corpse"])
    else:
        print(
            f"You swing the {item_text('sword')} around wildly. After a few wide arcs, it slips out of your fingers and clatters to the ground.\n"
        )
        player.remove_item(item["sword"])
        player.loc.add_item(item["sword"])


setattr(item["sword"], "use", use_sword)


def on_search_goblin_corpse():
    item["goblin_corpse"].desc = "It's a dead goblin. You don't want to touch it again."
    player.loc.add_item(item["matchbook"])
    delattr(item["goblin_corpse"], "on_search")


setattr(item["goblin_corpse"], "on_search", on_search_goblin_corpse)


#
# Main
#

game_on = True

time_passed = False
player_moved = False

print("WELCOME TO ADVENTURE!\n")

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

    mobs_here = []
    for i in mob:
        if mob[i].alive == False:
            continue
        if mob[i].loc == player.loc:
            mobs_here.append(mob[i])

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

    elif command[0] in ("n", "s", "e", "w", "north", "south", "east", "west"):
        dir = command[0][0]
        result = player.move(dir)
        if result:
            print(result)
            time_passed = True
            player_moved = True
        else:
            print(error_text("ERROR: MOVEMENT NOT ALLOWED\n"))

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
                if hasattr(selected, "on_search"):
                    selected.on_search()
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
