import time
from text_style import item_text
from logic import parse_list


def run_help():
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

def run_go(command, player):
    dir_letter = command["adv"][0]
    result = player.move(dir_letter)
    if result:
        return {
            "time_passed": True,
            "player_moved": True,
        }
        

def run_inventory(player):
    if len(player.items) > 0:
        print(f"You have {parse_list(player.items)} in your inventory.\n")
    else:
        print("You have no items in your inventory.\n")

def run_wait():
    return {
        "time_passed": True,
    }

def run_quit():
    confirm = input('Are you sure? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        print("\nExiting game...\n")
        time.sleep(0.75)
        return {"game_on": False}
    else:
        print()

def run_look(command, player, item, mob):
    d_obj = command["d_obj"]
    if not d_obj:
        print("What would you like to look at?\n")
    elif player.loc.dark and player.light_check() == False:
        print("Too dark for that right now.\n")
    elif d_obj in item:
        result = player.look_item(item[d_obj])
        if result:
            return {"time_passed": True}
    elif d_obj in mob:
        result = player.look_mob(mob[d_obj])
        if result:
            return {"time_passed": True}
    else:
        print("There's nothing here by that name.\n")

def run_get(command, player, item):
    d_obj = command["d_obj"]
    if not d_obj:
        print(f"What would you like to get?\n")
    elif d_obj in item:
        result = player.get_item(item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        print("There's nothing here by that name.\n")

def run_drop(command, player, item):
    d_obj = command["d_obj"]
    if not d_obj:
        print(f"What would you like to drop?\n")
    elif d_obj in item:
        result = player.drop_item(item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        print("You don't have one of those in your inventory\n")

def run_use(command, player, item):
    d_obj = command["d_obj"]
    if not d_obj:
        print(f"What would you like to use?\n")
    elif d_obj in item:
        result = player.use_item(item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        print("There's nothing here by that name.\n")

def run_attack(command, player, item, mob):
    pass

def run_eat(command, player, item, mob):
    d_obj = command["d_obj"]
    if not d_obj:
        print(f"What would you like to eat?\n")
    elif d_obj in item:
        result = player.eat_item(item[d_obj])
        if result:
            return {"time_passed": True}
    elif d_obj in mob:
        if mob[d_obj].loc == player.loc:
            print(f"That's... not food.\n")
        else:
            print("There's nothing here by that name.\n")
    else:
        print("There's nothing here by that name.\n")
