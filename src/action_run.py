import time
from text_style import item_text, error_text
from logic import parse_list


def run_help(command, player, item, mob):
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

def run_go(command, player, item, mob):
    dir_letter = command["adv"][0]
    result = player.move(dir_letter)
    if result:
        return {
            "time_passed": True,
            "player_moved": True,
        }
        

def run_inventory(command, player, item, mob):
    if len(player.items) > 0:
        print(f"You have {parse_list(player.items)} in your inventory.\n")
    else:
        print("You have no items in your inventory.\n")

def run_wait(command, player, item, mob):
    return {
        "time_passed": True,
    }

def run_quit(command, player, item, mob):
    confirm = input('Are you sure? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        print("\nExiting game...\n")
        time.sleep(0.75)
        return {"end_game": True}
    else:
        print()

def run_look(command, player, item, mob):
    if command["act"] != "look":
        if command["i_obj"]:
            print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))
        obj = command["d_obj"]
    else:
        if command["d_obj"]:
            print(error_text("ERROR: COMMAND NOT RECOGNIZED\n"))
        obj = command["i_obj"]
    if player.loc.dark and player.light_check() == False:
        print("Too dark for that right now.\n")
    elif obj in item:
        result = player.look_item(item[obj])
        if result:
            return {"time_passed": True}
    elif obj in mob:
        result = player.look_mob(mob[obj])
        if result:
            return {"time_passed": True}
    else:
        print("There's nothing here by that name.\n")

def run_get(command, player, item, mob):
    d_obj = command["d_obj"]
    if d_obj in item:
        result = player.get_item(item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        print("There's nothing here by that name.\n")

def run_drop(command, player, item, mob):
    d_obj = command["d_obj"]
    if d_obj in item:
        result = player.drop_item(item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        print("You don't have one of those in your inventory\n")

def run_use(command, player, item, mob):
    d_obj = command["d_obj"]
    i_obj = command["d_obj"]
    if d_obj in player.items:
        result = player.use_item(item[d_obj], i_obj)
        if result:
            return {"time_passed": True}
    elif d_obj in player.loc.items:
        result = player.use_item_from_env(item[d_obj], i_obj)
        if result:
            return {"time_passed": True}
    else:
        print("There's nothing here by that name.\n")

def run_attack(command, player, item, mob):
    d_obj = command["d_obj"]
    i_obj = command["i_obj"]
    if d_obj in mob:
        if mob[d_obj].loc == player.loc:
            if i_obj in player.items:
                pass
            else:
                if i_obj[0] in ["a", "e", "i", "o", "u"]:
                    print(f"You don't have an {i_obj} on you.")
                else:
                    print(f"You don't have a {i_obj} on you.") 
        else:
            print(f"There's no {d_obj} here.\n")
        
        result = player.attack_mob(item[d_obj], i_obj)
        if result:
            return {"time_passed": True}
    else:
        print("There's nothing here by that name.\n")

def run_eat(command, player, item, mob):
    d_obj = command["d_obj"]
    if d_obj in item:
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
