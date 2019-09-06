# Function to parse out language for listing items. Pass a list of items or mobs into it.
def parse_list(list):
    if len(list) > 0:
        list_string = ""
        length = len(list)
        for (ind, el) in enumerate(list):
            if ind == 0:
                list_string = el.long_name
            elif length > ind + 1:
                list_string = f"{list_string}, {el.long_name}"
            elif length == 2:
                list_string = f"{list_string} and {el.long_name}"
            else:
                list_string = f"{list_string}, and {el.long_name}"

    return list_string

single_word_replace = {
    "h": "help",
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "i": "inventory",
    "inv": "inventory",
    "l": "look",
    "examine": "look",
    "inspect": "look",
    "g": "get",
    "take": "get",
    "d": "drop",
    "leave": "drop",
    "u": "use",
    "swing": "wield",
    "q": "quit",
}

multi_word_replace = {
    "look at": "look",
    "pick up": "get",
    "put down": "drop",
    "attack with": "wield",
    "goblin corpse": "goblin_corpse",
}