import shelve
from constants import text_style, pause
from logic import parse_list

def run_help(command, player, item, mob):
    print("==============\nBasic Controls\n==============")
    print(
        f"Move around: \"{text_style['item']('n')}orth\", \"{text_style['item']('s')}outh\", \"{text_style['item']('e')}ast\", \"{text_style['item']('w')}est\", \"down\", \"up\""
    )
    print(
        f"Interact with things: \"{text_style['item']('l')}ook\", \"{text_style['item']('g')}et\", \"{text_style['item']('d')}rop\", \"{text_style['item']('u')}se\""
    )
    print(f"Check inventory: \"{text_style['item']('i')}nv\"")
    print(f"Do nothing: wait")
    print(f"Exit game: \"{text_style['item']('q')}uit\"")
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
        pause(0.75)
        return {"end_game": True}
    else:
        print()

def run_look(command, player, item, mob):
    # GENERAL LOOK
    if not command["i_obj"] and not command["d_obj"]:
        if player.loc.dark and not player.light_check():
            print(f"{player.loc.dark_desc}\n")
        else:
            print(f"{player.loc.desc}\n")

        mobs_here = [mob[i] for i in mob if mob[i].alive and mob[i].loc == player.loc]

        if not player.loc.dark or player.light_check():
            if len(player.loc.items) > 0:
                print(f"You see {parse_list(player.loc.items)} here.")
                if len(mobs_here) == 0:
                    print()

            if len(mobs_here) > 0:
                print(f"You see {parse_list(mobs_here)} here.\n")
        else:
            if len(mobs_here) > 0:
                print(f"You hear {parse_list('something')} moving in the darkness.\n")
    else:    
    # SPECIFIC LOOK
        # Grammar check (because "look" uses prepositions but none of its synonyms do)
        if command["act"] != "look":
            if command["i_obj"]:
                print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
            obj = command["d_obj"]
        else:
            if command["d_obj"]:
                print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
            obj = command["i_obj"]

        # Check lights
        if player.loc.dark and not player.light_check():
            print("Too dark for that right now.\n")
        
        # Return description for item or mob if available
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
            if not i_obj:
                weapons = [i for i in player.items if "weapon" in i.tags] + [item["fists"]]
                weapon_string = "Attack with what?"
                for i in range(len(weapons)):
                    weapon_string += f"\n{i + 1}:  {text_style['item'](weapons[i].name)}"
                print(weapon_string)
                selection = input('\n> ')
                try:
                    selection = int(selection) - 1
                    i_obj = weapons[selection]
                except:
                    return
            elif not item[i_obj] in player.items:
                if i_obj[0] in ["a", "e", "i", "o", "u"]:
                    print(f"You don't have an {i_obj} on you.\n")
                    return
                else:
                    print(f"You don't have a {i_obj} on you.\n")
                    return
            elif "weapon" not in item[i_obj].tags:
                print("That's not a weapon.\n")
                return
            else:
                i_obj = item[i_obj]
            player.attack_mob(i_obj, mob[d_obj])
            return {"time_passed": True}                 
        else:
            print(f"There's no {d_obj} here.\n")
    else:
        print(f"There's no {d_obj} here.\n")

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

def run_save(player, item, room, mob, mem):
    # Get saved games
    saved_games = shelve.open('saved_games')
    if not "list" in saved_games:
        saved_games["list"] = []
    confirm = input('Save your game? (Type "y" to confirm)\n> ')
    if not confirm in ("y", "yes"):
        print("\nNever mind, then.\n")
        saved_games.close()
        return
    print("\nPick a name.")
    name = input('> ')
    if not name or name == "list":
        print("\nSave failed.\n")
        saved_games.close()
        return
    elif name in saved_games:
        confirm = input('That name already exists. Overwrite saved game? (Type "y" to confirm)\n> ')
        if not confirm in ("y", "yes"):
            print("\nNever mind, then.\n")
            saved_games.close()
            return
    mem["save_dat"] = {
        "player": player,
        "item": item,
        "room": room,
        "mob": mob
    }
    saved_games["list"] += [name]
    saved_games[name] = mem
    saved_games.close()
    print("\nSaved!.\n")
    return   
    
def run_load(player, item, room, mob, mem, loop=False):
    saved_games = shelve.open('saved_games')
    if not loop:
        confirm = input('Load a saved game? (Type "y" to confirm)\n> ')
        if not confirm in ("y", "yes"):
            print("\nNever mind, then.\n")
            saved_games.close()
            return
        print('\nLoad which game?')
        print(text_style['error']("0: NONE (Cancel load)"))
        for i in range(len(saved_games["list"])):
            print(text_style['item'](f"{i + 1}: {saved_games['list'][i]}\n"))
    else:
        print('\nPlease enter a valid number\n')
    number = input('> ')
    try:
        if int(number) == 0:
            print("\nNever mind, then.\n")
            saved_games.close()
            return
        elif int(number) - 1 in range(len(saved_games["list"])):
            print("\nLoading game...\n")
            pause(0.75)
            name = saved_games["list"][int(number) - 1]
            mem = saved_games[name]
            saved_games.close()
            return {"load_game": mem}
        else:
            run_load(player, item, room, mob, mem, loop=True)
    except:
        run_load(player, item, room, mob, mem, loop=True)

run = {
    "help": run_help,
    "go": run_go,
    "inventory": run_inventory,
    "wait": run_wait,
    "quit": run_quit,
    "look": run_look,
    "get": run_get,
    "drop": run_drop,
    "use": run_use,
    "attack": run_attack,
    "eat": run_eat,
    "save": run_save,
    "load": run_load
}