from text_style import error_text


class Player:
    def __init__(self, init_loc, init_items=[]):
        self.loc = init_loc
        self.items = init_items
        self.health = 10
        self.strength = 10
        self.accuracy = 10
        self.evasion = 10
        self.status = "normal"
        self.load = sum(i.weight for i in self.items)
        self.max_load = 10

    def light_check(self):
        light_source = False
        for i in self.items:
            try:
                if i.active: light_source = True
            except:
                pass
        for i in self.loc.items:
            try:
                if i.active: light_source = True
            except:
                pass
        return light_source

    def move(self, dir):
        if hasattr(self.loc, f"{dir}_to"):
            dest = getattr(self.loc, f"{dir}_to")
            self.loc = dest[0]
            print(f"{dest[1]}\n")
            return True
        else:
            print(error_text("ERROR: MOVEMENT NOT ALLOWED\n"))
            return False

    def look_item(self, item):
        if item in self.items or item in self.loc.items:
            print(f"{item.desc}\n")
            item.on_look()
            return True
        else:
            print("There's nothing here by that name.\n")
            return False

    def look_mob(self, mob):
        if mob.loc == self.loc:
            print(f"{mob.desc}\n")
            mob.on_look()
            return True
        else:
            print("There's nothing here by that name.\n")
            return False

    def get_item(self, item):
        if item in self.loc.items:
            result = self.loc.remove_item(item)
            if result:
                if self.load + item.weight > self.max_load:
                    print(f"Your pack is too full for the {item.name}.\n")
                    return False
                else:
                    self.items.append(item)
                    self.load += item.weight
                    print(f"You pick up the {item.name}.\n")
                    item.on_pick_up()
                    return True
            else:
                return False
        else:
            print("There's nothing here by that name.\n")
            return False

    def drop_item(self, item, quiet=False):
        if item in self.items:
            if self.loc.no_drop:
                print("You don't think that's a good idea here.\n")
                return False
            self.items.remove(item)
            if quiet == False:
                print(f"You set down the {item.name}.\n")
            self.load -= item.weight
            self.loc.add_item(item)
            return True
        else:
            print("You don't have one of those in your inventory\n")
            return False
    
    def use_item(self, item, target):
        if item in self.items:
            return item.use(target)
        
        elif item in self.loc.items:
            return item.use_from_env(target)
                
        else:
            print("There's nothing here by that name.\n")
            return False
    
    def attack_mob(self, item, target):
        pass
    
    def eat_item(self, item):
        if item in self.items:
            return item.eat(self)
        
        elif item in self.loc.items:
            return item.eat(self.loc)

                
        else:
            print("There's nothing here by that name.\n")
            return False