multi_word_replace = {
    "look at": "look",
    "pick up": "get",
    "put down": "drop",
    "attack with": "wield",
    "goblin corpse": "goblin_corpse",
    "amulet of yendor": "amulet_of_yendor",
    "up to": "up_to",
    "out of": "out_of"
}

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

ignore_words = (
    "the",
    "a",
    "an",
    "and"
)

prepositions = (
    "with",
    "using",
    "at",
    "toward",
    "to",
    "beneath",
    "underneath",
    "under",
    "below",
    "above",
    "over",
    "on",
    "onto",
    "upon",
    "by",
    "in",
    "inside",
    "into",
    "up_to",
    "against",
    "from",
    "out_of"
)

# Function to help interpret player commands
def parse_command(command):
    error = {
                "action": "error",
                "d_obj": None,
                "prep": None,
                "i_obj": None,
            }
    # Edge case
    if len(command) == 0: return error

    # Check input for any phrases to be simplified
    for i in multi_word_replace:
        if i in command:
            command = command.replace(i, multi_word_replace[i])

    # Split input into words
    command = command.split()

    # Remove unnecessary words
    command = [i for i in command if not i in ignore_words]

    # Check input for any words to replace with recognized commands
    for i in range(len(command)):
        if command[i] in single_word_replace:
            command[i] = single_word_replace[command[i]]
    
   
    # Declare return object, set action
    result = {
        "action": command[0],
        "d_obj": None,
        "prep": None,
        "i_obj": None,
    }

    # Check for movement shortcuts
    if command in (["north"], ["south"], ["east"], ["west"], ["up"], ["down"]):
        return {
            "action": "go",
            "dir": command[0],
            "d_obj": None,
            "prep": None,
            "i_obj": None,
        }

    # Filter out action (because it's already set)
    command.pop(0)

    # Check for preposition, define indirect object if one is found
    prep = None
    for i in range(len(command)):
        if command[i] in prepositions:
            if prep: return error
            prep = [command[i]]
            try:
                i_obj = command[i + 1]
            except:
                return error

    # Filter out preposition, indirect object
    if prep:
        command.remove(prep)
        command.remove(i_obj)
    
    # if anything is left, it's the direct object
    if len(command) > 1:
        return error
    
    try:
        result["d_obj"] = command[0]
    except:
        pass

    try:
        result["prep"] = prep
    except:
        pass

    try:        
        result["i_obj"] = i_obj
    except:
        pass

    return result

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