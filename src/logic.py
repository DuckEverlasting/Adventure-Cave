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
    "amulet": "amulet_of_yendor"
}

multi_word_replace = {
    "look at": "look",
    "pick up": "get",
    "put down": "drop",
    "attack with": "wield",
    "goblin corpse": "goblin_corpse",
    "amulet of yendor": "amulet_of_yendor"
}

ignore_word = (
    "the",
    "go",
    "travel"
)

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

# Function to help interpret player commands
def parse_command(command):
    # Edge case
    if len(command) == 0: return ["no_command"]

    # Check input for any phrases to be simplified
    for i in multi_word_replace:
        if i in command:
            command = command.replace(i, multi_word_replace[i])

    # Split input into words
    command = command.split()

    # Check input for any words to replace with recognized commands
    for i in range(len(command)):
        if command[i] in ignore_word:
            command.pop(i)
        if command[i] in single_word_replace:
            command[i] = single_word_replace[command[i]]
    
    return command
