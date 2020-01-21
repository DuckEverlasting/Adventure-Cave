import random
import copy
from colorama import init as color_init
import os

from constants import text_style, pause
from logic import parse_list, parse_command, action_synonyms
from definitions import create
from mob_act import mob_act

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

# Initialize colorama
color_init()

end_game = False
time_passed = False
player_moved = True
item = None
room = None
mob = None
player = None
action = None
mem = {}

def initialize_state():
    global item
    global room
    global mob
    global player
    global action
    state = create()
    item = state["item"]
    room = state["room"]
    mob = state["mob"]
    player = state["player"]
    action = state["action"]

def initialize_mem():
# Initialize mem - use when starting new game
    return {
        "score": 0,
        "looked_at": {},
        "save_dat": {}
    }

initialize_state()
mem = initialize_mem()

# Opening sequence
print(
    text_style['title'](
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

# Start of main loop
while not end_game:

    # Check for loaded game
    if not mem["save_dat"] == {}:
        player = mem["save_dat"]["player"]
        item = mem["save_dat"]["item"]
        room = mem["save_dat"]["room"]
        mob = mem["save_dat"]["mob"]
        mem["save_dat"] = {}

    # Before player's turn
    # Mob actions
    if time_passed:
        for i in mob:
            if mob[i].alive:
                mob_act(mob[i], player, player_moved)

    # Determine which information to display            
    if player_moved:
        spacers = "-" * len(player.loc.name)
        print(spacers)
        print(player.loc.name)
        print(spacers)

    mobs_here = [mob[i] for i in mob if mob[i].alive and mob[i].loc == player.loc]
    if player.loc.dark and not player.light_check():
        if not player.loc.slug + "_dark" in mem["looked_at"]:
            print(f"{player.loc.dark_desc}\n")
            mem["looked_at"][player.loc.slug + "_dark"] = True
        if player_moved and len(mobs_here) > 0:
            print(f"You hear {parse_list('something')} moving in the darkness.\n")
    else:
        if not player.loc.slug in mem["looked_at"]:
            print(f"{player.loc.desc}\n")
            mem["looked_at"][player.loc.slug] = True
        if player_moved:
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
        print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))

    if act in action:
        grammar_check = action[act].check_grammar(command)
        if not grammar_check["result"]:
            print(grammar_check["message"] + "\n")
        if act == "save":
            action_result = action[act].run(
                player = player,
                item = item,
                room = room,
                mob = mob,
                mem = mem
            )
        elif act == "load":
            action_result = action[act].run(mem = mem)
            if action_result and "load_game" in action_result:
                mem = action_result["load_game"]
                player_moved = True
                os.system("cls" if os.name == "nt" else "clear")
        else:
            action_result = action[act].run(
                command = command,
                player = player,
                item = item,
                mob = mob
            )

            if action_result != None:  
                if "time_passed" in action_result:
                    time_passed = True
                if "player_moved" in action_result:
                    player_moved = True
                if "end_game" in action_result:
                    end_game = True
                if "load_game" in action_result:
                    mem = action_result["load_game"]
                    player_moved = True

    else:
        print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
        

    # Brief pause included for flavor
    pause()

    # check for game over cases
    if player.health <= 0:
        print("You have died. Better luck next time!")

    elif item["amulet_of_yendor"] in player.items:
        print("You've won the game! Congratulations!!!")
    
    if player.health <= 0 or item["amulet_of_yendor"] in player.items:
        pause()
        print(
            text_style['title'](
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
        pause(2)
        choice = None
        while choice not in ["1", "2", "3"]:
            if not choice == None:
                print("Please enter one of the below options:")
            print(text_style["item"]("1: Start new game\n2: Load game\n3: Quit game\n"))
            choice = input("> ")
        if choice == "1":
            initialize_state()
            mem = initialize_mem()
            player_moved = True
            os.system("cls" if os.name == "nt" else "clear")
            pause()
        elif choice == "2":
            result = action["load"].run(mem = mem, get_confirm=False)
            if result and "load_game" in result:
                mem = result["load_game"]
                player_moved = True
                os.system("cls" if os.name == "nt" else "clear")
                pause()
            else:
                end_game = True
        elif choice == "3":
            end_game = True
            print("\nExiting game...\n")
            pause(0.75)
        

