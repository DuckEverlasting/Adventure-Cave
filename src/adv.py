import time
from colorama import Fore, Back, Style, init as colorInit
import os
import textwrap

from room import Room
from player import Player
from item import Item

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

# Initialize colorama
colorInit()

# Set up wrapper for indenting text
indentText = textwrap.TextWrapper(
    initial_indent="    ", width=70, subsequent_indent="    "
)

# Declare the items
item = {
    "sword": Item(
        f"{Fore.CYAN}{Style.BRIGHT}sword{Style.RESET_ALL}",
        f"a {Fore.CYAN}{Style.BRIGHT}sword{Style.RESET_ALL}",
        "This sword has seen better days, but it's probably got one or two good swings left in it.",
    ),
    "lantern": Item(
        f"{Fore.CYAN}{Style.BRIGHT}lantern{Style.RESET_ALL}",
        f"a {Fore.CYAN}{Style.BRIGHT}lantern{Style.RESET_ALL}",
        "The lantern is unlit. It has fuel though; you imagine you could get it lit if you had some matches.",
    ),
    "rope": Item(
        f"{Fore.CYAN}{Style.BRIGHT}rope{Style.RESET_ALL}",
        f"some {Fore.CYAN}{Style.BRIGHT}rope{Style.RESET_ALL}",
        "Good, sturdy rope, about 50 feet long.",
    ),
}

# Declare the rooms
room = {
    "outside": Room(
        "Outside Cave Entrance",
        """North of you, the cave mouth beckons."""
    ),
    "foyer": Room(
        "Foyer",
        """Dim light filters in from the south. Dusty
passages run north and east.""",
        [item["sword"]],
    ),
    "overlook": Room(
        "Grand Overlook",
        """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""",
        [item["lantern"], item["rope"]],
    ),
    "narrow": Room(
        "Narrow Passage",
        """The narrow passage bends here from west
to north. The smell of gold permeates the air.""",
    ),
    "treasure": Room(
        "Treasure Chamber",
        """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""",
    ),
}

# Link rooms together
room["outside"].n_to = (
    room["foyer"],
    """You step into the mouth of the cave."""
)
room["foyer"].s_to = (
    room["outside"],
    """You head south, and find yourself outside the cave.""",
)
room["foyer"].n_to = (
    room["overlook"],
    """You make your way north, and the cave opens up suddenly, revealing a vast chasm before you.""",
)
room["foyer"].e_to = (
    room["narrow"],
    """You take the eastern passage. It grows narrower until you have a hard time standing straight.""",
)
room["overlook"].s_to = (
    room["foyer"],
    """You step back from the cliff's edge and head south.""",
)
room["narrow"].w_to = (
    room["foyer"],
    """You move west through the cramped passage until it opens up a bit.""",
)
room["narrow"].n_to = (
    room["treasure"],
    """You follow your nose and head north."""
)
room["treasure"].s_to = (
    room["narrow"],
    """You head south into the narrow passage."""
)

# Function to parse out language for listing items. Pass a list of items into it.
def itemCheck(list):
    if len(list) > 0:
        itemString = ""
        length = len(list)
        for (index, el) in enumerate(list):
            if index == 0:
                itemString = el.longName
            elif length > index + 1:
                itemString = f"{itemString}, {el.longName}"
            elif length == 2:
                itemString = f"{itemString} and {el.longName}"
            else:
                itemString = f"{itemString}, and {el.longName}"

    return itemString

# Declare the player
player = Player(room["outside"])

#
# Main
#

gameOn = True

while gameOn:
    print("Current Room: " + player.loc.name)
    print(indentText.fill(f"{Fore.YELLOW}{player.loc.desc}{Style.RESET_ALL}"))
    if len(player.loc.items) > 0:
        print(f"\nYou see {itemCheck(player.loc.items)} here.")

    command = input("\n> ").lower().split()

    print()

    if len(command) > 2:
        print(f"{Fore.RED}{Style.BRIGHT}ERROR: USE TWO WORDS OR LESS\n{Style.RESET_ALL}")

    elif command[0] in ("n", "s", "e", "w", "north", "south", "east", "west"):
        dir = command[0][0]
        player.move(dir)

    elif command[0] in ("l", "look"):
        if len(command) > 1 and command[1] in item:
            player.lookItem(item[command[1]])
        else:
            print(f"{Fore.RED}{Style.BRIGHT}ERROR: NO SUCH ITEM\n{Style.RESET_ALL}")

    elif command[0] in ("i", "inv", "inventory"):
        if len(player.items) > 0:
            print(f"You have {itemCheck(player.items)} in your inventory.\n")
        else:
            print("You have no items in your inventory.\n")

    elif command[0] in ("get", "take"):
        if len(command) > 1 and command[1] in item:
            selected = item[command[1]]
            result = player.loc.removeItem(selected)
            if result: player.addItem(selected)
        else:
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: NO SUCH ITEM IN ROOM\n{Style.RESET_ALL}')

    elif command[0] in ("drop", "leave"):
        if len(command) > 1 and command[1] in item:
            selected = item[command[1]]
            result = player.removeItem(selected)
            if result: player.loc.addItem(selected)
        else:
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: NO SUCH ITEM IN INVENTORY\n{Style.RESET_ALL}')

    elif command[0] in ("q", "quit"):
        print("Exiting game...\n")
        gameOn = False

    else:
        print(f"{Fore.RED}{Style.BRIGHT}ERROR: COMMAND NOT RECOGNIZED\n{Style.RESET_ALL}")

# Brief pause included for flavor 
    time.sleep(0.5)
