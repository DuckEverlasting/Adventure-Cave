from room import Room
from player import Player
from item import Item, Light_Source
from mob import Mob
from action import Action
from action_run import *
from text_style import (
    desc_text,
    item_text,
    item_in_desc_text,
    mob_text,
    mob_in_desc_text,
    dir_text,
    dir_in_desc_text,
)


# Declare the items
item = {
    "sword": Item(
        name=item_text("sword"),
        long_name=f"a {item_text('sword')}",
        desc=desc_text(
            "This sword has seen better days, but it's probably got one or two good swings left in it."
        ),
    ),
    "lantern": Light_Source(
        name=item_text("lantern"),
        long_name=f"an extinguished {item_text('lantern')}",
        desc=desc_text(
            "The lantern is unlit. It has fuel though; you imagine you could get it lit if you had some matches."
        ),
    ),
    "rope": Item(
        name=item_text("rope"),
        long_name=f"some {item_text('rope')}",
        desc=desc_text("Good, sturdy rope, about 50 feet long."),
    ),
    "goblin_corpse": Item(
        name=item_text("goblin corpse"),
        long_name=f"a {item_text('goblin corpse')}",
        desc=desc_text(
            f"It's a dead goblin. You turn it over, looking for valuables, but all you can find is a\ncrumpled {item_in_desc_text('matchbook')}, which falls to the floor next to the corpse."
        ),
        obtainable=False,
    ),
    "matchbook": Item(
        name=item_text("matchbook"),
        long_name=f"a {item_text('matchbook')}",
        desc=desc_text(
            "At first glance, the crumpled matchbook appears to be empty, but looking closer,\nyou see it still has a few matches inside."
        ),
    ),
    "lever": Item(
        name=item_text("lever"),
        long_name=f"a {item_text('lever')} jutting from the cliffside",
        desc=desc_text(
            "It looks close enough to reach. Your fingers twitch. You never could resist a good lever."
        ),
        obtainable=False,
    ),
    "amulet_of_yendor": Item(
        name=item_text("Amulet of Yendor"),
        long_name=f"the {item_text('Amulet of Yendor')}",
        desc=desc_text(
            "This amulet is said to contain unimaginable power."
        ),
    ),
}


# Declare the rooms
room = {
    "outside": Room(
        name = "Outside Cave Entrance",
        desc = desc_text(
            f"{dir_in_desc_text('North')} of you, the cave mouth beckons."
        ),
        no_mobs = True,
    ),
    "foyer": Room(
        name = "Foyer",
        desc = desc_text(
            f"Dim light filters in from the {dir_in_desc_text('south')}. Dusty passages run {dir_in_desc_text('north')} and {dir_in_desc_text('east')}."
        ),
        init_items = [item["sword"]],
    ),
    "overlook": Room(
        name = "Grand Overlook",
        desc = desc_text(
            f"A steep cliff appears before you, falling into the darkness. Ahead to the {dir_in_desc_text('north')}, a light\nflickers in the distance, but there is no way across the chasm. A passage leads {dir_in_desc_text('south')},\naway from the cliff."
        ),
        init_items = [item["rope"]],
    ),
    "narrow": Room(
        name = "Narrow Passage",
        desc = desc_text(
            f"The narrow passage bends here from {dir_in_desc_text('west')} to {dir_in_desc_text('north')}. The smell of gold permeates the air."
        ),
    ),
    "treasure": Room(
        name = "Treasure Chamber",
        desc = desc_text(
            f"You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by\nearlier adventurers. The only exit is to the {dir_in_desc_text('south')}."
        ),
        init_items = [item["lantern"]],
    ),
    "chasm": Room(
        name = "Over The Edge",
        desc = desc_text(
            f"You find yourself suspended over a dark chasm, at the end of a rope that was clearly not\nlong enough for this job. Glancing about, you see a {item_in_desc_text('lever')} jutting out from the wall, half hidden.\nThe rope leads back {dir_in_desc_text('up')}."
        ),
        dark = True,
        dark_desc = desc_text(
            f"You find yourself suspended over a dark chasm, at the end of a rope that was clearly not\nlong enough for this job. It is dark. You can't see a thing. You are likely to be eaten by a grue.\nThe rope leads back {dir_in_desc_text('up')}."
        ),
        no_mobs = True,
        no_drop = True,
        init_items=[item["lever"]]
    ),
    "final": Room(
        name = "Across the Chasm",
        desc = desc_text(
            f"You find a small, elaborately decorated room. Sunlight streams down a hole in the ceiling high\nabove you, illuminating an altar upon which sits the fabled {item_in_desc_text('Amulet of Yendor')}.\nTo the {dir_in_desc_text('south')}, a bridge leads back the way you came."
        ),
        init_items=[item["amulet_of_yendor"]]
    ),
}


