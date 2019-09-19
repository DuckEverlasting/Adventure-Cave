import random
from colorama import init as color_init
import os

from constants import text_style, pause
from logic import parse_list, parse_command, action_synonyms
from definitions import item, room, mob, player, action
from mob_act import mob_act

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

# Initialize colorama
color_init()

#
mem = {
    "looked_at": {}
}

#
# Main loop
#

end_game = False
time_passed = False
player_moved = True


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

pause(.5)

os.system("cls" if os.name == "nt" else "clear")

pause()

# Start of loop
while not end_game:

    # Before player's turn
    if time_passed:
        for i in mob:
            if mob[i].alive:
                mob_act(mob[i], player, player_moved)
                
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
        print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
        

    # Brief pause included for flavor
    pause()

    if item["amulet_of_yendor"] in player.items:
        # set game to end after this loop
        end_game = True
        print("You've won the game! Congratulations!!!")
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
        pause(3)

