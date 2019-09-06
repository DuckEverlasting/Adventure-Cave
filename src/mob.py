import random
from text_style import dir_text


class Mob:
    def __init__(self, name, long_name, desc, enter_text, exit_text, init_loc):
        self.name = name
        self.long_name = long_name
        self.desc = desc
        self.enter_text = enter_text
        self.exit_text = exit_text
        self.loc = init_loc
        self.prev_loc = None
        self.alive = True

    def __str__(self):
        return self.name

    # def move(self, dir):
    #     if hasattr(self.loc, f"{dir}_to"):
    #         dest = getattr(self.loc, f"{dir}_to")
    #         self.loc = dest[0]
    #         return True
    #     else:
    #         return False
    
    def moveRand(self):
        directions = {
            "n_to": dir_text("north"),
            "s_to": dir_text("south"),
            "e_to": dir_text("east"),
            "w_to": dir_text("west")
        }

        if random.randint(0, 2) != 0:
            return False
        else:
            possibleMoves = [i for i in (directions.keys()) if hasattr(self.loc, i)]
            dir_to = random.choice(possibleMoves)
            dest = getattr(self.loc, dir_to)
            self.prev_loc = self.loc
            self.loc = dest[0]
            return directions[dir_to]
    
    def kill(self):
        self.alive = False
        self.loc = None