# Declare the mobs
mob = {
    "goblin": Mob(
        name = mob_text("goblin"),
        long_name = f"a {mob_text('goblin')}",
        desc = desc_text(
            f"The {mob_in_desc_text('goblin')} is eyeing you warily and shuffling his weight from one foot to the other.\nA crude knife dangles from his belt."
        ),
        enter_text = f"A {mob_text('goblin')} shuffles into the room. At the sight of you, he gives a squeal of surprise and bares his teeth.",
        exit_text = f"The {mob_text('goblin')} skitters out of the room, heading ",
        idle_text = (
            f"The {mob_text('goblin')} grumbles nervously about how crowded the cave has gotten lately.",
            f"The {mob_text('goblin')} pulls out a knife, then thinks better of it and puts the knife back.",
            f"The {mob_text('goblin')} is momentarily transfixed by a rash on his elbow.",
        ),
        init_loc = room["foyer"],
    )
}

# Declare the actions
action = {
    "help": Action(
        name = "help",
        grammar = {
            "d_obj_prohibited": True,
            "i_obj_prohibited": True,
        },
        run = run_help
    ),
    "go": Action(
        name = "go",
        grammar = {
            "adv_required": True,
        },
        run = run_go
    ),
    "inventory": Action(
        name = "inventory",
        grammar = {

        },
        run = run_inventory
    ),
    "wait": Action(
        name = "wait",
        grammar = {},
        run = run_wait
    ),
    "quit": Action(
        name = "quit",
        grammar = {
            "d_obj_prohibited": True,
            "i_obj_prohibited": True,
        },
        run = run_quit
    ),
    "look": Action(
        name = "look",
        grammar = {
            "d_obj_prohibited": True,
            "preps_accepted": ("at", "in", "into", "inside", "beneath", "underneath", "under", "below", )
        },
        run = run_look
    ),
    "get": Action(
        name = "get",
        grammar = {
            "d_obj_required": True,
            "i_obj_prohibited": True,
        },
        run = run_get
    ),
    "drop": Action(
        name = "drop",
        grammar = {
            "d_obj_required": True,
            "i_obj_prohibited": True,
        },
        run = run_drop
    ),
    "use": Action(
        name = "use",
        grammar = {
            "d_obj_required": True,
            "preps_accepted": ("with", "on",)
        },
        run = run_use
    ),
    "attack": Action(
        name = "attack",
        grammar = {
            "d_obj_required": True,
            "preps_accepted": ("with", "using"),
        },
        run = run_attack
    ),
    "eat": Action(
        name = "eat",
        grammar = {
            "d_obj_required": True,
            "i_obj_prohibited": True,
        },
        run = run_eat
    ),
}

# Declare the player
player = Player(init_loc = room["outside"])

# Link rooms together
room["outside"].n_to = (room["foyer"], "You step into the mouth of the cave.")
room["foyer"].s_to = (room["outside"], "You head south, and find yourself outside the cave.")
room["foyer"].n_to = (room["overlook"], "You make your way north, and the cave opens up suddenly, revealing a vast chasm before you.")
room["foyer"].e_to = (room["narrow"], "You take the eastern passage. It grows narrower until you have a hard time standing straight.")
room["overlook"].s_to = (room["foyer"], "You step back from the cliff's edge and head south.")
room["overlook"].n_to = (room["overlook"], "You take a step back, and get ready to jump over the gap. Then you realize that is an\nincredibly stupid idea, and decide you would rather live.")
room["narrow"].w_to = (room["foyer"], "You move west through the cramped passage until it opens up a bit.")
room["narrow"].n_to = (room["treasure"], "You follow your nose and head north.")
room["treasure"].s_to = (room["narrow"], "You head south into the narrow passage.")
room["chasm"].u_to = (room["overlook"], "You climb slowly back up the rope, and pull yourself back onto the overlook, panting.")
room["final"].s_to = (room["overlook"], "You go back across the bridge, resisting the pull of the amulet.")


# Add functionality to items

