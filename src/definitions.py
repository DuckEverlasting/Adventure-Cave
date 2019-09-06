from room import Room
from player import Player
from item import Item
from mob import Mob
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
    "lantern": Item(
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
            "At first glance, the crumpled matchbook appears to be empty, but looking closer,\nyou see it still has one match inside."
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
            f"A steep cliff appears before you, falling into the darkness. Ahead to the {dir_in_desc_text('north')}, a light\nflickers in the distance, but there is no way across the chasm.\nA passage leads {dir_in_desc_text('south')}, away from the cliff."
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
            f"You find yourself suspended over a dark chasm, at the end of a rope that was clearly not\nlong enough for this job. It is dark. You can't see a thing. You are likely to be eaten by a grue.\nThe rope leads back {dir_in_desc_text('up')}."
        ),
        no_mobs = True,
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
        init_loc = room["foyer"],
    )
}


# Declare the player
player = Player(init_loc = room["outside"])


# Link rooms together
room["outside"].n_to = (room["foyer"], "You step into the mouth of the cave.")
room["foyer"].s_to = (
    room["outside"],
    "You head south, and find yourself outside the cave.",
)
room["foyer"].n_to = (
    room["overlook"],
    "You make your way north, and the cave opens up suddenly, revealing a vast chasm before you.",
)
room["foyer"].e_to = (
    room["narrow"],
    "You take the eastern passage. It grows narrower until you have a hard time standing straight.",
)
room["overlook"].s_to = (
    room["foyer"],
    "You step back from the cliff's edge and head south.",
)
room["narrow"].w_to = (
    room["foyer"],
    "You move west through the cramped passage until it opens up a bit.",
)
room["narrow"].n_to = (room["treasure"], "You follow your nose and head north.")
room["treasure"].s_to = (room["narrow"], "You head south into the narrow passage.")
room["chasm"].u_to = (
    room["overlook"],
    "You climb slowly back up the rope, and pull yourself back onto the overlook, panting.",
)


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
        print(
            f"You swing the {item_text('sword')} around wildly. After a few wide arcs, it slips out of your fingers and clatters to the ground.\n"
        )
        player.remove_item(item["sword"])
        player.loc.add_item(item["sword"])


item["sword"].use = use_sword

# rope
def use_rope():
    if player.loc == room["overlook"]:
        print(
            f"You tie off one end of the {item_text('rope')} to a convenient stalagmite and drop the rest off the cliff.\n"
        )

        # remove from inventory
        player.remove_item(item["rope"])

        # modify the room
        room["overlook"].add_item(item["rope"])
        room["overlook"].desc = desc_text(
            f"A steep cliff appears before you, falling into the darkness. Ahead to the {dir_in_desc_text('north')}, a light\nflickers in the distance, but there is no way across the chasm.\nA passage leads {dir_in_desc_text('south')}, away from the cliff. A tied off rope offers a way {dir_in_desc_text('down')}."
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

        item["rope"].use_from_env = use_from_env_rope

    else:
        print(f"You try to use the {item_text('rope')} as a lasso, and fail miserably.")


item["rope"].use = use_rope

# lantern
def use_lantern():
    pass


item["lantern"].use = use_lantern


def use_matchbook():
    pass


item["matchbook"].use = use_matchbook


def on_look_goblin_corpse():
    item["goblin_corpse"].desc = "It's a dead goblin. You don't want to touch it again."
    player.loc.add_item(item["matchbook"])
    delattr(item["goblin_corpse"], "on_look")


item["goblin_corpse"].on_look = on_look_goblin_corpse
