from text_style import error_text


class Player:
    def __init__(self, init_loc, init_items=[]):
        self.loc = init_loc
        self.items = init_items

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
                self.items.append(item)
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
            self.loc.add_item(item)
            return True
        else:
            print("You don't have one of those in your inventory\n")
            return False
    
    def use_item(self, item):
        if item in self.items:
            return item.use()
        
        elif item in self.loc.items:
            return item.use_from_env()
                
        else:
            print("There's nothing here by that name.\n")
            return False
    
    def eat_item(self, item):
        if item in self.items:
            return item.eat()
        
        elif item in self.loc.items:
            return item.eat()
                
        else:
            print("There's nothing here by that name.\n")
            return False