# sword
def use_sword():
    if mob["goblin"].loc == player.loc:
        print(
            f"You swing the {item_text('sword')} wildly at the {mob_text('goblin')}, and somehow manage to connect. He cries out in shock,\nthen gives you a baleful glare that fades into a look of weary resignation as he slumps to the ground.\n"
        )
        mob["goblin"].kill()
        player.loc.add_item(item["goblin_corpse"])
    else:
        if player.loc.no_drop:
            print(f"This isn't a great place to mess around with your {item_text('sword')}. You leave it be.")
            return False
        else:
            print(
                f"You swing the {item_text('sword')} around wildly. After a few wide arcs, it slips out of your fingers and clatters to the ground.\n"
            )
            player.drop_item(item["sword"], quiet = True)
    
    return True

item["sword"].use = use_sword

# rope
def use_rope():
    if player.loc == room["overlook"]:
        print(
            f"You tie off one end of the {item_text('rope')} to a convenient stalagmite and drop the rest off the cliff.\n"
        )

        # remove from inventory
        player.drop_item(item["rope"], quiet = True)

        # modify the room
        room["overlook"].desc = desc_text(
            f"A steep cliff appears before you, falling into the darkness. Ahead to the {dir_in_desc_text('north')}, a light\nflickers in the distance, but there is no way across the chasm. A passage leads {dir_in_desc_text('south')},\naway from the cliff. A tied off rope offers a way {dir_in_desc_text('down')}."
        )
        room["overlook"].d_to = (
            room["chasm"],
            "You climb down the rope, and make it about a third of the way\ndown the cliff before you reach the end of the line. Oh dear.",
        )

        # modify the item
        item["rope"].long_name = f"a tied off length of {item_text('rope')}"
        item["rope"].desc = desc_text(
            "The rope looks pretty sturdy. It will probably hold your weight. Probably."
        )
        item["rope"].obtainable = False

        def use_from_env_rope():
            player.move("d")
            return True

        item["rope"].use_from_env = use_from_env_rope

    else:
        print(f"You try to use the {item_text('rope')} as a lasso, and fail miserably.")
    
    return True

item["rope"].use = use_rope

# lantern
def use_lantern():
    if item["matchbook"] in player.items:
        if item["lantern"].active:
            print(f"The lantern is already lit.\n")
            return False
        else:
            item["lantern"].active = True
            item["lantern"].long_name = f"a lit {item_text('lantern')}"
            item["lantern"].desc = f"The {item_text('lantern')} is giving off a warm glow."
            print(f"You strike a match and light the lantern. The room brightens.\n")
            return True
    else:
        print("You don't have anything to light it with.")
        return False

item["lantern"].use = use_lantern

# matchbook
def use_matchbook():
    if item["lantern"] in player.items:
        if item["lantern"].active:
            print(f"The lantern is already lit.\n")
            return False
        else:
            item["lantern"].active = True
            print(f"You strike a match and light the lantern. The room brightens.\n")
            return True
    else:
        print("You don't have anything you want to light on fire.\n")
        return False

item["matchbook"].use = use_matchbook

# goblin_corpse
def on_look_goblin_corpse():
    item["goblin_corpse"].desc = "It's a dead goblin. You don't want to touch it again."
    player.loc.add_item(item["matchbook"])
    delattr(item["goblin_corpse"], "on_look")

item["goblin_corpse"].on_look = on_look_goblin_corpse

def eat_goblin_corpse():
    print("What? No. That's just... no.\n\nGross.\n")
    return False

item["goblin_corpse"].eat = eat_goblin_corpse

# lever
def use_from_env_lever():
    if player.light_check():
        print("You pull the lever. A loud rinding noise echoes through the chasm. You nearly lose your grip but\nmanage to hold on as a bridge lowers from the ceiling of the cave, shuddering into place\nabove you. Looks like you can cross the chasm now. What are the odds that lever would be in this exact\nplace on the cliff side?\n")
        room["overlook"].desc = desc_text(
            f"A steep cliff appears before you, falling into the darkness. Ahead to the {dir_in_desc_text('north')}, a narrow bridge\nhas been lowered, leading to a light flickering in the distance. A passage leads {dir_in_desc_text('south')}, away from the cliff.\nA tied off rope offers a way {dir_in_desc_text('down')}."
        )
        room["overlook"].n_to = (room["final"], "You carefully walk across the bridge, heading towards the light on the other side.")
        return True
    else:
        print(f"It's too dark for that right now. Also, how do you know about the {item_text('lever')}, cheater?\n")
        return False

item["lever"].use_from_env = use_from_env_lever